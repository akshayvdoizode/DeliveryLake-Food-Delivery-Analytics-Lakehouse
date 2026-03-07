from generate_customers import generate_customers
from generate_restaurants import generate_restaurants
from generate_drivers import generate_drivers
from generate_orders import generate_orders
from generate_order_items import generate_order_items
from generate_delivery import generate_delivery_events
from generate_refunds import generate_refunds
from generate_payments import generate_payments

def main():

    generate_customers()
    generate_restaurants()
    generate_drivers()
    generate_orders()
    generate_order_items()
    generate_delivery_events()
    generate_payments()
    generate_refunds()  
if __name__ == "__main__":
    main()