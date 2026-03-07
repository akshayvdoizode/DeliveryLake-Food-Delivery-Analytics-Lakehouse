import pandas as pd
import random
from datetime import datetime,timedelta
from db import get_engine
import config

def generate_orders():

    orders = []

    base = datetime(2023,1,1)

    for i in range(config.NUM_ORDERS):

        time = base + timedelta(minutes=random.randint(0,600000))

        status = random.choices(
            ["completed","cancelled"],
            weights=[92,8]
        )[0]

        orders.append({
            "order_id": i+1,
            "customer_id": random.randint(1,config.NUM_CUSTOMERS),
            "restaurant_id": random.randint(1,config.NUM_RESTAURANTS),
            "order_time": time,
            "order_status": status
        })

    df = pd.DataFrame(orders)

    engine = get_engine()
    df.to_sql("orders",engine,if_exists="replace",index=False)

    print("orders generated")