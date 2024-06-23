import pymongo

public_health_care_client = pymongo.MongoClient('mongodb://localhost:27017/')['public-health-care']
stock_collection = public_health_care_client['stock']
delivery_collection = public_health_care_client['delivery']

def get_stock_quantity_by_id(stock_id):
    return stock_collection.find_one({'id': stock_id}, {})['quantity']

def update_stock_quantity_by_id(stock_id, new_quantity):
    stock_collection.update_one({'id': stock_id}, {'$set': {'quantity': new_quantity}})

def handle_sus_supply(stock_id, quantity):
    current_quantity = get_stock_quantity_by_id(stock_id)
    update_stock_quantity_by_id(stock_id, current_quantity + quantity)

def handle_patient_delivery(stock_id, quantity):
    current_quantity = get_stock_quantity_by_id(stock_id)
    update_stock_quantity_by_id(stock_id, current_quantity - quantity)
    
def handle_region_delivery(region_destiny_id, region_origin_id, quantity):
    destiny_quantity = get_stock_quantity_by_id(region_destiny_id)
    origin_quantity = get_stock_quantity_by_id(region_origin_id)
    update_stock_quantity_by_id(region_destiny_id, destiny_quantity + quantity)
    update_stock_quantity_by_id(region_origin_id, origin_quantity - quantity)
    
def submit_delivery(concluded_delivery_id):
    delivery = delivery_collection.find_one({'id': concluded_delivery_id}, {})
    print(delivery)
    if delivery['type'] == 'PATIENT':
        handle_patient_delivery(delivery['stock_base'], delivery['quantity'])
    elif delivery['type'] == 'REGION':
        handle_region_delivery(delivery['stock_base'], delivery['stock_destiny'], delivery['quantity'])
