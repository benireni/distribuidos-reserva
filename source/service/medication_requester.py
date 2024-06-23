import pymongo
from kafka import KafkaProducer
import json

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)

def send_message(message):
    producer.send('medication-request', message)

public_health_care_client = pymongo.MongoClient("mongodb://localhost:27017/")["public-health-care"]

prescription_collection = public_health_care_client["prescription"]
patient_collection = public_health_care_client["patient"]

def get_prescription_by_id(prescription_id):
    return prescription_collection.find_one({'id': prescription_id}, {})

def get_patient_region_by_cpf(patient_cpf):
    return patient_collection.find_one({'cpf': patient_cpf}, {})['region']

def submit_medication_request(prescription_id):
    prescription = get_prescription_by_id(prescription_id)
    if not prescription['valid']:
        return 'Receita inválida.'

    region = get_patient_region_by_cpf(prescription['patient_cpf'])

    request = {
        'prescription_id': prescription['id'],
        'patient_cpf': prescription['patient_cpf'],
        'register_medication': prescription['register_medication'],
        'quantity': prescription['quantity'],
        'region': region
    }

    send_message(request)
    return request
