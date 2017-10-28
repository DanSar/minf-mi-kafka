import argparse
from confluent_kafka import Consumer

parser = argparse.ArgumentParser()
parser.add_argument('--topic', '-t', required=True,
                    help='kafka topic and twitter search keyword')
parser.add_argument('--filename', '-f', required=True,
                    help='Name of chart file')
parser.add_argument('--kafka', '-k',
                    help='Kafka server url', default='localhost:9092')
args = parser.parse_args()

# connect to Kafka
print('Connecting to kafka cluster..')
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
conf = {'bootstrap.servers': args.kafka, 'group.id': 'mygroup',
        'default.topic.config': {'auto.offset.reset': 'smallest'}}
c = Consumer(**conf)
print('Done..\nSubsribing to {}..'.format(args.topic))
c.subscribe([args.topic])
running = True
print('Start polling..\nStop with ctrl-c..')
while running:
    msg = c.poll()
    try:
        if not msg.error():
            with open(args.filename, 'wb') as f:
                f.write(msg.value())
        else:
            pass
    except KeyboardInterrupt:
        running = False
