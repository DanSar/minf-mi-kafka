import time
from kafka import SimpleProducer, KafkaClient

# connect to Kafka
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)

topic = 'twitter'

print('Connecting to twitter API')

# test
for i in range(100):
    producer.send_messages(topic, bytes(str(i * i), 'utf-8'))
    time.sleep(0.2)

print('finished...')
