from pytube import YouTube
import moviepy.editor as mp
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)


class Downloaders():
    def __init__(self, Video_path, Audio_path, text_file):
        self.Video_path = Video_path
        self.Audio_path = Audio_path
        self.text_file = text_file
        
    def videDownloader(self, link):
        #stories in english - Mysteries Caves - English Stories - Moral Stories in English
        video_url = link

        # Create a YouTube object
        yt = YouTube(video_url)

        #get the highest resolution available
        video = yt.streams.get_highest_resolution()


        filename = self.Video_path  # Adjust the filename and extension as needed

        try:
            video.download(filename=filename)
            print("Video Download complete!")

        except Exception as e:
            print(f"An error occurred: {e}")



    def audioDownloader(self):



        # Load the video clip
        video = mp.VideoFileClip(self.Video_path)

        # Extract and write audio
        video.audio.write_audiofile(self.Audio_path)

        # Clean up 
        video.close()


    def deepgram_audio2txt(self):
        load_dotenv()

        API_KEY = os.getenv('api_key')

        AUDIO_FILE = self.Audio_path
        text_file = self.text_file



        try:
            # STEP 1 Create a Deepgram client using the API key
            deepgram = DeepgramClient(API_KEY)

            with open(AUDIO_FILE, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            #STEP 2: Configure Deepgram options for audio analysis
            options = PrerecordedOptions(
            model="nova-2",
            language="en",
            summarize="v2", 
            topics=True, 
            intents=True, 
            smart_format=True, 
            punctuate=True, 
                )

            # STEP 3: Call the transcribe_file method with the text payload and options
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

            # STEP 4: Print the response
            Final_text = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            with open(text_file, 'w') as reader:
                write_text = reader.write(Final_text)
            print(Final_text)



        except Exception as e:
            print(f"Exception: {e}")




    def elevenLabsPlayerFromText(self):
        with open(self.text_file, 'r') as file:
            text2Convert = file.read()

        api_key = os.getenv("eleven_labs_api_key")
        client = ElevenLabs(api_key=api_key)
        audio_response = client.generate(text=text2Convert, voice='Paul', output_format='mp3_44100_64')
        play(audio_response, use_ffmpeg=False)


