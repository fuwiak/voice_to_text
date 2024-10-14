import streamlit as st
import subprocess
import speech_recognition as sr
import io
import tempfile
import os

# Title
st.title('Голосовое сообщение в текст (OGG Only)')

# Upload OGG audio file
voice_message = st.file_uploader("Загрузите голосовое сообщение (OGG)", type=['ogg'])

if voice_message is not None:
    # Save uploaded OGG file to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_ogg_file:
        temp_ogg_file.write(voice_message.read())
        temp_ogg_file_path = temp_ogg_file.name

    # Convert OGG to WAV using ffmpeg subprocess
    def convert_ogg_to_wav(ogg_file_path):
        wav_output = ogg_file_path.replace('.ogg', '.wav')  # Change file extension to .wav
        try:
            # Directly call 'ffmpeg' (no need for explicit binary path on Ubuntu)
            subprocess.run(['ffmpeg', '-i', ogg_file_path, wav_output], check=True)
            return wav_output
        except subprocess.CalledProcessError as e:
            st.error(f"Ошибка при преобразовании OGG в WAV: {e}")
            return None

    # Convert OGG to WAV
    wav_file_path = convert_ogg_to_wav(temp_ogg_file_path)

    if wav_file_path:
        recognizer = sr.Recognizer()

        # Load the converted WAV audio with speech recognition
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)

        try:
            # Recognize the text (support Russian and English)
            text = recognizer.recognize_google(audio_data, language='ru-RU')  # Use 'ru-RU' for Russian, 'en-US' for English
            st.write('### Распознанный текст из голосового сообщения:')
            st.write(text)
        except sr.UnknownValueError:
            st.write("Не удалось распознать текст. Попробуйте снова.")
        except sr.RequestError as e:
            st.write(f"Ошибка при запросе к сервису распознавания речи: {e}")
    else:
        st.write("Не удалось преобразовать OGG файл в WAV.")
