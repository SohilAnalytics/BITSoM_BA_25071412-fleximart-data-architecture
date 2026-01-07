-- ================================
-- dim_date (Jan–Feb 2024, 30 rows)
-- ================================
INSERT INTO dim_date VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,false),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,false),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,false),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,false),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,false),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,true),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,true),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,false),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,false),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,false),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,false),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,false),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,true),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,true),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,false),
(20240116,'2024-01-16','Tuesday',16,1,'January','Q1',2024,false),
(20240117,'2024-01-17','Wednesday',17,1,'January','Q1',2024,false),
(20240118,'2024-01-18','Thursday',18,1,'January','Q1',2024,false),
(20240119,'2024-01-19','Friday',19,1,'January','Q1',2024,false),
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,true),
(20240121,'2024-01-21','Sunday',21,1,'January','Q1',2024,true),
(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,false),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,false),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,true),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,true),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,false),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,false),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,false),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,false),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,false);

-- ================================
-- dim_product (15 products, 3 categories)
-- ================================
INSERT INTO dim_product (product_id,product_name,category,subcategory,unit_price) VALUES
('P001','Laptop','Electronics','Computers',55000),
('P002','Smartphone','Electronics','Mobiles',30000),
('P003','Headphones','Electronics','Audio',2500),
('P004','LED TV','Electronics','TV',45000),
('P005','Tablet','Electronics','Gadgets',20000),
('P006','T-Shirt','Clothing','Men',800),
('P007','Jeans','Clothing','Men',1800),
('P008','Dress','Clothing','Women',2500),
('P009','Jacket','Clothing','Winter',4000),
('P010','Shoes','Clothing','Footwear',3500),
('P011','Mixer Grinder','Home Appliances','Kitchen',6000),
('P012','Microwave','Home Appliances','Kitchen',12000),
('P013','Refrigerator','Home Appliances','Large',35000),
('P014','Washing Machine','Home Appliances','Large',28000),
('P015','Iron','Home Appliances','Small',1500);

-- ================================
-- dim_customer (12 customers, 4 cities)
-- ================================
INSERT INTO dim_customer (customer_id,customer_name,city,state,customer_segment) VALUES
('C001','John Doe','Mumbai','Maharashtra','Retail'),
('C002','Jane Smith','Delhi','Delhi','Retail'),
('C003','Amit Shah','Ahmedabad','Gujarat','Corporate'),
('C004','Priya Mehta','Mumbai','Maharashtra','Retail'),
('C005','Ravi Kumar','Bengaluru','Karnataka','Corporate'),
('C006','Neha Singh','Delhi','Delhi','Retail'),
('C007','Arjun Rao','Bengaluru','Karnataka','Retail'),
('C008','Sneha Patel','Ahmedabad','Gujarat','Retail'),
('C009','Vikas Jain','Mumbai','Maharashtra','Corporate'),
('C010','Anita Verma','Delhi','Delhi','Retail'),
('C011','Karan Malhotra','Bengaluru','Karnataka','Corporate'),
('C012','Pooja Desai','Ahmedabad','Gujarat','Retail');

-- ================================
-- fact_sales (40 transactions)
-- ================================
INSERT INTO fact_sales (date_key,product_key,customer_key,quantity_sold,unit_price,discount_amount,total_amount) VALUES
(20240106,1,1,1,55000,5000,50000),
(20240106,2,2,2,30000,2000,58000),
(20240107,3,3,4,2500,0,10000),
(20240107,6,4,5,800,0,4000),
(20240113,4,5,1,45000,3000,42000),
(20240113,7,6,2,1800,0,3600),
(20240114,8,7,1,2500,0,2500),
(20240114,9,8,1,4000,0,4000),
(20240120,10,9,2,3500,500,6500),
(20240120,11,10,1,6000,0,6000),
(20240121,12,11,1,12000,1000,11000),
(20240121,13,12,1,35000,2000,33000),
(20240105,14,1,1,28000,1500,26500),
(20240110,15,2,3,1500,0,4500),
(20240111,6,3,4,800,0,3200),
(20240112,7,4,2,1800,0,3600),
(20240115,1,5,1,55000,5000,50000),
(20240116,2,6,1,30000,2000,28000),
(20240117,3,7,2,2500,0,5000),
(20240118,4,8,1,45000,3000,42000),
(20240203,5,9,2,20000,1000,39000),
(20240203,6,10,6,800,0,4800),
(20240204,7,11,2,1800,0,3600),
(20240204,8,12,1,2500,0,2500),
(20240205,9,1,1,4000,0,4000),
(20240205,10,2,2,3500,500,6500),
(20240206,11,3,1,6000,0,6000),
(20240206,12,4,1,12000,1000,11000),
(20240207,13,5,1,35000,2000,33000),
(20240207,14,6,1,28000,1500,26500),
(20240208,15,7,2,1500,0,3000),
(20240208,1,8,1,55000,5000,50000),
(20240209,2,9,1,30000,2000,28000),
(20240209,3,10,3,2500,0,7500),
(20240108,4,11,1,45000,3000,42000),
(20240109,5,12,1,20000,1000,19000),
(20240122,6,1,5,800,0,4000),
(20240123,7,2,2,1800,0,3600),
(20240124,8,3,1,2500,0,2500),
(20240125,9,4,1,4000,0,4000);
