import time
from winton_kafka_streams.processor import BaseProcessor, TopologyBuilder
import winton_kafka_streams.kafka_config as kafka_config
import winton_kafka_streams.kafka_streams as kafka_streams
from emoji import UNICODE_EMOJI

class EmojiParserProcessor(BaseProcessor):

  def initialise(self, _name, _context):
    super().initialise(_name, _context)
    # output updated counts every second
    self.context.schedule(1.)
    self.emojis = []

  def process(self, key, value):
    self.emojis.extend(self.extract_emojis(value.decode("utf-8")))
    
  def punctuate(self, timestamp):
    for emoji in self.emojis:
      self.context.forward("emoji", emoji)
    self.emojis = []

  def extract_emojis(self, text): 
    return [c for c in text if c in UNICODE_EMOJI]


def run(src_topic, kafka_url):
  kafka_config.BOOTSTRAP_SERVERS = kafka_url
  kafka_config.AUTO_OFFSET_RESET = 'earliest'

  with TopologyBuilder() as topology_builder:
    topology_builder. \
      source('tweets', [src_topic]). \
      processor('emoji', EmojiParserProcessor, 'tweets'). \
      sink('emojis', src_topic + '-emoji', 'emoji')

  wks = kafka_streams.KafkaStreams(topology_builder, kafka_config)
  wks.start()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    pass
  finally:
    wks.close()


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description="Converts tweets to emojis")
  parser.add_argument('--topic', '-t', help="kafka topic to connect to")
  parser.add_argument('--kafka', '-k', help='Kafka server url', default='localhost:9092')
  args = parser.parse_args()

  run(args.topic, args.kafka)