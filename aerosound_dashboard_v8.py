"""AeroSound — Streamlit dashboard prototype.
Run: python -m streamlit run aerosound_dashboard_v8.py
Requires: streamlit, requests (plus existing frontend requirements).
"""
import io
import base64
from pathlib import Path

import requests
import streamlit as st
import streamlit.components.v1 as components
import html

IMAGE_PATH = Path(__file__).with_name("aerosound_fan_v5.png")

API_URL = SERVICE_URL

st.set_page_config(page_title="AeroSound | Acoustic Monitoring", page_icon="🎧", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root {--navy:#0c1c2e;--teal:#29c8bd;--ink:#14283b;}
.stApp {background:linear-gradient(130deg,#0b192a 0%,#112d43 58%,#0a1a2c 100%); color:#f3f8fb;}
.block-container {max-width:1370px;padding-top:.7rem;padding-bottom:.6rem;}
[data-testid="stHeader"] {background:transparent;}
h1,h2,h3 {color:#f4f9fc!important;}
/* Streamlit's upload widget has its own theme rules: style every nested layer. */
[data-testid="stFileUploader"] {background:#edf5f8!important;border-radius:14px;padding:12px!important;color:#14283b!important;}
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {background:#eaf9f9!important;border:2px dashed #159e9b!important;border-radius:12px!important;}
[data-testid="stFileUploader"] section *,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {color:#123347!important;opacity:1!important;}
[data-testid="stFileUploader"] button {background:#ffffff!important;color:#123347!important;border:1px solid #159e9b!important;box-shadow:none!important;}
[data-testid="stFileUploader"] button:hover {background:#d6f6f1!important;color:#0b3b3d!important;}
[data-testid="stFileUploader"] svg {color:#0c827d!important;fill:none;}
/* Uploaded-file row: Streamlit renders this separately from the dropzone.
   Explicitly override its dark-theme surface and every text/icon layer. */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] > div,
[data-testid="stFileUploaderFileData"],
[data-testid="stFileUploaderFileData"] > div {
  background-color:#eaf9f9!important;
  color:#123347!important;
  border-radius:9px!important;
}
[data-testid="stFileUploaderFile"] *,
[data-testid="stFileUploaderFileData"] *,
[data-testid="stFileUploaderFileName"],
[data-testid="stFileUploaderFileSize"] {
  color:#123347!important;
  opacity:1!important;
}
[data-testid="stFileUploaderFile"] svg {
  color:#078f8a!important;
  stroke:#078f8a!important;
}
[data-testid="stFileUploaderFile"] button {
  background:#fff!important;
  color:#123347!important;
  border:1px solid #8bcac8!important;
  border-radius:7px!important;
}
[data-testid="stFileUploaderFile"] button svg {
  color:#123347!important;
  stroke:#123347!important;
}
/* Fallback for Streamlit releases with different internal test IDs. */
[data-testid="stFileUploader"] [data-testid*="UploadedFile"],
[data-testid="stFileUploader"] [data-testid*="FileInfo"] {
  background:#eaf9f9!important;
  color:#123347!important;
}
/* Hide Streamlit's inaccessible dark selected-file chip entirely.
   The selected filename is rendered separately in our own high-contrast panel. */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFileList"],
[data-testid="stFileUploaderFileData"] {display:none!important;}
/* The uploader may retain an empty list container in some Streamlit versions. */
[data-testid="stFileUploader"] ul {display:none!important;}
.selected-file {background:#eaf9f9;color:#123347;border:1px solid #89d2cf;
  border-radius:10px;padding:9px 12px;margin:5px 0 9px;font-size:13px;
  overflow-wrap:anywhere;}
.selected-file strong {color:#0a5d5a;}
/* Verified selected-file chip styling (Firefox inspector). */
[data-testid="stFileUploader"] [data-testid="stFileChip"] {background-color:#e8f7f7!important;color:#123347!important;border:1px solid #29c8bd!important;border-radius:8px!important;}
[data-testid="stFileChip"] *,[data-testid="stFileChipName"] {color:#123347!important;opacity:1!important;}
[data-testid="stFileChipDeleteBtn"] {color:#123347!important;}
/* Chromium audio controls: enforce light controls, including during playback. */
[data-testid="stAudio"] {background:#eaf2f6!important;border-radius:12px!important;padding:5px!important;color-scheme:light!important;}
[data-testid="stAudio"] audio, audio {width:100%;color-scheme:light!important;background:#eaf2f6!important;border-radius:10px;}
audio::-webkit-media-controls-panel {background-color:#eaf2f6!important;}
audio::-webkit-media-controls-play-button,
audio::-webkit-media-controls-mute-button {background-color:#b6eae6!important;border-radius:50%;}
audio::-webkit-media-controls-current-time-display,
audio::-webkit-media-controls-time-remaining-display {color:#15364c!important;text-shadow:none!important;}

div.stButton > button {background:#17b7ad;color:#07222d;border:0;border-radius:10px;font-weight:750;padding:.75rem 1.5rem;width:100%;min-height:48px;font-size:16px;}
div.stButton > button:hover {background:#52e0d2;color:#07222d;}
.hero {border:1px solid #31546a;background:linear-gradient(120deg,#17384c,#0b2236);border-radius:18px;padding:8px 20px;margin-bottom:7px;overflow:hidden;position:relative;min-height:72px;}
.hero:after {content:"";position:absolute;right:-30px;top:-60px;width:380px;height:280px;border-radius:50%;background:repeating-radial-gradient(circle at center,transparent 0 14px,rgba(51,222,207,.16) 15px 17px,transparent 18px 28px);transform:rotate(-24deg);}
.brand {font-size:29px;font-weight:850;letter-spacing:-1.6px;line-height:1.1;position:relative;z-index:1;}
.brand span {color:#42d8cb;}
.eyebrow {color:#6de4d8;font-size:12px;font-weight:800;letter-spacing:2.2px;text-transform:uppercase;position:relative;z-index:1;}
.tagline {color:#c8dbe7;font-size:16px;margin-top:3px;position:relative;z-index:1;}
.panel {background:#edf4f8;border:1px solid #dce9f0;border-radius:15px;padding:11px 15px;margin-bottom:8px;color:#132b3e;}
.panel-title {color:#163249;font-weight:800;font-size:17px;margin-bottom:4px;}
.panel-text {color:#516c7b;font-size:14px;line-height:1.5;}
.statline {color:#15364c;font-size:14px;margin-top:7px;}
.machine-art {height:210px;background:radial-gradient(circle at 50% 50%,#42768a 0%,#173e54 43%,#091d2c 85%);border:1px solid #3d6878;border-radius:15px;display:flex;align-items:center;justify-content:center;margin-bottom:12px;overflow:hidden;}
.machine-art svg {max-height:190px;width:100%;}
.result {border-radius:14px;padding:20px 24px;font-size:23px;font-weight:850;margin-top:8px;}
.result-normal {background:#d9f6ed;color:#07644e;border-left:7px solid #16a37d;}
.result-abnormal {background:#fff0dc;color:#965411;border-left:7px solid #e69b34;}
.result-wait {background:#eaf3f7;color:#355467;border-left:7px solid #79a5b8;}
.smallnote {color:#b8d0dd;font-size:12px;margin-top:6px;}
.machine-photo {width:100%;height:275px;object-fit:cover;object-position:center 50%;border-radius:14px;border:1px solid #3d6878;display:block;margin-bottom:8px;}
[data-testid="stFileUploader"] {padding:6px!important;}
[data-testid="stFileUploader"] section {min-height:60px!important;}
[data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"] {background:#edf4f8;border-radius:14px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><div class="eyebrow">Industrial acoustic monitoring · Prototype</div>
<div class="brand">Aero<span>Sound</span></div><div class="tagline">Listen to machines. Detect acoustic anomalies.</div></div>""", unsafe_allow_html=True)

uploaded = None
left, right = st.columns([1, 1.15], gap="medium")
with left:
    # A real machine photograph can replace this generated industrial illustration later.
    if IMAGE_PATH.exists():
        image_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("ascii")
        st.markdown(f'<img class="machine-photo" src="data:image/png;base64,{image_b64}" alt="Industrial machine">', unsafe_allow_html=True)
    else:
        st.info("Add aerosound_machine.png alongside this script to display the machine image.")
    st.markdown('''<div class="panel"><div class="panel-title">About AeroSound</div>
    <div class="panel-text">A proof of concept for acoustic anomaly detection on industrial machinery.</div>
    <div class="statline"><b>Dataset:</b> MIMII (Hitachi)</div></div>''', unsafe_allow_html=True)
    waveform_slot = st.container()


with right:
    st.markdown('<div class="panel"><div class="panel-title">01 &nbsp; Audio input</div><div class="panel-text">Upload a recording to analyze its acoustic signature.</div></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a WAV recording", type=["wav"], label_visibility="collapsed")
    if uploaded is not None:
        data = uploaded.getvalue()
        audio_b64 = base64.b64encode(data).decode("ascii")
        player_html = f"""<!doctype html><html><head><meta charset='utf-8'><style>
        *{{box-sizing:border-box}}body{{margin:0;font-family:Arial,sans-serif;background:#edf4f8;color:#123347}}
        .player{{display:flex;align-items:center;gap:12px;padding:9px 12px;border-radius:12px;border:1px solid #cbdde6;background:#edf4f8}}
        button{{background:#078f8a;color:white;border:0;border-radius:50%;width:43px;height:43px;flex-shrink:0;font-size:19px;cursor:pointer}}
        button:hover{{background:#08726f}}button:focus-visible{{outline:3px solid #073e51;outline-offset:2px}}
        input[type=range]{{accent-color:#078f8a;flex:1;min-width:35px;cursor:pointer}}
        .time{{font-size:12px;white-space:nowrap;color:#183c50}}
        </style></head><body><div class='player'>
        <button id='play' aria-label='Play audio'>▶</button><span class='time' id='clock'>0:00 / 0:00</span>
        <input type='range' id='seek' min='0' max='1000' value='0' aria-label='Audio position'>
        <button id='mute' aria-label='Mute audio' style='font-size:16px;width:34px;height:34px'>♫</button>
        <audio id='audio' preload='metadata' src='data:audio/wav;base64,{audio_b64}'></audio></div>
        <script>
        const a=document.getElementById('audio'),p=document.getElementById('play'),m=document.getElementById('mute'),s=document.getElementById('seek'),c=document.getElementById('clock');
        const fmt=x=>Number.isFinite(x)?Math.floor(x/60)+':'+String(Math.floor(x%60)).padStart(2,'0'):'0:00';
        const update=()=>{{c.textContent=fmt(a.currentTime)+' / '+fmt(a.duration);s.value=a.duration?Math.round(a.currentTime/a.duration*1000):0;}};
        p.onclick=()=>{{if(a.paused){{a.play().catch(()=>{{p.textContent='▶';}});}}else a.pause();}};
        a.onplay=()=>{{p.textContent='❚❚';p.setAttribute('aria-label','Pause audio')}};
        a.onpause=()=>{{p.textContent='▶';p.setAttribute('aria-label','Play audio')}};
        a.ontimeupdate=update;a.onloadedmetadata=update;a.onended=update;
        s.oninput=()=>{{if(a.duration)a.currentTime=s.value/1000*a.duration}};
        m.onclick=()=>{{a.muted=!a.muted;m.textContent=a.muted?'×':'♫';m.setAttribute('aria-label',a.muted?'Unmute audio':'Mute audio')}};
        </script></body></html>"""
        components.html(player_html, height=68, scrolling=False)
    if "last_file" not in st.session_state:
        st.session_state.last_file = None
        st.session_state.prediction = None
        st.session_state.error = None
    if uploaded is None or uploaded.name != st.session_state.last_file:
        st.session_state.prediction = None
        st.session_state.error = None

    if st.button("Analyze sound", type="primary", disabled=uploaded is None):
        with st.spinner("Analyzing the audio recording…"):
            try:
                response = requests.post(
                    API_URL,
                    files={"file": (uploaded.name, uploaded.getvalue(), "audio/wav")},
                    timeout=90,
                )
                response.raise_for_status()
                result = response.json()["class"]
                if result not in (0, 1):
                    raise ValueError(f"Unexpected prediction class: {result!r}")
                st.session_state.prediction = result
                st.session_state.error = None
                st.session_state.last_file = uploaded.name
            except (requests.RequestException, ValueError, KeyError) as exc:
                st.session_state.prediction = None
                st.session_state.error = str(exc)

    if st.session_state.error:
        st.error(f"Analysis failed: {st.session_state.error}")
    elif st.session_state.prediction == 0:
        st.markdown('<div class="result result-normal"><div style="font-size:14px;font-weight:750;margin-bottom:5px">03 &nbsp; Prediction result</div>✓ &nbsp; NORMAL</div>', unsafe_allow_html=True)
        st.caption("No acoustic anomaly detected by this prototype model.")
    elif st.session_state.prediction == 1:
        st.markdown('<div class="result result-abnormal"><div style="font-size:14px;font-weight:750;margin-bottom:5px">03 &nbsp; Prediction result</div>⚠ &nbsp; ABNORMAL</div>', unsafe_allow_html=True)
        st.caption("Potential acoustic anomaly detected. Further inspection may be needed.")
    else:
        st.markdown('<div class="result result-wait"><div style="font-size:14px;font-weight:750;margin-bottom:5px">03 &nbsp; Prediction result</div>Awaiting analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="smallnote">Research prototype · Results are not an industrial diagnosis.</div>', unsafe_allow_html=True)

st.markdown('''<div class="smallnote">MIMII Dataset — H. Purohit et al. / Hitachi, Ltd. ·
<a href="https://zenodo.org/records/3384388" target="_blank" style="color:#80e4dd">Source (Zenodo)</a> ·
<a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" style="color:#80e4dd">CC BY-SA 4.0</a> ·
Audio recordings transformed into numerical features for model analysis.</div>''', unsafe_allow_html=True)

# Fill the waveform placeholder after the uploader is processed.
with waveform_slot:
    if uploaded is not None:
        try:
            # soundfile handles the 16-bit PCM and float WAV variants that the
            # standard-library wave reader may reject. This is DISPLAY ONLY.
            import numpy as np
            import soundfile as sf

            signal, rate = sf.read(io.BytesIO(data), dtype="float32", always_2d=True)
            frames, channels = signal.shape
            if frames == 0 or rate <= 0:
                raise ValueError("The audio file contains no samples.")
            mono = signal.mean(axis=1)
            # Preserve peaks when reducing a long signal for a compact preview.
            bins = min(240, frames)
            edges = np.linspace(0, frames, bins + 1, dtype=int)
            peaks = [float(np.max(np.abs(mono[edges[i]:edges[i + 1]])))
                     for i in range(bins) if edges[i + 1] > edges[i]]
            max_peak = max(max(peaks, default=0.0), 0.01)
            bar_width = 960 / max(len(peaks), 1)
            bars = "".join(
                f'<rect x="{i * bar_width:.2f}" y="{55 - 49 * peak / max_peak:.2f}" '
                f'width="{max(bar_width - 1, 0.6):.2f}" '
                f'height="{max(2 * 49 * peak / max_peak, 1.5):.2f}" rx="0.7"/>'
                for i, peak in enumerate(peaks)
            )
            st.markdown(
                '<div style="background:#edf4f8;border-radius:12px;padding:10px 12px">'
                '<div style="color:#163249;font-weight:800;font-size:17px;margin-bottom:6px">Audio waveform</div>'
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 110" '
                'role="img" aria-label="Audio waveform amplitude preview" '
                'style="width:100%;height:100px;display:block">'
                '<line x1="0" y1="55" x2="960" y2="55" stroke="#a8c8cf" stroke-width="1"/>'
                f'<g fill="#0caaa5">{bars}</g></svg></div>',
                unsafe_allow_html=True,
            )
            st.caption(f"{frames / rate:.1f} s · {rate:,} Hz · {channels} channel(s) · Waveform preview")
        except ImportError:
            st.warning("Waveform preview requires NumPy and SoundFile: pip install numpy soundfile")
        except Exception as exc:
            st.warning(f"Waveform preview unavailable: {exc}. The original WAV can still be analyzed.")
    else:
        st.markdown('<div class="panel"><div class="panel-title">Audio waveform</div><div class="panel-text">The waveform will appear after you upload a recording.</div></div>', unsafe_allow_html=True)
