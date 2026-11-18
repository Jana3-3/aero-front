"""AeroSound Demo Day: presentation and V8 dashboard in one Streamlit app."""
from pathlib import Path
import runpy
import streamlit as st

#--------------
# test to wake up the API early enough
import time, threading, requests

WAKE_SLIDE = 2          # index of slide 3
WAKE_COOLDOWN = 60      # time (in sec) during which no new oing is needed
API_URL = st.secrets['SERVICE_URL']

def _wake_api():
    try:
        requests.get(f"{API_URL}/", timeout=120)
    except Exception:
        pass

def wake_api_if_needed():
    last = st.session_state.get("last_ping", 0)
    if time.time() - last > WAKE_COOLDOWN:
        st.session_state["last_ping"] = time.time()
        threading.Thread(target=_wake_api, daemon=True).start()

# part II see further down after else:-statement
#-----------------------

HERE = Path(__file__).resolve().parent
SLIDES = sorted((HERE / 'slides').glob('slide-*.png'), key=lambda p: int(p.stem.split('-')[-1]))
st.set_page_config(page_title='AeroSound | Demo Day', page_icon='🎧', layout='wide', initial_sidebar_state='collapsed')

if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0
if 'aerosound_section' not in st.session_state:
    st.session_state.aerosound_section = 'Presentation'

# Global styles: apply to BOTH sections, not only when the dashboard is rendered.
st.markdown('''<style>
.stApp {background:linear-gradient(130deg,#0b192a 0%,#112d43 58%,#0a1a2c 100%);color:#f3f8fb;}
/* Reserve scrollbar space on both views to prevent horizontal jumps. */
html {overflow-y:scroll!important;scrollbar-gutter:stable!important;}
body {scrollbar-gutter:stable!important;}
/* Dashboard V8 also sets max-width:1370px. Keep the same width in both views. */
.block-container {max-width:1370px!important;padding-top:.45rem!important;padding-bottom:.5rem!important;}
[data-testid="stHeader"] {background:transparent;}
/* Radio navigation is intentionally left in normal document flow. No absolute
   positioning or transform: clickable areas remain aligned with labels. */
[data-testid="stRadio"] {background:#17384c;border:1px solid #31546a;border-radius:12px;padding:10px 16px;margin-bottom:8px;}
[data-testid="stRadio"] label {color:#f3f8fb!important;cursor:pointer;}
[data-testid="stRadio"] p {color:#f3f8fb!important;font-weight:700;font-size:1.03rem;}
[data-testid="stRadio"] input {accent-color:#29c8bd;}
[data-testid="stImage"] img {display:block;margin:auto;max-height:calc(100dvh - 155px);width:auto;max-width:100%;object-fit:contain;}
/* Navigation stays in the same position even when V8 loads its own CSS. */
[data-testid="stRadio"] {margin-top:0!important;}
/* Slide controls: high contrast, including on dark AeroSound backgrounds. */
.st-key-slide_previous button, .st-key-slide_next button {
  background:#29c8bd!important;color:#092436!important;
  border:1px solid #29c8bd!important;font-weight:750!important;
}
.st-key-slide_previous button:hover:not(:disabled), .st-key-slide_next button:hover:not(:disabled) {
  background:#6be3d8!important;color:#092436!important;
}
.st-key-slide_previous button:disabled, .st-key-slide_next button:disabled {
  background:#274658!important;color:#d2e1e8!important;
  border-color:#4a697a!important;opacity:0.8!important;
}
.st-key-slide_previous button p, .st-key-slide_next button p,
.st-key-slide_previous button span, .st-key-slide_next button span {
  color:inherit!important;
}
</style>''', unsafe_allow_html=True)

st.markdown('<div style="font-size:24px;font-weight:800;color:#f3f8fb;margin:0 0 4px">Aero<span style="color:#42d8cb">Sound</span> <span style="font-size:13px;font-weight:500;color:#c8dbe7">· Demo Day 2026</span></div>', unsafe_allow_html=True)

section = st.radio('Navigation', ['Presentation', 'Live Demo'], horizontal=True,
                   key='aerosound_section', label_visibility='collapsed')

if section == 'Presentation':
    if not SLIDES:
        st.error('Slide images missing: expected slides/slide-1.png through slide-5.png')
    else:
        i = min(st.session_state.slide_index, len(SLIDES) - 1)
        #--------
        # test wake up ping
        if i == WAKE_SLIDE:
            wake_api_if_needed()
        #---------
        left, center, right = st.columns([1, 2, 1], vertical_alignment='center')
        with left:
            if st.button('← Previous', key='slide_previous', disabled=(i == 0), use_container_width=True):
                st.session_state.slide_index = i - 1
                st.rerun()
        with center:
            st.markdown(f'<div style="text-align:center;color:#c8dbe7">Slide {i + 1} / {len(SLIDES)}</div>', unsafe_allow_html=True)
        with right:
            if st.button('Next →', key='slide_next', disabled=(i == len(SLIDES) - 1), use_container_width=True):
                st.session_state.slide_index = i + 1
                st.rerun()
        st.image(str(SLIDES[i]), use_container_width=True)
else:
    # The dashboard copy has no second set_page_config call.
    runpy.run_path(str(HERE / 'aerosound_dashboard_v8.py'), run_name='__main__')
