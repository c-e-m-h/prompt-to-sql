import csv
import random
import datetime
import os
from faker import Faker

# Column names (for README and reference)
# customers.csv: id,name,state
# orders.csv: id,customer_id,product_id,order_date,amount,status

data_dir = os.path.join(os.path.dirname(__file__), '../data')
fake = Faker()
states = ["CA", "NY", "TX", "FL", "WA"]
products = [1, 2, 3]

num_customers = 300
num_orders = 600

# Generate customers
customers = []
for i in range(1, num_customers + 1):
    name = fake.name()
    state = random.choice(states)
    customers.append([i, name, state])

# Generate orders
orders = []
for i in range(1, num_orders + 1):
    customer_id = random.randint(1, num_customers)
    product_id = random.choice(products)
    # Order date between 2024-07-01 and 2025-05-31
    order_date = fake.date_between(
        datetime.date(2024, 7, 1),
        datetime.date(2025, 5, 31)
    )
    amount = round(random.uniform(50, 300), 2)
    status = "paid"
    orders.append([i, customer_id, product_id, order_date, amount, status])

# Write customers.csv (no header)
with open(os.path.join(data_dir, 'customers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(customers)

# Write orders.csv (no header)
with open(os.path.join(data_dir, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(orders)

print('Generated customers.csv and orders.csv (no headers).') 