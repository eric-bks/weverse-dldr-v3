#!/bin/bash

# Convert MP4 to MP3
ffmpeg -i output.mp4 -q:a 0 -map a output.mp3