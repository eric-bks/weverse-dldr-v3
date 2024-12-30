#!/usr/bin/env python
# coding: utf-8

# # Weverse Downloader - Rewrite

# The Weverse Downloader performs a series of tasks related to downloading, processing, and manipulating video and audio files. It includes functions to retrieve the YouTube title, create an output directory, download video files, concatenate the downloaded clips, write the final video to an .mp4 file, and play the video within a Jupyter Notebook.
# 
# Additionally, the code utilizes the Whisper ASR (Automated Speech Recognition) model to transcribe the audio from the video, convert the transcription result into SubRip subtitle format (.srt), and write it as an .srt file.

# Weverse Live streams are delivered differently from other video broadcasting websites. The src path to the stream is a blob link that leads to an error page. Third-party downloaders cannot process the link or are locked behind a paywall. 
# 
# Clips are sent from the servers in encoded segments under network requests. The request URL has a consistent format that can be edited programmatically. The request URL expires after the browser expires.

# ### imports


# Standard library imports
import os
import logging
import time

# Related third party imports
import requests
from IPython.display import display, Markdown
from moviepy.editor import concatenate_videoclips, VideoFileClip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import undetected_chromedriver as uc
import whisper
from googletrans import Translator

# Local application/library specific imports
import Credentials


class WeverseScraper:
    """
    A website scraper that accesses Weverse Live and extracts metadata from it.
    
    Attributes:
        video_url (str)
    """
    def __init__(self, video_url):
        """
        Initializes the WeverseScraper object with the video URL that will be scraped.

        Args:
            video_url (str): The URL of the video to be scraped.

        """
        self.video_url = video_url
        
    def _initialize_webdriver(self):
        """
        Starts up the webdriver.
        Loads the website.
        The webdriver is stored as an instance attribute to be used in other methods.
        """
        options = uc.ChromeOptions()
        options.add_headless = False

        self.driver_weverse = uc.Chrome(options = options)
        self.driver_weverse.get(self.video_url)
        
    def _login_to_website(self, username, password):
        """
        Logs into the website using the provided USERNAME and PASSWORD.

        This method utilizes the webdriver instance stored in self.driver_weverse to navigate the website's login process.

        Arguments:
            USERNAME (str): The username to be used for logging in.
            PASSWORD (str): The password to be used for logging in.
        """
        WebDriverWait(self.driver_weverse, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'UserJoinInduceLayerView_link__wcuim'))).click()
        WebDriverWait(self.driver_weverse, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="confirm modal"].ModalButtonView_button__B5k-Z'))).click()
        self.driver_weverse.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB + username + Keys.ENTER)
        time.sleep(2)
        self.driver_weverse.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB + Keys.TAB + password + Keys.ENTER)

    def _retrieve_title_and_date(self, YEAR):
        """
        Retrieves the title and date information from the webpage.

        This method uses the webdriver instance stored in self.driver_weverse to retrieve information from specific elements on the page.

        Arguments:
            YEAR (str): The year in which the video was uploaded.

        Returns:
            h2_text (str): The title text extracted from the webpage.
            output_name (str): The date associated with the data in the format 'yearmonthday'.
        """
        h2_text = WebDriverWait(self.driver_weverse, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'TitleView_title__SSnHb'))).text.replace("replay\n", '')
        span_text = self.driver_weverse.find_element(By.CLASS_NAME, 'HeaderView_info__j-KNX').text
        month = span_text.split('.')[0]
        day = span_text.split('.')[1]
        output_name = f'{YEAR}{month}{day}'
        return h2_text, output_name
    
    def _translate_titles(self, h2_text, output_name):
        """
        Translates the titles from Korean into English, Spanish, and Japanese.

        This method uses the Google Translate API to translate the provided h2_text into English, Spanish, and Japanese.
        It then formats these translated titles into YouTube title format for each respective language.

        Arguments:
            h2_text (str): The original title text to translate.
            output_name (str): The output name to include in the YouTube title.

        Returns:
            youtube_title (str): The formatted YouTube title in English.
            youtube_title_SPA (str): The formatted YouTube title in Spanish.
            youtube_title_KOR (str): The formatted YouTube title in Korean.
            youtube_title_JPN (str): The formatted YouTube title in Japanese.
        """
        ENG_title = Translator().translate(h2_text, dest = 'en')
        SPA_title = Translator().translate(h2_text, dest = 'es')
        JPN_title = Translator().translate(h2_text, dest = 'ja')
        
        youtube_title = f"[ENG SUB] {output_name} | LE SSERAFIM Weverse Live 🔴 ({h2_text}) {ENG_title.text}"
        youtube_title_SPA = f"[SPA SUB] {output_name} | LE SSERAFIM Weverse EN VIVO 🔴 ({h2_text}) {SPA_title.text}"
        youtube_title_KOR = f"[한국어 자막] {output_name} | 르세라핌 위버스 라이브 🔴 ({h2_text})"
        youtube_title_JPN = f"[日本語字幕] {output_name} | レ・セラフィム ウィバースライブ 🔴 ({h2_text}) {JPN_title.text}"
        return youtube_title, youtube_title_SPA, youtube_title_KOR, youtube_title_JPN
        
    def _print_titles(self, youtube_title, youtube_title_SPA, youtube_title_KOR, youtube_title_JPN):
        """
        Prints the titles.

        Arguments:
            youtube_title (str): The title of the video translated into English.
            youtube_title_SPA (str): The title of the video translated into Spanish.
            youtube_title_KOR (str): The title of the video translated into Korean.
            youtube_title_JPN (str): The title of the video translated into Japanese.
        """
        print(youtube_title)
        print(youtube_title_SPA)
        print(youtube_title_KOR)
        print(youtube_title_JPN)

        
    def execute_data_retrieval_process(self, USERNAME, PASSWORD, YEAR):
        """
        Executes the process of retrieving data by orchestrating the execution of helper functions.

        Arguments:
            USERNAME (str): The username to log into the website.
            PASSWORD (str): The password to log into the website.
            YEAR (str): The year to be used in date retrieval.

        Returns:
            output_name (str): The retrieved date associated with the data.
        """
        self._initialize_webdriver()
        self._login_to_website(USERNAME, PASSWORD)
        h2_text, output_name = self._retrieve_title_and_date(YEAR)
        youtube_title, youtube_title_SPA, youtube_title_KOR, youtube_title_JPN = self._translate_titles(h2_text, output_name)
        self._print_titles(youtube_title, youtube_title_SPA, youtube_title_KOR, youtube_title_JPN)
        self.driver_weverse.quit()
        return output_name


class VideoDownloader:
    """
    This class facilitates downloading videos from a list of network request urls and stores them in a new directory.

    Attributes:
        output_name (str): The name of the output directory where the videos will be saved.
        url_template (str): A template for the URLs of the videos to be downloaded.
                            It includes a '{code}' placeholder for the specific code of each video.
    """
    def __init__(self, output_name, network_request_url, last_code_index):
        """
        Initializes a VideoDownloader instance.

        Args:
            output_name (str): The name of the directory where the downloaded videos will be stored.
            network_request_url (str): A typical URL of the network request used to download videos.
                                        The last part of this URL, corresponding to a specific video code, 
                                        is replaced with '{code}' to form a URL template.
            last_code_index (int): The last index in the range of codes for the videos to be downloaded. 
                                    The range starts at 1.

        The resulting instance has an attribute `url_template`, which is a URL that includes a '{code}' 
        placeholder for the specific code of each video.
        """
        self.output_name = output_name
        self.url_template = network_request_url.replace(network_request_url.split('-')[-1].split('.')[0], '{code}')
        self.last_code_index = last_code_index
    
    def create_dir(self):
        """
        Checks if the specified directory exists, if not, it creates a new one.

        Arguments:
            output_name (str): The name of the output directory where the videos will be saved.
        """
        try:
            if not os.path.exists(self.output_name):
                os.makedirs(self.output_name)
        except OSError as e:
            print(f"An error occurred while creating the directory: {e}")
    
    def downloader(self, url_template, last_code_index, output_name):
        """
        Iterates over a range of network request codes and downloads the corresponding videos.
        If a video file fails to download, it prints a message indicating the failure and moves on to the next one.

        Arguments:
            url_template (str): A template for the URLs of the videos to be downloaded.
                                It includes a '{code}' placeholder for the specific code of each video.
            last_code_index (int): The last index in the range of codes for the videos to be downloaded. The range starts at 1.
            output_name (str): The name of the output directory where the videos will be saved.
        """
        with requests.Session() as session:
            for i in tqdm(range(1, last_code_index), desc="Downloading", unit="file", leave=True):
                code = f'{i:06d}'
                url = url_template.replace('{code}', code)

                try:
                    response = session.get(url)
                    if response.status_code == 200: #Checks if valid URL.
                        file_path = os.path.join(output_name, f'output_{code}.ts')
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                    else:
                        print(f"Failed to retrieve TS file with code {code}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error downloading file with code {code}: {e}")


class VideoProcessor:
    """
    A class for processing video clips. This class is responsible for loading video clips,
    concatenating these clips into a single video, and writing the final video to a file.
    """
    
    def __init__(self, output_name):
        """
        Initializes a VideoProcessor object with the given output_name.
        
        Args:
            output_name (str): The name to be used for the output directory and video file.
        """
        pass

    def load_video_clip(self, file_path):
        """
        Attempts to load a video clip from a given file path.

        Args:
            file_path (str): The path of the video file to be loaded.

        Returns:
            VideoFileClip if the video file is successfully loaded, else None.
        """
        try:
            return VideoFileClip(file_path)
        except Exception as e:
            logging.error(f"Error loading video clip from {file_path}: {e}")
            return None

    def video_clips_list(self, last_code_index, output_name):
        """
        Creates a list of VideoFileClip objects for all video files in the output directory.
        
        Args:
            last_code_index (int): The index of the last video file in the sequence.
            
        Returns:
            video_clips (list): A list of VideoFileClip objects.
        """
        cwd = os.getcwd()
        file_range = range(1, last_code_index)
        file_paths = [os.path.join(cwd, output_name, f"output_{i:06d}.ts") for i in file_range]

        video_clips = [self.load_video_clip(file_path) for file_path in tqdm(file_paths, desc="Loading Clips", unit="clip") if self.load_video_clip(file_path) is not None]
        return video_clips

    def concatenate(self, video_clips):
        """
        Concatenates the video clips into a single video.
        
        Args:
            video_clips (list): A list of VideoFileClip objects to be concatenated.
        
        Returns:
            final_clip (VideoFileClip): A VideoFileClip object representing the concatenated video.
        """
        batch_size = 10  # Number of clips to concatenate at a time
        num_batches = len(video_clips) // batch_size + 1

        # Concatenate clips in batches
        clip_batches = [video_clips[i:i+batch_size] for i in range(0, len(video_clips), batch_size)]
        concatenated_clips = []

        for clips in tqdm(clip_batches, desc='Concatenating Batches', unit='batch'):
            concatenated_clips.append(concatenate_videoclips(clips, method='compose'))

        # Concatenate the batches into a final clip
        final_clip = concatenate_videoclips(concatenated_clips, method='compose')
        return final_clip
        
    def write(self, final_clip, output_name):
        """
        Writes the final video to a file.
        
        Args:
            final_clip (VideoFileClip): The final video clip to be written to a file.
            output_name (str): The name to be used for the final clip.
        """
        final_clip.write_videofile(f"{output_name}.mp4", fps = 30, threads = 4)


class Transcription:
    """
    A class to handle transcription of video content.
    """
    def __init__(self, output_name):
        """
        Initializes a Transcription object with the provided parameters.
        
        Args:
            output_name (str): The name of the video file to be transcribed, without the .mp4 extension.
        """
        self.output_name = output_name
        
    def transcribe(self):
        """
        Transcribes the audio from the video file.
        
        This method utilizes the whisper ASR model and loads the video file based on the name 
        stored in the output_name attribute of this Transcription instance.

        Returns:
            result: The transcription result generated by the whisper ASR model.
        """
        model = whisper.load_model("tiny")
        audio = whisper.load_audio(f'{output_name}.mp4') 
        result = model.transcribe(audio, verbose = True, language = 'Korean', task = 'translate') 
        return result
        
    def format_time(self, time):
        """
        Formats a time value into the standard subtitle format (HH:MM:SS,mmm).
        
        Args:
            time (float): The time value to be formatted.

        Returns:
            str: The time formatted in the standard subtitle format.
        """
        hours = int(time // 3600)
        minutes = int((time % 3600) // 60)
        seconds = int(time % 60)
        milliseconds = int((time % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        
    def convert_to_srt(self, segments, output_file):
        """
        Converts a list of segments into SubRip subtitle format and writes them to a file.
        
        Args:
            segments (list): A list of dictionaries, where each dictionary contains information about one segment of subtitles.
            output_file (str): The name of the file where the subtitles will be written.
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            index = 1
            for segment in segments:
                
                start_time = self.format_time(segment['start'])
                end_time = self.format_time(segment['end'])
                text = segment['text']
                
                file.write(f"{index}\n")
                file.write(f"{start_time} --> {end_time}\n")
                file.write(f"{text}\n")
                file.write("\n")
                
                index += 1


if __name__ == "__main__":
    # Constants
    USERNAME = Credentials.username
    PASSWORD = Credentials.password
    YEAR = "23"
    last_code_index = (10) + 1
    video_url = "https://weverse.io/lesserafim/live/3-123907106"
    network_request_url = "https://weverse-rmcnmv.akamaized.net/c/read/v2/VOD_ALPHA/weverse_2023_07_06_0/hls/499a455b-1bed-11ee-b37e-a0369ffdede8-000109.ts?__gda__=1689273260_8c1a0de87536ac89f0d5ee2487d9798f"
    
    # Scrape the video data.
    scraper = WeverseScraper(video_url)
    output_name = scraper.execute_data_retrieval_process(USERNAME, PASSWORD, YEAR)

    # Download the videos
    downloader = VideoDownloader(output_name, network_request_url, last_code_index)
    downloader.create_dir()
    downloader.downloader(downloader.url_template, last_code_index, output_name)

    # Process the videos
    processor = VideoProcessor(output_name)
    video_clips = processor.video_clips_list(last_code_index, output_name)
    final_clip = processor.concatenate(video_clips)
    processor.write(final_clip, output_name)
    



# https://colab.research.google.com/drive/1kmnzxf7a-wGjsEDXjO46PyVxQOv54tW0?usp=sharing

# ## Post Notes

# ### To-do
# 
# - Create helper functions: _login_to_website, _get_title_info, and _translate_title.
# - Automate file run on new upload.
# - Automate network request URL.
# - Automate last_code_index.
# - Automate upload to YouTube with API.
# - Reduce Redundancy defVariables().
# - Find solution to run program off home machine.
# - Whisper JAX.
# - Kaggle Notebook TPUs.
# - Docker?
# - Automate upload using YouTube API.

# ### Limitations
# 
# - Requires manual link entry.
# - getYoutubeTitle() sometimes misclicks in webdriver.
# - Requires a lot of CPU and RAM.
# - WhisperAI large model requires 10 GB VRAM.
# - Cannot be run on my work machine due to lack of RAM.
# - Currently runs Whisper on Google Colab.
# - Concatenation leaves behind a residual stutter.
# - Whisper large-v2 has WER of 13%.
# - Whisper cannot distinguish music from speech.
# - Whisper needs to "warm-up".
# - Speed decreases until kernel is restart.
# - Cannot load too many files; kernel must be restarted after about 2 calls.
# - Too many global variables.

# In[ ]:




