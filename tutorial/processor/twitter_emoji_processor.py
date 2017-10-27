from winton_kafka_streams.processor import BaseProcessor
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
  