context = """
<scheme>
Customers:
- customer_id INTEGER PRIMARY KEY
- first_name TEXT
- last_name TEXT
- email TEXT
- phone TEXT
- address TEXT
- city TEXT
- zip_code TEXT
- birth_day DATE

Products:
- product_id INTEGER PRIMARY KEY
- product_name TEXT
- description TEXT
- category TEXT
- price INTEGER
- stock_quantity INTEGER

Orders:
- order_id INTEGER PRIMARY KEY
- customer_id INTEGER
- order_date DATE
- total_amount INTEGER
- status TEXT
- FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)

Order_Items:
- order_item_id INTEGER PRIMARY KEY
- order_id INTEGER
- product_id INTEGER
- quantity INTEGER
- price REAL
- FOREIGN KEY (order_id) REFERENCES Orders (order_id)
- FOREIGN KEY (product_id) REFERENCES Product (product_id)

Reviews:
- review_id INTEGER PRIMARY KEY,
- product_id INTEGER,
- customer_id INTEGER,
- rating INTEGER,
- comment TEXT,
- review_date DATE,
- FOREIGN KEY (product_id) REFERENCES Product (product_id),
- FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)

</scheme>
"""