from generate_customers import generate_customers
from generate_restaurants import generate_restaurants
from generate_drivers import generate_drivers
from generate_orders import generate_orders
from generate_order_items import generate_order_items

def main():

    generate_customers()
    generate_restaurants()
    generate_drivers()
    generate_orders()
    generate_order_items()

if __name__ == "__main__":
    main()