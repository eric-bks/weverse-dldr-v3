'''file pipeline:
Main.py
    split_link.py
    convert_to_links.sh
    ffmpeg (copy .mp4)
    ffmpeg (convert .mp3)
'''


# TODO: TEST print statements
# TODO: add auto indexing (in set variables section)

# Imports
import subprocess
from split_link import set_variables

# [Manual] Download m3u8
# [Manual] Move m3u8 to parent directory

# [Manual] Copy m3u8 URL from Weverse
file_url = input("Enter m3u8 URL: ")
print(f"\n>>> received input URL: {file_url}")

# Set variables
year = "2024"
base_url, input_m3u8, auth_token, month_num, date = set_variables(file_url)
output_m3u8 = "output_m3u8_" + input_m3u8
output_mp4 = "output_mp4_" + date + ".mp4"    # RENAME HERE FOR MORE SAME-DAY FILES TODO: add auto indexing
output_mp3 = "output_mp3_" + date + ".mp3"    # RENAME HERE FOR MORE SAME-DAY FILES 
print("\n" + "="*50)
print("\n-----> following variables set:\nbase_url, input_m3u8, auth_token, month_num, date,\noutput_m3u8, output_mp4, and output_mp3\n\n\n")

# Convert .ts to links
print("\n-----> converting .ts to links")
subprocess.run(["bash", "convert_to_links.sh", base_url, input_m3u8, auth_token, output_m3u8])
print("\n" + "="*50)
print(f"\n-----> {output_m3u8} created\n\n\n")

# Download .mp4
print(f"\n-----> downloading .mp4")
subprocess.run(["ffmpeg", "-protocol_whitelist", "https,file,crypto,data,tcp,tls", "-i", output_m3u8, "-c", "copy", output_mp4])
print("\n" + "="*50)
print(f"\n-----> {output_mp4} created\n\n\n")

# Create mp3
print("\n-----> converting an .mp3")
subprocess.run(["ffmpeg", "-i", output_mp4, "-q:a", "0", "-map", "a", output_mp3])
print("\n" + "="*50)
print(f"\n-----> {output_mp3} created\n\n\n")

# [Manual] Upload mp4 to YouTube
# https://studio.youtube.com/channel/@KkuraFIMLY

# [Manual] Upload mp3 to colab
# https://colab.research.google.com/drive/1kmnzxf7a-wGjsEDXjO46PyVxQOv54tW0