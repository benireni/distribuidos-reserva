from flask import Flask, make_response, request
from bson import json_util
from uuid import uuid4
import json, pymongo

from service import medication_requester, stock_updater

app = Flask(__name__)

@app.route('/')
def hello():
  return make_response('Vambora grupo', 200)

public_health_care_client = pymongo.MongoClient("mongodb://localhost:27017/")["public-health-care"]

stock_collection = public_health_care_client["stock"]
patient_collection = public_health_care_client["patient"]
prescription_collection = public_health_care_client["prescription"]
medication_collection = public_health_care_client["medication"]
delivery_collection = public_health_care_client["delivery"]

def send_result(data, status_code):
  return make_response(json.dumps(list(data), default=json_util.default), status_code)

## Médico

@app.route('/prescription/', methods=['POST'])
def post_prescription():
  req_payload = request.get_json()

  new_prescription_id = str(uuid4())
  new_prescription = {
    'id': new_prescription_id,
    'crm': req_payload['crm'],
    'name_doctor': req_payload['name_doctor'],
    'patient_cpf': req_payload['patient_cpf'],
    'description': req_payload['description']
  }

  prescription_collection.insert_one(new_prescription)
  return make_response(new_prescription_id, 201)

## Farmacêutico

@app.route('/prescription/<prescription_id>', methods=['GET'])
def get_prescription(prescription_id):
  prescription = prescription_collection.find({'id': prescription_id}, {})
  return send_result(prescription, 200)  

@app.route('/prescription/<prescription_id>/discard', methods=['POST'])
def discard_prescription(prescription_id):
  prescription_collection.update_one({'id': prescription_id}, {'$set': {'valid': False}})
  return send_result('Successfully updated', 200)

@app.route('/stock/', methods=['POST'])
def create_stock():
  req_payload = request.get_json()

  new_stock_id = str(uuid4())
  new_stock = {
    'id': new_stock_id,
    'type': req_payload['type'],
    'patient_cpf': req_payload['patient_cpf'],
    'prescription_id': req_payload['prescription_id'],
    'region_origin': req_payload['region_origin'],
    'region_destiny': req_payload['region_destiny'],
    'stock_base': req_payload['stock_base'],
    'stock_destiny': req_payload['stock_destiny'],
    'quantity': req_payload['quantity']
  }

  stock_collection.insert_one(new_stock)
  return make_response(new_stock_id, 201)

## Paciente

@app.route('/request/<prescription_id>', methods=['POST'])
def create_medication_request(prescription_id):
  response = medication_requester.submit_medication_request(prescription_id)
  return make_response(response, 200)

## SUS

@app.route('/stock/<stock_id>/supply', methods=['POST'])
def add_to_stock(stock_id):
  supplied_quantity = request.get_json()['quantity']
  stock_updater.handle_sus_supply(stock_id, supplied_quantity)
  return make_response('Remédios recebidos!', 200)

if __name__ == '__main__':
  app.run(port=8080)