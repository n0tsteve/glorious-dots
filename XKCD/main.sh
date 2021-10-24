#!/usr/bin/env bash

# Background color
BG="#0E121A"
# Foreground color
FG="#ABB2BF"

# A place to store the downloaded the comic
COMIC_LOC="$HOME/comic.png"
# A place to store the recolored version of the comic
COMIC_RECOL="$HOME/recolor.png"
# The base image
BG_DEF="$HOME/default.png"
# The output image
OUT="$HOME/output.png"

# Get current comic number
COMIC_URL="$(curl -s 'https://xkcd.com/info.0.json' | jq -r .img)"
# Download the comic
wget $COMIC_URL -O $COMIC_LOC
# Change the colors of the comic
convert $COMIC_LOC +level-colors $FG,$BG $COMIC_RECOL
# Put the comic on the original image
convert -composite -gravity center $BG_DEF $COMIC_RECOL $OUT
