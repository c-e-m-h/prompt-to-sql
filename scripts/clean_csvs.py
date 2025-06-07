import csv
import os

def clean_customers(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as infile, open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['id', 'name', 'email', 'state']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(reader, start=1):
            writer.writerow({
                'id': idx,
                'name': row['name'],
                'email': row['email'],
                'state': row['state']
            })

def clean_orders(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as infile, open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['id', 'customer_id', 'product_id', 'order_date', 'amount', 'status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(reader, start=1):
            try:
                writer.writerow({
                    'id': idx,
                    'customer_id': int(row['customer_id']),
                    'product_id': int(row['product_id']),
                    'order_date': row['order_date'],
                    'amount': row['amount'],
                    'status': row['status']
                })
            except Exception as e:
                print(f"Skipping row {idx} in orders.csv due to error: {e}")

data_dir = os.path.join(os.path.dirname(__file__), '../data')

clean_customers(
    os.path.join(data_dir, 'customers.csv'),
    os.path.join(data_dir, 'customers.csv')
)

clean_orders(
    os.path.join(data_dir, 'orders.csv'),
    os.path.join(data_dir, 'orders.csv')
)
print('CSV cleaning complete.') 