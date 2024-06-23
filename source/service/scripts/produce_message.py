from kafka import KafkaProducer
import json

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)

def send_message(message):
    producer.send('medication-request', message)