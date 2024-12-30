# WORKFLOW INSTRUCTIONS:

## Download Video

<!-- COMPLETE -->

1. (Manual) **Download** .m3u8 file

   - **Go to** https://weverse.io/lesserafim/live

   - **Select** latest live

   - **Press** F12, then **select** network tab
   - **Filter** by .m3u8
   - **Set resolution** to 1080p
   - **Access** .m3u8 link by opening in separate tab to download
   - **Save** to folder

2. **Run** [Main.py](Main.py) in VSCode
   - (Manual) **Input** .m3u8 URL
     - _internal_: [Set variables](set_variables.py)
     - _internal_: [Convert to links](convert_to_links.sh)
     - _internal_: **Copy** .mp4 from server with ffmpeg
     - _internal_: **Create** .mp3 from .mp4 with ffmpeg
   - **Output** .mp4 and .mp3

## Upload Video

<!--
automate:
   - upload to youtube
   - edit date
   - edit title
   - pin comment (?)
-->

3. **Upload** .mp4 to [YouTube](https://studio.youtube.com/channel/@KkuraFIMLY)
   - **Edit** date
   - **Edit** title
   - [Manual] **Verify** tags, end screen, unlisted
   - **Pin** comment "Please let me know of any corrections 🙇"
   - **Publish** at the end

## Process Subtitles with Colab and

<!--
integrate model large-v3 in google drive

automate:
   - upload to colab
   - mount google drive (?)
   - SubtitleEdit main functions (?)
-->

4. **Upload** .mp3 to [Colab](https://colab.research.google.com/drive/1kmnzxf7a-wGjsEDXjO46PyVxQOv54tW0#scrollTo=_JkiAGAUGUb9) ([Drive link](https://drive.google.com/drive/folders/1JYBl2cNPybWEt-8E49cnu6DOlcVw8QiI))
   - **Run** block one
     - _internal_: **Install** whisper
     - _internal_: **Install** and **update** ffmpeg
   - **Run** block two
     - _internal_: **import** whisper
     - _internal_: **run** whisper to create .srt
   - **Download** .srt
5. **Edit** .srt file

   - **Run** SubtitleEdit
   - Edits:
     - Merge lines with Same Text
     - Merge short lines
     - Visual Sync
     - Multiple Replace...
     - Spell Check
     - Fix common errors
     - Beautify Timecodes
     - Netflix Quality Check
   - **Review** subtitles

## Create Thumbnail

<!--
automate:
   - enabling guidelines
   - title and caption creation
   - title and caption centering and offset
   - upload to YouTube (?)

set default location:
   - .xcf save
   - .png export
-->

6. **Edit** thumbnail
   - **Screenshot** from video
   - **Open** with GIMP
   - **Add** Guidelines
     - Image &rarr; Guides &rarr; New Guide (by Percent)...
     - H 33.33, 66.66
     - V 33.33, 66.66
   - **Scale** image (Shift+S)
   - **Position** group in lower two-thirds
   - **Add** title, 180px
     - **Center** title XY distribution
     - **Set** title offset to Y: -360
     - **Outline**
       - Layer &rarr; Text to Path
       - Edit &rarr; Stroke Path
         - **Stroke** Line, Solid Color, 6px
   - **Add** caption "_ENG SUB ON_", 90px
     - **Center** caption XY distribution
     - **Set** caption offset to X: -640, Y: 360
     - **Outline**
       - Layer &rarr; Text to Path
       - Edit &rarr; Stroke Path
         - **Stroke** Line, Solid Color, 4px
   - **Save** as .xcf
   - **Export** to .png
   - **Upload** to [YouTube](https://studio.youtube.com/channel/@KkuraFIMLY)
