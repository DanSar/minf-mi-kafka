#!/bin/bash

chart_path="chart.png"
if [[ $1 ]]; then
	x-terminal-emulator -e python producer/twitter_producer.py -t twitter -s 'trump' 
	x-terminal-emulator -e python processor/twitter_pipeline.py -st twitter -tt emoji-chart
	x-terminal-emulator -e python consumer/chart_consumer.py -t emoji-chart -f ${1}${chart_path}
else
	echo "$BASH_SOURCE <relative-path-to-consumer-image-loader>"
	echo "i.g.: $BASH_SOURCE consumer/image-loader/"	
fi	
