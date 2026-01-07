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

DATA_FILES = {
    "customers": os.path.join(DATA_DIR, "customers_raw.csv"),
    "products": os.path.join(DATA_DIR, "products_raw.csv"),
    "sales": os.path.join(DATA_DIR, "sales_raw.csv")
}

def clean_phone(phone):
    """Standardizes phone numbers to +91-XXXXXXXXXX format."""
    if pd.isna(phone):
        return None
    
    # Convert scientific notation/floats to string
    s = str(phone)
    if 'e' in s.lower():
        try:
            s = str(int(float(phone)))
        except:
            pass
            
    # Remove non-digit characters
    digits = re.sub(r'\D', '', s)
    
    # Extract last 10 digits
    if len(digits) >= 10:
        return f"+91-{digits[-10:]}"
    return None

def extract_data():
    """Reads CSV files into DataFrames."""
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
    """Cleans and transforms the data."""
    print("\n--- Transforming Data ---")
    
    # 1. CLEAN CUSTOMERS
    cust = dfs['customers'].copy()
    initial_cust = len(cust)
    
    # Remove duplicates
    cust = cust.drop_duplicates()
    
    # Handle missing emails (Drop records as email is UNIQUE NOT NULL)
    cust = cust.dropna(subset=['email'])
    
    # Standardize Phone
    cust['phone'] = cust['phone'].apply(clean_phone)
    
    # Standardize Date (Handle mixed formats like DD-MM-YYYY or MM-DD-YYYY)
    cust['registration_date'] = pd.to_datetime(
        cust['registration_date'], dayfirst=True, errors='coerce'
    ).dt.strftime('%Y-%m-%d')
    
    # Add Surrogate Key (New Integer ID)
    cust = cust.reset_index(drop=True)
    cust['new_customer_id'] = cust.index + 1
    
    # Create Mapping for FKs: {Old_ID: New_ID}
    cust_map = dict(zip(cust['customer_id'], cust['new_customer_id']))
    
    print(f"Customers cleaned: {len(cust)} (dropped {initial_cust - len(cust)} duplicates/missing)")

    # 2. CLEAN PRODUCTS
    prod = dfs['products'].copy()
    initial_prod = len(prod)
    
    # Remove duplicates
    prod = prod.drop_duplicates()
    
    # Handle missing prices (Drop)
    prod = prod.dropna(subset=['price'])
    
    # Fill missing stock with 0
    prod['stock_quantity'] = prod['stock_quantity'].fillna(0)
    
    # Standardize Category
    prod['category'] = prod['category'].str.title()
    
    # Add Surrogate Key
    prod = prod.reset_index(drop=True)
    prod['new_product_id'] = prod.index + 1
    prod_map = dict(zip(prod['product_id'], prod['new_product_id']))
    
    print(f"Products cleaned: {len(prod)} (dropped {initial_prod - len(prod)} duplicates/missing)")

    # 3. CLEAN SALES (Transactions)
    sales = dfs['sales'].copy()
    initial_sales = len(sales)
    
    # Remove duplicates
    sales = sales.drop_duplicates()
    
    # Remove rows with missing IDs
    sales = sales.dropna(subset=['customer_id', 'product_id'])
    
    # Map Foreign Keys (Replace C001 with 1, P001 with 1, etc.)
    sales['customer_id'] = sales['customer_id'].map(cust_map)
    sales['product_id'] = sales['product_id'].map(prod_map)
    
    # Drop Orphaned Records (Sales where customer/product was deleted in previous steps)
    sales = sales.dropna(subset=['customer_id', 'product_id'])
    
    # Standardize Date
    # Uses 'mixed' format inference to handle differences like 15-01-2023 and 01-22-2024
    sales['transaction_date'] = pd.to_datetime(
        sales['transaction_date'], dayfirst=False, errors='coerce'
    ).dt.strftime('%Y-%m-%d')
    
    # Calculate Subtotals
    sales['subtotal'] = sales['quantity'] * sales['unit_price']
    
    print(f"Sales cleaned: {len(sales)} (dropped {initial_sales - len(sales)} duplicates/invalid)")

    return cust, prod, sales

def load_data(cust, prod, sales):
    """Loads data into SQLite database."""
    print("\n--- Loading Data to Database ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Tables (Based on Schema)
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
    cust_data.to_sql('customers', conn, if_exists='append', index=False, header=False)
    
    # 2. Load Products
    prod_data = prod[['new_product_id', 'product_name', 'category', 'price', 'stock_quantity']]
    prod_data.to_sql('products', conn, if_exists='append', index=False, header=False)
    
    # 3. Load Orders & Order Items
    # Group sales by transaction to create Orders
    orders = sales.groupby('transaction_id').agg({
        'customer_id': 'first',
        'transaction_date': 'first',
        'subtotal': 'sum',
        'status': 'first'
    }).reset_index()
    
    # Assign Order IDs
    orders['order_id'] = range(1, len(orders) + 1)
    
    # Load Orders
    orders_load = orders[['order_id', 'customer_id', 'transaction_date', 'subtotal', 'status']]
    orders_load.to_sql('orders', conn, if_exists='append', index=False, header=False)
    
    # Map Transaction ID to Order ID for Items
    tx_map = dict(zip(orders['transaction_id'], orders['order_id']))
    sales['order_id'] = sales['transaction_id'].map(tx_map)
    
    # Load Order Items
    sales['order_item_id'] = range(1, len(sales) + 1)
    items_load = sales[['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'subtotal']]
    items_load.to_sql('order_items', conn, if_exists='append', index=False, header=False)

    conn.commit()
    print("Data loaded successfully into 'fleximart.db'")
    conn.close()

if __name__ == "__main__":
    try:
        raw_data = extract_data()
        clean_cust, clean_prod, clean_sales = transform_data(raw_data)
        load_data(clean_cust, clean_prod, clean_sales)
        print("\nETL Pipeline Completed Successfully!")
    except Exception as e:

        print(f"\nETL Pipeline Failed: {e}")
