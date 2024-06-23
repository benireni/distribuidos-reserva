import pymongo, uuid, json
from kafka import KafkaConsumer

def json_deserializer(v):
    if v is None:
        return None
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        print('Unable to decode: %s', v)
        return None

consumer = KafkaConsumer('medication-request',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='main-group',
                         value_deserializer=json_deserializer)

public_health_care_client = pymongo.MongoClient("mongodb://localhost:27017/")["public-health-care"]

stock_collection = public_health_care_client["stock"]
prescription_collection = public_health_care_client["prescription"]
delivery_collection = public_health_care_client["delivery"]

def get_stock_by_region_and_medication(region, medication_register):
    return stock_collection.find_one({'region': region, 'medication_register': medication_register}, {})

def get_stock_by_medication(medication_register, target_region):
    return stock_collection.find_one({'$and': [{'region': {'$ne': target_region}}, {'medication_register': medication_register}]}, {})

def discard_prescription(prescription_id):
    prescription_collection.update_one({'id': prescription_id}, {'$set': {'valid': False}})

def place_delivery_patient(region, patient_cpf, base_stock_id, prescription_id, quantity):
    delivery_id = str(uuid.uuid4())
    delivery = {
        'id': delivery_id,
        'type': "PATIENT",
        'patient_cpf': patient_cpf,
        'prescription_id': prescription_id,
        'region_origin': None,
        'region_destiny': region,
        'stock_base': base_stock_id,
        'stock_destiny': None,
        'quantity': quantity
    }
    delivery_collection.insert_one(delivery)
    return delivery_id

def place_delivery_region(region_destiny, region_origin, base_stock_id, destiny_stock_id, quantity):
    delivery_id = str(uuid.uuid4())
    delivery = {
        'id': delivery_id,
        'type': "REGION",
        'patient_cpf': None,
        'prescription_id': None,
        'region_origin': region_origin,
        'region_destiny': region_destiny,
        'stock_base': base_stock_id,
        'stock_destiny': destiny_stock_id,
        'quantity': quantity
    }
    delivery_collection.insert_one(delivery)
    return delivery_id

def handle_medication_request(medication_request):
    region_patient = medication_request['region']
    medication_register = medication_request['medication_register']

    stock = get_stock_by_region_and_medication(region_patient, medication_register)

    available_quantity = stock['quantity']
    needed_quantity = medication_request['quantity']
    if stock:
        if available_quantity >= needed_quantity:
            discard_prescription(medication_request['prescription_id'])
            delivery_id = place_delivery_patient(medication_request['region'], medication_request['patient_cpf'], stock['id'], medication_request['prescription_id'], medication_request['quantity'])
            return 'Entrega separada! ID: {}'.format(delivery_id)
        
    available_region = get_stock_by_medication(medication_register, region_patient)
    if available_region:
        delivery_id = place_delivery_region(medication_request['region'], available_region['region'], stock['id'], available_region['id'], medication_request['quantity'])
        discard_prescription(medication_request['prescription_id'])
        return 'Remedio indisponível, tente novamente mais tarde. Transferência agendada: ID {}'.format(delivery_id)
    else:
        return 'Remedio contido na receita não é oferecido ou não existe na quantidade adequada.'

mocked_prescription = {
    'id': '982c38fe-2250-4c7c-926a-fa08f9970907',
    'crm': 123,
    'doctor_name': 'medicao',
    'patient_cpf': '51410642549',
    'quantity': 90,
    'medication_register': 'dff8e6f3-f485-43de-9d66-be8d356446ef',
    'description': "prescription daorinha pra ficar legau",
    'valid': True
}

mocked_region = 'Centrinho'


print('Hearing medication requests...')
for message in consumer:
    response = handle_medication_request(message.value)
    print('handled: {}'.format(message))
    print(response)
