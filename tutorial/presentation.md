# Kafka
Libs:
- https://github.com/dpkp/kafka-python
- https://github.com/wintoncode/winton-kafka-streams

## Example
Using screen cast and python.

1. simple setup
2. twitter analysis (Emoji-Stream)
  - Producers:
    - Twitter API
    - 1 Hashtag -> 1 Topic
      - https://www.trendsmap.com
    - Example implementation: https://github.com/seandolinar/socialmediaparse
    - Emojis: https://unpkg.com/emoji.json@5.0.0/emoji.json
  - Stream API:
    - parse Tweet and extract emoji -> push every emoji to topic.
    - create graph periodically (every 5s): https://plot.ly/python/
  - Consumers:
    - trending events: https://twitter.com/OfficialSanta/status/923455168435417088
    - show graph periodically

## Topics
TWITTER -producer-> TWEETs -stream-> EMOJIs -stream-> PLOTs


## Screencast

```bash
zookeeper-server-start.sh /usr/local/kafka_2.11-0.11.0.1/config/zookeeper.properties
kafka-server-start.sh /usr/local/kafka_2.11-0.11.0.1/config/server.properties

python3 producers/twitter_producer.py --topic christmas-raw --search christmas
python3 processor/twitter_pipeline.py --src_topic christmas-raw --target_topic christmas-chart
python3 -m consumer/chart_consumer.py --topic christmas-chart --filename consumer/image-loader/chart.png

kafka-console-producer.sh --broker-list localhost:9092 --topic christmas-raw
kafka-console-producer.sh --broker-list localhost:9092 --topic christmas-chart

cd consumer/image-loader
python3 -m http.server
```