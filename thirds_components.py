import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.title("3rd party components")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

lottie_url = "https://assets10.lottiefiles.com/packages/lf20_1pxqjqps.json"
lottie_json = load_lottieurl(lottie_url)

st_lottie(lottie_json,height=200)