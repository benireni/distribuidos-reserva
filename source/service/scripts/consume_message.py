from kafka import KafkaConsumer

consumer = KafkaConsumer('medication-request', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='main-group')

def consume_messages():
    return [message.value for message in consumer]
