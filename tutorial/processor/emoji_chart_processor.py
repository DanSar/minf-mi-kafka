import matplotlib.pyplot as plt
import matplotlib.font_manager as font_mng
import pandas as pd

from io import BytesIO

from winton_kafka_streams.processor import BaseProcessor


class EmojiChartProcessor(BaseProcessor):

    def initialise(self, _name, _context):
        super().initialise(_name, _context)
        # output updated counts every 10 seconds
        self.context.schedule(10.)
        self.emojis = {}

    def process(self, key, value):
        self._create_bar_chart(value)

    def punctuate(self, timestamp):
        pass

    def _create_bar_chart(self, emoji):
        self.emojis.setdefault(emoji, 0)
        self.emojis[emoji] += 1
        # sort emojis and return the most favored
        emojis_sorted = sorted(self.emojis.items(),
                               key=lambda e: e[1],
                               reverse=True)[:10]
        # append empty char for beautiful emoji plotting :)
        emoji_list = ['{} '.format(k[0].decode('utf-8'))
                      for k in emojis_sorted]
        count_list = [v[1] for v in emojis_sorted]
        data = {'emoji_counts': pd.Series(count_list, index=emoji_list)}
        df = pd.DataFrame(data)
        fig, axis = plt.subplots()

        font_mng._rebuild()

        # set font of x-axis
        for label in (axis.get_xticklabels()):
            label.set_fontname('EmojiOne Color')
            label.set_fontsize(10)
        axis.set_xlabel('emoji')
        axis.set_ylabel('total counts')
        df['emoji_counts'].plot(
            kind='bar',
            ax=axis,
            title='10th most favored emojis :)\n'
            '{} emojis totally counted'.format(len(self.emojis)),
            legend=True)
        buf = BytesIO()
        plt.xticks(rotation=0)
        plt.savefig(buf, dpi=300, format='png')
        self.context.forward('chart', buf.getvalue())
        buf.close()
        plt.close()
