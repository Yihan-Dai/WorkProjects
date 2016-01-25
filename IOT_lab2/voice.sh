#!/bin/sh
arecord -D plughw:0,0 -q -f cd -t wav -d 4 -r 16000 | flac - -f --best --sample-rate 16000 -s -o voice.flac;

exit 0

