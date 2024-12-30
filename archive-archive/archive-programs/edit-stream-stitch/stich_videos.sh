#!/bin/bash

# Check for proper usage
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <video1> <video2> ... <videoN> <transition_video> <output_file>"
    exit 1
fi

# Extract the last argument as the output file
OUTPUT_FILE="${@: -1}"

# Create a temporary file list for ffmpeg
TEMP_FILE="inputs.txt"
> "$TEMP_FILE"  # Clear the file

# Loop through all video segments and add to the file list
for (( i=1; i<$#; i++ )); do
    VIDEO="${!i}"
    echo "file '$VIDEO'" >> "$TEMP_FILE"
    echo "file 'transition.mp4'" >> "$TEMP_FILE"
done

# Remove the last transition entry
sed -i '$d' "$TEMP_FILE"

# Stitch the videos together
ffmpeg -f concat -safe 0 -i "$TEMP_FILE" -c copy "$OUTPUT_FILE"

# Clean up
rm "$TEMP_FILE"
