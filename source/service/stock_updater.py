import pymongo

public_health_care_client = pymongo.MongoClient('mongodb://localhost:27017/')['public-health-care']
stock_collection = public_health_care_client['stock']

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
    
def submit_delivery(concluded_delivery):
    if concluded_delivery['type'] == 'PATIENT':
        handle_patient_delivery(concluded_delivery['stock_destiny'], concluded_delivery['quantity'])
    elif concluded_delivery['type'] == 'REGION':
        handle_region_delivery(concluded_delivery['stock_base'], concluded_delivery['stock_destiny'], concluded_delivery['quantity'])

# mocked_region_delivery = {
#     'id': '93f526bb-e17d-46b1-b274-11126039cf76',
#     'type': 'REGION',
#     'patient_cpf': None,
#     'prescription_id': None,
#     'region_origin': 'Centro',
#     'region_destiny': 'Jardim',
#     'stock_base': '464fa38d-bf5e-46e4-9fe8-bc6161949760',
#     'stock_destiny': 'def069a4-d568-4b40-ac8b-4747c4e3af17',
#     'quantity': 7
# }

# mocked_patient_delivery = {
#     'id': '93f526bb-e17d-46b1-b274-11126039cf76',
#     'type': 'PATIENT',
#     'patient_cpf': '22937029902',
#     'region_origin': None,
#     'region_destiny': 'oratorio',
#     'stock_base': None,
#     'stock_destiny': '464fa38d-bf5e-46e4-9fe8-bc6161949760',
#     'quantity': 10
# }

# submit_delivery(mocked_region_delivery)
# submit_delivery(mocked_patient_delivery)
