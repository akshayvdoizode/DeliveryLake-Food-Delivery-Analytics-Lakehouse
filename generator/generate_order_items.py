import pandas as pd
import random
from db import get_engine

MENU_ITEMS = [
    "Burger",
    "Pizza",
    "Pasta",
    "Biryani",
    "Noodles",
    "Fries",
    "Coffee"
]

def generate_order_items():

    engine = get_engine()

    orders = pd.read_sql("SELECT order_id FROM orders", engine)

    rows = []
    item_id = 1

    for order in orders.itertuples():

        item_count = random.randint(1,4)

        for _ in range(item_count):

            rows.append({
                "order_item_id": item_id,
                "order_id": order.order_id,
                "menu_item": random.choice(MENU_ITEMS),
                "quantity": random.randint(1,3),
                "unit_price": random.randint(120,600)
            })

            item_id += 1

    df = pd.DataFrame(rows)

    df.to_sql("order_items", engine, if_exists="replace", index=False)

    print("order_items generated")