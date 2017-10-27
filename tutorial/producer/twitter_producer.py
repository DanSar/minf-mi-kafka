import twitter
import argparse
from emoji import UNICODE_EMOJI
from kafka import SimpleProducer, KafkaClient # TODO: use other lib

parser = argparse.ArgumentParser()
parser.add_argument('--topic', '-t', help='kafka topic and twitter search keyword')
parser.add_argument('--consumer-key', '-ck', help='Twitter consumer key')
parser.add_argument('--consumer-secret', '-cs', help='Twitter consumer secret')
parser.add_argument('--access-token-key', '-ak', help='Twitter access token key')
parser.add_argument('--access-token-secret', '-as', help='Twitter access token secret')
args = parser.parse_args()


def connect_to_twitter(args):
    return twitter.Api(
        consumer_key=args.consumer_key,
        consumer_secret=args.consumer_secret,
        access_token_key=args.access_token_key,
        access_token_secret=args.access_token_secret)

def extract_emoji(text): 
    return [c for c in text if c in UNICODE_EMOJI]

def line_to_text(line):
    # Signal that the line represents a tweet
    if 'in_reply_to_status_id' in line:
        tweet = twitter.Status.NewFromJsonDict(line)
        return tweet.text
    
    return ""

# connect to Kafka
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)


# connect to twitter
print('Connecting to twitter API')
api = connect_to_twitter(args)

stream = api.GetStreamFilter(track=[args.topic])
for line in stream:
    for emoji in extract_emoji(line_to_text(line)):
        producer.send_messages(args.topic, bytes(emoji, 'utf-8'))
