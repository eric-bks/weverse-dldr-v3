#!/bin/bash

# Check for proper usage
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <transition_text> <output_transition_file>"
    exit 1
fi

# Assign arguments
TRANSITION_TEXT=$1
OUTPUT_FILE=$2
FONT_PATH="/path/to/font.ttf" # Change this to your font path

# Create the transition video
ffmpeg -f lavfi -i color=c=black:s=1920x1080:d=3 -vf "drawtext=fontfile=${FONT_PATH}:text='${TRANSITION_TEXT}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2" -t 3 "${OUTPUT_FILE}"
