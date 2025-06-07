from faker import Faker
import random, datetime, csv, pathlib

fake = Faker()
states = ["CA", "NY", "TX", "FL", "WA"]
products = [
    (1, "Vintage Hoodie", "Apparel", "2024-01-01"),
    (2, "Bluetooth Earbuds", "Electronics", "2024-06-15"),
    (3, "EchoSmart Speaker", "Electronics", "2025-01-10")  # trending star
]

rows_customers, rows_orders = [], []
customer_id = 1
order_id = 1

for _ in range(300):
    state = random.choice(states)
    rows_customers.append((customer_id, fake.name(), fake.email(), state))

    # Each customer places 1–4 orders
    for _ in range(random.randint(1, 4)):
        prod = random.choices(products, weights=[1, 1, 3])[0]  # bias toward product 3
        # If prod 3, skew toward later months & CA
        if prod[0] == 3 and state == "CA":
            order_date = fake.date_between(
                datetime.date.fromisoformat("2025-02-01"),
                datetime.date.fromisoformat("2025-05-31")
            )
        else:
            order_date = fake.date_between(
                datetime.date.fromisoformat("2024-07-01"),
                datetime.date.fromisoformat("2025-05-31")
            )
        amount = round(random.uniform(50, 300), 2)
        rows_orders.append((order_id, customer_id, prod[0], order_date, amount, "paid"))
        order_id += 1
    customer_id += 1

# Write CSVs then psql can COPY them, or emit INSERT statements
pathlib.Path("data").mkdir(exist_ok=True)
with open("data/customers.csv", "w") as f:
    csv.writer(f).writerows(rows_customers)
with open("data/orders.csv", "w") as f:
    csv.writer(f).writerows(rows_orders) 