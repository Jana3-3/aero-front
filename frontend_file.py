import streamlit as st
import requests

st.title("First aerosound frontend!")

st.markdown("Upload a wav file")

# upload wav-file
uploaded_file = st.file_uploader("Choose a WAV file")

#conversion
if st.button('make a prediction'):
    if uploaded_file is None:
        st.write('I need a WAV-file!')
    else:
        #TODO:code a check for wav-file conformance!
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "audio/wav")} # parameter from endpoint file = "file"

        response_post = requests.post('https://aerosound-app-764002966062.europe-west1.run.app/predict', files=files)
        # local:
        # response_post = requests.post('http://127.0.0.1:8080/predict', files=files)


        if response_post.ok:
            result = response_post.json()['class']
            if result==0:
                st.write('The machine is running normally!')
            elif result==1:
                st.write('The machine might have a problem!')
        else:
            st.error(f"Fehler {response_post.status_code}: {response_post.text}")



## UI for simple text conversion
#------------------------------

# st.markdown("Prediction by text-extraction")
# folder = st.text_input('please write down the file address:', '/kaggle/input/datasets/bisheshgiri/mimii-dataset/-6_dB_fan/fan/id_00/abnormal/00000000.wav')

# url = "https://aerosound-app-764002966062.europe-west1.run.app/predict_text"



# params = dict(wav_name= folder)

# response = requests.get(url, params)

# sound_class = response.json()['predicted classification']
# st.write(f"The predicted class is {sound_class}.")
