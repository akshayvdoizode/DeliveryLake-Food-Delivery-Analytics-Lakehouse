import pandas as pd
from datetime import timedelta
from db import get_engine
import config

def generate_delivery_events():

    engine = get_engine()

    orders = pd.read_sql(
        "SELECT order_id, order_time FROM orders WHERE order_status='completed'",
        engine
    )

    rows = []
    event_id = 1

    for order in orders.itertuples():

        base = order.order_time

        events = [
            ("order_created", base),
            ("restaurant_accepted", base + timedelta(minutes=3)),
            ("driver_assigned", base + timedelta(minutes=8)),
            ("picked_up", base + timedelta(minutes=20)),
            ("delivered", base + timedelta(minutes=40))
        ]

        for e in events:

            rows.append({
                "event_id": event_id,
                "order_id": order.order_id,
                "event_type": e[0],
                "event_time": e[1]
            })

            event_id += 1

    df = pd.DataFrame(rows)

    df.to_sql("delivery_events", engine, if_exists="replace", index=False)

    print("delivery events generated")