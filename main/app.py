import whisper
from pytube import YouTube
import os
model= whisper.load_model("base")
yt_url = input("Paste a youtube link here!:")

def download_youtube_audio(url) :
  yt = youtube(url)
  stream = yt.streams.filter(only_audio=True).first()
  stream.download(filename="yt_audio.mp3")
  return "yt_audio.mp3"
if yt_url:
  filename = download_youtube_audio(yt_url)

result = model.transcribe(filename)
transcript = result["text"]
print("📜 Transcript:\n")
print(transcript)

import openai
openai.api_key = "your-openai-api-key"

def generate_notes(text):
  prompt = f"summarize these lecture notes clearly and simply:\n{text}"
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo" ,
      messages=[{"role": "user","content": prompt}]
  )
  return response['choices'][0]['message']['content']

notes = generate_notes(transcript)
print(notes)
def generate_flashcards(text):
  prompt = f"make 10 flashcards from this content in Q: A: format.\n{text}"
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}]
  )
  return response['choices'][0]['message']['content']

flashcards = generate_flashcards(transcript)
print(flashcards)
