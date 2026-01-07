import pandas as pd
import sqlite3
import re
import os

# --- Configuration ---
# Get current script directory to find relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level to find 'data' folder
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DB_NAME = "fleximart.db"

# Input Files
DATA_FILES = {
    "customers": os.path.join(DATA_DIR, "customers_raw.csv"),
    "products": os.path.join(DATA_DIR, "products_raw.csv"),
    "sales": os.path.join(DATA_DIR, "sales_raw.csv")
}

def clean_phone(phone):
    """Standardizes phone numbers to +91-XXXXXXXXXX format."""
    if pd.isna(phone):
        return None
    s = str(phone)
    if 'e' in s.lower():
        try:
            s = str(int(float(phone)))
        except:
            pass
    digits = re.sub(r'\D', '', s)
    if len(digits) >= 10:
        return f"+91-{digits[-10:]}"
    return None

def robust_date_parse(date_str):
    """
    Tries multiple formats to parse dates (handles mixed US/UK formats).
    Returns YYYY-MM-DD string or None if failed.
    """
    if pd.isna(date_str):
        return None
    
    # Force string type
    d = str(date_str).strip()
    
    try:
        # Try 1: Auto-detect (works for ISO YYYY-MM-DD)
        return pd.to_datetime(d).strftime('%Y-%m-%d')
    except:
        try:
            # Try 2: Day First (DD-MM-YYYY or DD/MM/YYYY)
            return pd.to_datetime(d, dayfirst=True).strftime('%Y-%m-%d')
        except:
            try:
                # Try 3: Month First (MM-DD-YYYY or MM/DD/YYYY)
                return pd.to_datetime(d, dayfirst=False).strftime('%Y-%m-%d')
            except:
                return None

def extract_data():
    print("--- Extracting Data ---")
    dfs = {}
    for name, file in DATA_FILES.items():
        if os.path.exists(file):
            dfs[name] = pd.read_csv(file)
            print(f"Loaded {name}: {len(dfs[name])} records")
        else:
            raise FileNotFoundError(f"Missing file: {file}")
    return dfs

def transform_data(dfs):
    print("\n--- Transforming Data ---")
    
    # 1. CLEAN CUSTOMERS
    cust = dfs['customers'].copy()
    cust = cust.drop_duplicates()
    cust = cust.dropna(subset=['email'])
    cust['phone'] = cust['phone'].apply(clean_phone)
    
    # Clean Dates (Customers usually have consistent DD-MM-YYYY)
    cust['registration_date'] = cust['registration_date'].apply(robust_date_parse)
    
    cust = cust.reset_index(drop=True)
    cust['new_customer_id'] = cust.index + 1
    cust_map = dict(zip(cust['customer_id'], cust['new_customer_id']))
    
    # 2. CLEAN PRODUCTS
    prod = dfs['products'].copy()
    prod = prod.drop_duplicates()
    prod = prod.dropna(subset=['price'])
    prod['stock_quantity'] = prod['stock_quantity'].fillna(0)
    prod['category'] = prod['category'].str.title()
    
    prod = prod.reset_index(drop=True)
    prod['new_product_id'] = prod.index + 1
    prod_map = dict(zip(prod['product_id'], prod['new_product_id']))

    # 3. CLEAN SALES
    sales = dfs['sales'].copy()
    sales = sales.drop_duplicates()
    sales = sales.dropna(subset=['customer_id', 'product_id'])
    
    sales['customer_id'] = sales['customer_id'].map(cust_map)
    sales['product_id'] = sales['product_id'].map(prod_map)
    # Drop orphans
    sales = sales.dropna(subset=['customer_id', 'product_id'])
    
    # Fix Dates: Apply robust parser
    sales['transaction_date'] = sales['transaction_date'].apply(robust_date_parse)
    
    # CRITICAL FIX: Drop rows where date parsing failed (prevents DB crash)
    before_date_drop = len(sales)
    sales = sales.dropna(subset=['transaction_date'])
    if len(sales) < before_date_drop:
        print(f"Warning: Dropped {before_date_drop - len(sales)} sales records due to invalid dates.")

    sales['subtotal'] = sales['quantity'] * sales['unit_price']
    
    return cust, prod, sales

def load_data(cust, prod, sales):
    print("\n--- Loading Data to Database ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        city VARCHAR(50),
        registration_date DATE
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INT DEFAULT 0
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT NOT NULL,
        order_date DATE NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending',
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        unit_price DECIMAL(10,2) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)

    # 1. Load Customers
    cust_data = cust[['new_customer_id', 'first_name', 'last_name', 'email', 'phone', 'city', 'registration_date']]
    cust_data = cust_data.rename(columns={'new_customer_id': 'customer_id'})
    cust_data.to_sql('customers', conn, if_exists='append', index=False)
    
    # 2. Load Products
    prod_data = prod[['new_product_id', 'product_name', 'category', 'price', 'stock_quantity']]
    prod_data = prod_data.rename(columns={'new_product_id': 'product_id'})
    prod_data.to_sql('products', conn, if_exists='append', index=False)
    
    # 3. Load Orders
    # Group sales by transaction to create Orders
    orders = sales.groupby('transaction_id').agg({
        'customer_id': 'first',
        'transaction_date': 'first',
        'subtotal': 'sum',
        'status': 'first'
    }).reset_index()
    
    orders['order_id'] = range(1, len(orders) + 1)
    
    orders_load = orders[['order_id', 'customer_id', 'transaction_date', 'subtotal', 'status']]
    orders_load.columns = ['order_id', 'customer_id', 'order_date', 'total_amount', 'status']
    orders_load.to_sql('orders', conn, if_exists='append', index=False)
    
    # 4. Load Order Items
    tx_map = dict(zip(orders['transaction_id'], orders['order_id']))
    sales['order_id'] = sales['transaction_id'].map(tx_map)
    
    sales['order_item_id'] = range(1, len(sales) + 1)
    items_load = sales[['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'subtotal']]
    items_load.to_sql('order_items', conn, if_exists='append', index=False)

    conn.commit()
    print("Data loaded successfully into 'fleximart.db'")
    conn.close()

def generate_report(raw_data, clean_cust, clean_prod, clean_sales):
    print("\n--- Generating Data Quality Report ---")
    
    cust_raw = len(raw_data['customers'])
    cust_clean = len(clean_cust)
    cust_dropped = cust_raw - cust_clean
    
    prod_raw = len(raw_data['products'])
    prod_clean = len(clean_prod)
    prod_dropped = prod_raw - prod_clean
    
    sales_raw = len(raw_data['sales'])
    sales_clean = len(clean_sales)
    sales_dropped = sales_raw - sales_clean
    
    report_content = f"""DATA QUALITY REPORT
===================
Generated by: FlexiMart ETL Pipeline
-----------------------------------

FILE 1: CUSTOMERS (customers_raw.csv)
-------------------------------------
- Total records processed:       {cust_raw}
- Records dropped (dupes/missing/invalid dates): {cust_dropped}
- Records loaded successfully:   {cust_clean}

FILE 2: PRODUCTS (products_raw.csv)
-----------------------------------
- Total records processed:       {prod_raw}
- Records dropped (dupes/missing): {prod_dropped}
- Records loaded successfully:   {prod_clean}

FILE 3: SALES (sales_raw.csv)
-----------------------------
- Total records processed:       {sales_raw}
- Records dropped (dupes/missing/orphans/dates): {sales_dropped}
- Records loaded successfully:   {sales_clean}

===================================
TOTAL SUMMARY
===================================
- Total Raw Records:             {cust_raw + prod_raw + sales_raw}
- Total Cleaned Records Loaded:  {cust_clean + prod_clean + sales_clean}
"""
    with open("data_quality_report.txt", "w") as f:
        f.write(report_content)
    print("Report generated: data_quality_report.txt")

if __name__ == "__main__":
    try:
        raw_data = extract_data()
        clean_cust, clean_prod, clean_sales = transform_data(raw_data)
        load_data(clean_cust, clean_prod, clean_sales)
        generate_report(raw_data, clean_cust, clean_prod, clean_sales)
        print("\nETL Pipeline Completed Successfully!")
    except Exception as e:
        print(f"\nETL Pipeline Failed: {e}")
