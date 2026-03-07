import pandas as pd
import random
from datetime import timedelta
from db import get_engine

def generate_refunds():

    engine = get_engine()

    orders = pd.read_sql(
        "SELECT order_id, order_time FROM orders WHERE order_status='completed'",
        engine
    )

    refund_orders = orders.sample(frac=0.04)

    rows = []

    refund_id = 1

    for order in refund_orders.itertuples():

        rows.append({
            "refund_id": refund_id,
            "order_id": order.order_id,
            "refund_time": order.order_time + timedelta(hours=random.randint(1,48)),
            "refund_amount": random.randint(50,300),
            "refund_reason": random.choice([
                "late_delivery",
                "wrong_item",
                "food_quality"
            ])
        })

        refund_id += 1

    df = pd.DataFrame(rows)

    df.to_sql("refunds", engine, if_exists="replace", index=False)

    print("refunds generated")