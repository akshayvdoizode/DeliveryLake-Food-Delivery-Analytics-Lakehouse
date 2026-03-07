import pandas as pd
import random
from faker import Faker
from db import get_engine
import config

fake = Faker()

vehicle_types = ["Bike","Scooter","Car"]
cities = ["Bangalore","Delhi","Mumbai","Hyderabad","Chennai"]

def generate_drivers():

    drivers = []

    for i in range(config.NUM_DRIVERS):

        drivers.append({
            "driver_id": i+1,
            "driver_name": fake.name(),
            "city": random.choice(cities),
            "vehicle_type": random.choice(vehicle_types),
            "rating": round(random.uniform(3.5,5),1)
        })

    df = pd.DataFrame(drivers)

    engine = get_engine()
    df.to_sql("drivers",engine,if_exists="replace",index=False)

    print("drivers generated")