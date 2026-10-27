import streamlit as st
import requests

st.title("First aerosound frontend!")

folder = st.text_input('please write down the file address:', '/kaggle/input/datasets/bisheshgiri/mimii-dataset/-6_dB_fan/fan/id_00/abnormal/00000000.wav')

url = "https://aerosound-app-764002966062.europe-west1.run.app/predict"



params = dict(wav_name= folder)

response = requests.get(url, params)

sound_class = response.json()['predicted classification']
st.write(f"The predicted class is {sound_class}.")
