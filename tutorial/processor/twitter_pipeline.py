import time
from winton_kafka_streams.processor import TopologyBuilder
import winton_kafka_streams.kafka_config as kafka_config
import winton_kafka_streams.kafka_streams as kafka_streams

from twitter_emoji_processor import EmojiParserProcessor
from emoji_chart_processor import EmojiChartProcessor


def run(src_topic, target_topic, kafka_url):
    kafka_config.BOOTSTRAP_SERVERS = kafka_url
    kafka_config.AUTO_OFFSET_RESET = 'earliest'

    twitter_emoji_topic = src_topic + '-emoji'

    with TopologyBuilder() as topology_builder1:
        topology_builder1. \
            source('tweets', [src_topic]). \
            processor('emoji', EmojiParserProcessor, 'tweets'). \
            sink('emojis', twitter_emoji_topic, 'emoji')

    with TopologyBuilder() as topology_builder2:
        topology_builder2. \
            source('emoji', [twitter_emoji_topic]). \
            processor('chart', EmojiChartProcessor, 'emoji'). \
            sink('chart_file', target_topic, 'chart')

    wks1 = kafka_streams.KafkaStreams(topology_builder1, kafka_config)
    wks2 = kafka_streams.KafkaStreams(topology_builder2, kafka_config)
    wks1.start()
    wks2.start()
    print('Start streaming..\nStop with ctrl-c..')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        wks1.close()
        wks2.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Converts tweets to emojis")
    parser.add_argument('--src_topic', '-st', required=True,
                        help="kafka topic to connect to")
    parser.add_argument('--target_topic', '-tt', required=True,
                        help="kafka topic to connect to")
    parser.add_argument('--kafka', '-k', help='Kafka server url',
                        default='localhost:9092')
    args = parser.parse_args()
    run(args.src_topic, args.target_topic, args.kafka)
