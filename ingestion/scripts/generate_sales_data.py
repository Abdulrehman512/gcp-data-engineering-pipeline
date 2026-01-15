import csv
import random
import uuid
from datetime import datetime, timedelta

# ==============================
# CONFIG
# ==============================
OUTPUT_FILE = "data_samples/raw/sales_transactions.csv"
TOTAL_ROWS = 10_000_000        # change to 5_000_000 if needed
CHUNK_SIZE = 100_000

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

CURRENCIES = ["USD", "EUR", "GBP", "CAD", "PKR"]
PAYMENT_METHODS = ["card", "cash", "paypal", "apple_pay"]
PRODUCT_CATEGORIES = ["electronics", "clothing", "grocery", "furniture", "books"]
COUNTRIES = ["US", "CA", "UK", "PK"]

# ==============================
# HELPERS
# ==============================
def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_row():
    quantity = random.randint(1, 5)
    unit_price = round(random.uniform(5, 500), 2)
    gross_amount = round(quantity * unit_price, 2)
    discount = round(random.uniform(0, gross_amount * 0.2), 2)
    net_amount = round(gross_amount - discount, 2)

    return [
        str(uuid.uuid4()),
        random_date(START_DATE, END_DATE).isoformat(),
        f"CUST-{random.randint(10000, 999999)}",
        f"PROD-{random.randint(1000, 9999)}",
        random.choice(PRODUCT_CATEGORIES),
        quantity,
        unit_price,
        gross_amount,
        discount,
        net_amount,
        random.choice(CURRENCIES),
        random.choice(PAYMENT_METHODS),
        f"STORE-{random.randint(1, 500)}",
        random.choice(COUNTRIES),
        datetime.utcnow().isoformat()
    ]

# ==============================
# MAIN
# ==============================
def main():
    header = [
        "transaction_id",
        "transaction_timestamp",
        "customer_id",
        "product_id",
        "product_category",
        "quantity",
        "unit_price",
        "gross_amount",
        "discount_amount",
        "net_amount",
        "currency_code",
        "payment_method",
        "store_id",
        "country",
        "created_at"
    ]

    with open(OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        rows_written = 0
        while rows_written < TOTAL_ROWS:
            chunk = []
            for _ in range(min(CHUNK_SIZE, TOTAL_ROWS - rows_written)):
                chunk.append(generate_row())

            writer.writerows(chunk)
            rows_written += len(chunk)

            print(f"Rows written: {rows_written:,}")

    print("✅ Data generation complete")

if __name__ == "__main__":
    main()
