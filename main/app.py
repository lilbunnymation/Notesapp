import streamlit as st
from pytube import YouTube
import openai
import os

openai.api_key = "your-openai-api-key"
st.title("🎓 NoteSnap")
st.subheader("Turn a YouTube video into notes + flashcards!")
yt_url = st.text_input("📺 Paste a YouTube video link here:")
def download_youtube_audio(url):
  yt = YouTube(url)
  stream = yt.streams.filter(only_audio=True).first()
  stream.download(filename="yt_audio.mp3")
  return "yt_audio.mp3"
if yt_url:
  with st.spinner("🎧 Downloading and transcribing..."):
    filename = download_youtube_audio(yt_url)
    st.sbheader("📝 Transcript")
    st.text_area("Transript:", transcript, height=300)
    def generate_notes(text):
      prompt = f"summarize these lecture notes clearly and simply:\n{text}"
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo"
        messages=[{"role":"user", "content": prompt}]
      )
      return response ['choices'][0]['message']['content']
    notes = generate_notes(transcript)
    st.subheader("📚 Study Notes")
    st.markdown(notes)
    def generate_flashcards(text):
      prompt = f"make 10 flashcards from this content in Q: A: format:\n{text}"
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
      )
      return response['choices'][0]['message']['content']
    flashcards = generate_flashcards(transcript)
    st.subheader("Flashcards!")
    st.text_area("Flashcards:", flashcards, height=300)
