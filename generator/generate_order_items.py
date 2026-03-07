import pandas as pd
import random
from db import get_engine

menu_items = [
"Burger","Pizza","Pasta","Biryani",
"Noodles","Fries","Coffee","Sandwich"
]

def generate_order_items():

    engine = get_engine()

    orders = pd.read_sql("SELECT order_id FROM orders",engine)

    rows = []
    item_id = 1

    for order in orders.itertuples():

        items = random.randint(1,4)

        for _ in range(items):

            rows.append({
                "order_item_id": item_id,
                "order_id": order.order_id,
                "item_name": random.choice(menu_items),
                "quantity": random.randint(1,3),
                "item_price": random.randint(100,600)
            })

            item_id += 1

    df = pd.DataFrame(rows)

    df.to_sql("order_items",engine,if_exists="replace",index=False)

    print("order_items generated")