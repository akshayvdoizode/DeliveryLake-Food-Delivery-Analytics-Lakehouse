import pandas as pd
import random
from faker import Faker
from db import get_engine
import config

fake = Faker()

def generate_customers():

    rows = []

    for i in range(config.NUM_CUSTOMERS):

        rows.append({
            "customer_id": i + 1,
            "customer_name": fake.name(),
            "city": random.choice(config.CITIES),
            "signup_date": fake.date_between("-2y", "today")
        })

    df = pd.DataFrame(rows)

    engine = get_engine()
    df.to_sql("customers", engine, if_exists="replace", index=False)

    print("customers generated")