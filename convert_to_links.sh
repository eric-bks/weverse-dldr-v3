#!/bin/bash

# Define variables
BASE_URL=$1
INPUT_M3U8=$2
AUTH_TOKEN=$3

OUTPUT_M3U8=$4

# Create or empty the output file
> "$OUTPUT_M3U8"

# Read the input m3u8 file line by line
while IFS= read -r line
do
    # If the line is a .ts file, prepend the base URL and append the auth token
    if [[ "$line" == *.ts ]]; then
        echo "${BASE_URL}${line}${AUTH_TOKEN}" >> "$OUTPUT_M3U8"
    else
        # For non .ts lines (e.g., #EXTM3U, #EXTINF, etc.), just copy them as-is
        echo "$line" >> "$OUTPUT_M3U8"
    fi
done < "$INPUT_M3U8"
