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
