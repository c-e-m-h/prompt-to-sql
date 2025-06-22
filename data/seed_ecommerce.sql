-- customers.csv: id,name,state
-- orders.csv: id,customer_id,product_id,order_date,amount,status
-- Paste your e-commerce schema and INSERTs here 
-- data/seed_ecommerce.sql
-- CREATE EXTENSION IF NOT EXISTS pgvector;
-- pgvector extension is not required for this demo. Uncomment the above line if vector search is needed in the future.

CREATE TABLE customers (
    id          SERIAL PRIMARY KEY,
    name        TEXT,
    state       TEXT      -- e.g. 'CA'
);

CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        TEXT,
    category    TEXT,
    launch_date DATE
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id  INT REFERENCES products(id),
    order_date  DATE,
    amount      NUMERIC(10,2),
    status      TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    prompt_text TEXT NOT NULL,
    sql_text TEXT NOT NULL,
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (id,name,category,launch_date) VALUES
     (1,'Vintage Hoodie','Apparel','2024-01-01'),
     (2,'Bluetooth Earbuds','Electronics','2024-06-15'),
     (3,'EchoSmart Speaker','Electronics','2025-01-10');

\copy customers FROM '/data/customers.csv' WITH CSV;
\copy orders    FROM '/data/orders.csv'    WITH CSV;