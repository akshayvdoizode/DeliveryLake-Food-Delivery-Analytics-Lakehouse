import pandas as pd
import random
from datetime import timedelta
from db import get_engine

PAYMENT_METHODS = [
    "UPI",
    "Card",
    "Wallet",
    "Cash"
]

PAYMENT_STATUS = [
    "paid",
    "failed",
    "refunded"
]

def generate_payments():

    engine = get_engine()

    # read completed orders
    orders = pd.read_sql(
        "SELECT order_id, order_time FROM orders WHERE order_status='completed'",
        engine
    )

    # read order value from order_items
    order_values = pd.read_sql("""
        SELECT
            order_id,
            SUM(unit_price * quantity) as order_amount
        FROM order_items
        GROUP BY order_id
    """, engine)

    order_values = order_values.set_index("order_id")

    rows = []
    payment_id = 1

    for order in orders.itertuples():

        amount = order_values.loc[order.order_id].order_amount

        status = random.choices(
            ["paid","failed"],
            weights=[96,4]
        )[0]

        rows.append({
            "payment_id": payment_id,
            "order_id": order.order_id,
            "payment_time": order.order_time + timedelta(minutes=random.randint(1,5)),
            "payment_method": random.choice(PAYMENT_METHODS),
            "payment_status": status,
            "payment_amount": amount
        })

        payment_id += 1

    df = pd.DataFrame(rows)

    df.to_sql("payments", engine, if_exists="replace", index=False)

    print("payments generated")