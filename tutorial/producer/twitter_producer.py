import os
import twitter
import argparse
import configparser

from confluent_kafka import Producer

parser = argparse.ArgumentParser()
parser.add_argument('--topic', '-t', required=True,
                    help='kafka topic')
parser.add_argument('--search', '-s', required=True,
                    help='hashtag or search keyword for twitter')
parser.add_argument('--kafka', '-k', help='Kafka server url',
                    default='localhost:9092')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('{}/config.cnf'.format(
    os.path.dirname(os.path.abspath(__file__))))


def connect_to_twitter(config):
    return twitter.Api(
        consumer_key=config.get('twitter', 'consumer_key'),
        consumer_secret=config.get('twitter', 'consumer_secret'),
        access_token_key=config.get('twitter', 'access_token'),
        access_token_secret=config.get('twitter', 'access_token_secret'))


def line_to_text(line):
    # Signal that the line represents a tweet
    if 'in_reply_to_status_id' in line:
        tweet = twitter.Status.NewFromJsonDict(line)
        return tweet.text
    return ""


# connect to Kafka
print('Connecting to kafka cluster...')
# Producer configuration
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
conf = {'bootstrap.servers': args.kafka}

# Create Producer instance
p = Producer(**conf)

# connect to twitter
print('Connecting to twitter API...')
api = connect_to_twitter(config)
print('Done\nStart fetching from {}\nStop with ctrl-c..'.format(args.search))
stream = api.GetStreamFilter(track=[args.search])
for line in stream:
    tweet = line_to_text(line)
    # print("sending " + tweet)
    p.produce(args.topic, bytes(tweet, 'utf-8'))
