from requirements import Downloaders
Video_path = "Downloaded_video.mp4"
Audio_path = "Converted_audio.mp3"
youtube_video_link = "https://www.youtube.com/watch?v=wxb3yeBxkqE"
text_file = "transcription.txt"

players = Downloaders(Video_path=Video_path, Audio_path=Audio_path, text_file=text_file)
players.videDownloader(youtube_video_link)
players.audioDownloader()
players.deepgram_audio2txt()
players.elevenLabsPlayerFromText()