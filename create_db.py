import sqlite3

# SQLite 데이터베이스 연결 (또는 생성)
conn = sqlite3.connect('sample.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    zip_code TEXT,
    birth_day DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    description TEXT,
    category TEXT,
    price INTEGER,
    stock_quantity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount INTEGER,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    FOREIGN KEY (product_id) REFERENCES Product (product_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    rating INTEGER,
    comment TEXT,
    review_date DATE,
    FOREIGN KEY (product_id) REFERENCES Product (product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
)
''')

# 샘플 데이터 삽입
# Customers
cursor.execute("INSERT INTO Customers (first_name, last_name, email, phone, address, city, zip_code, birth_day) VALUES "
               "('John', 'Doe', 'john@example.com', '1234567890', '123 Elm St', 'Some City', '12345', '1980-01-01')")
cursor.execute("INSERT INTO Customers (first_name, last_name, email, phone, address, city, zip_code, birth_day) VALUES "
               "('Jane', 'Smith', 'jane@example.com', '0987654321', '456 Oak St', 'Any City', '67890', '1990-02-02')")
cursor.execute("INSERT INTO Customers (first_name, last_name, email, phone, address, city, zip_code, birth_day) VALUES "
               "('Alice', 'Sue', 'alice@example.com', '1112223333', '789 Pine St', 'New City', '54321', '1985-03-03')")
cursor.execute("INSERT INTO Customers (first_name, last_name, email, phone, address, city, zip_code, birth_day) VALUES "
               "('Bob', 'Brown', 'bob@example.com', '4445556666', '101 Maple St', 'Old City', '98765', '1975-04-04')")

# Product
cursor.execute("INSERT INTO Products (product_name, description, category, price, stock_quantity) VALUES "
               "('Widget', 'A useful widget', 'Gadgets', 19, 100)")
cursor.execute("INSERT INTO Products (product_name, description, category, price, stock_quantity) VALUES "
               "('Gadget', 'A fancy gadget', 'Gadgets', 29, 50)")
cursor.execute("INSERT INTO Products (product_name, description, category, price, stock_quantity) VALUES "
               "('Doodad', 'A handy doodad', 'Gadgets', 9, 150)")
cursor.execute("INSERT INTO Products (product_name, description, category, price, stock_quantity) VALUES "
               "('Thingamajig', 'An amazing thingamajig', 'Gadgets', 39, 200)")

# Orders
cursor.execute("INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES "
               "(1, '2023-01-01', 19, 'Shipped')")
cursor.execute("INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES "
               "(2, '2023-02-01', 29, 'Processing')")
cursor.execute("INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES "
               "(3, '2023-03-01', 39, 'Delivered')")
cursor.execute("INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES "
               "(4, '2023-04-01', 9, 'Pending')")

# Order_Items
cursor.execute("INSERT INTO Order_Items (order_id, product_id, quantity, price) VALUES "
               "(1, 1, 1, 19)")
cursor.execute("INSERT INTO Order_Items (order_id, product_id, quantity, price) VALUES "
               "(2, 2, 1, 29)")
cursor.execute("INSERT INTO Order_Items (order_id, product_id, quantity, price) VALUES "
               "(3, 3, 1, 39)")
cursor.execute("INSERT INTO Order_Items (order_id, product_id, quantity, price) VALUES "
               "(4, 4, 1, 9)")

# Reviews
cursor.execute("INSERT INTO Reviews (product_id, customer_id, rating, comment, review_date) VALUES "
               "(1, 1, 5, 'Great product!', '2023-01-02')")
cursor.execute("INSERT INTO Reviews (product_id, customer_id, rating, comment, review_date) VALUES "
               "(2, 2, 4, 'Very useful!', '2023-02-03')")
cursor.execute("INSERT INTO Reviews (product_id, customer_id, rating, comment, review_date) VALUES "
               "(3, 3, 3, 'Not bad.', '2023-03-02')")
cursor.execute("INSERT INTO Reviews (product_id, customer_id, rating, comment, review_date) VALUES "
               "(4, 4, 2, 'Could be better.', '2023-04-03')")

conn.commit()
conn.close()
