import pandas as pd
import random
import numpy as np
from faker import Faker
from db import get_engine
import config

fake = Faker()

cities = ["Bangalore","Delhi","Mumbai","Hyderabad","Chennai"]
cuisines = [
"Indian","Chinese","Italian","Cafe","Fast Food",
"Biryani","South Indian","North Indian"
]

def generate_restaurants():

    restaurants = []

    for i in range(config.NUM_RESTAURANTS):

        popularity = np.random.pareto(2) + 1

        restaurants.append({
            "restaurant_id": i+1,
            "restaurant_name": fake.company(),
            "city": random.choice(cities),
            "cuisine": random.choice(cuisines),
            "rating": round(random.uniform(3,5),1),
            "popularity_score": popularity
        })

    df = pd.DataFrame(restaurants)

    engine = get_engine()
    df.to_sql("restaurants",engine,if_exists="replace",index=False)

    print("restaurants generated")