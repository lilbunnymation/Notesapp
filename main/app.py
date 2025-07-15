import streamlit as st
from pytube import YouTube
import openai
import uuid
import os

openai.api_key = st.secrets["openai_api_key"]

def download_youtube_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = f"yt_audio_{uuid.uuid4().hex}.mp3"  # unique filename to avoid clashes
    stream.download(filename=filename)
    return filename

def generate_notes(text):
    prompt = f"summarize these lecture notes clearly and simply:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_flashcards(text):
    prompt = f"make 10 flashcards from this content in Q: A: format:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

st.title("🎓 NoteSnap")
st.subheader("Turn a YouTube video into notes + flashcards!")
yt_url = st.text_input("📺 Paste a YouTube video link here:")

if yt_url:
    try:
        with st.spinner("🎧 Downloading and transcribing..."):
            filename = download_youtube_audio(yt_url)
            with open(filename, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]

        st.subheader("📝 Transcript")
        st.text_area("Transcript:", value=transcript, height=300)
        st.success("✅ Transcription complete! Scroll down to see your notes and flashcards.")
        st.markdown("---")

        notes = generate_notes(transcript)
        st.subheader("📚 Study Notes")
        st.markdown(notes)
        st.markdown("---") 

        flashcards = generate_flashcards(transcript)
        st.subheader("🧠 Flashcards")
        st.text_area("Q&A Style Flashcards:", value=flashcards, height=300)
        st.markdown("---")

        os.remove(filename)  # delete the audio file to save space
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.info("Done studying? Refresh to try a new video or upload another one!")
