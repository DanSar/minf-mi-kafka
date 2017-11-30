# Kafka config 
kafka_config.BOOTSTRAP_SERVERS = kafka_url
kafka_config.AUTO_OFFSET_RESET = 'earliest'

emoji_topic = src_topic + '-emoji'
target_topic = src_topic + '-chart'

with TopologyBuilder() as topology_builder1:
    topology_builder1. \
        source('tweets', [src_topic]). \
        processor('emoji', EmojiParserProcessor, 'tweets'). \
        sink('emojis', emoji_topic, 'emoji')

with TopologyBuilder() as topology_builder2:
    topology_builder2. \
        source('emoji', [emoji_topic]). \
        processor('chart', EmojiChartProcessor, 'emoji'). \
        sink('chart_file', target_topic, 'chart')

kafka_streams.KafkaStreams(topology_builder1, kafka_config).start()
kafka_streams.KafkaStreams(topology_builder2, kafka_config).start()

# close on termination
