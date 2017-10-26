# Kafka


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
    - parse Tweet and extract emoji -> push every emoji to (new) topic.
    - create graph periodically (every 5s): https://plot.ly/python/
  - Consumers:
    - get


## Topics
TWITTER -producer-> TWEETs -stream-> EMOJIs -stream-> PLOTs
