import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 

img = Image.new('RGB', (200, 100), color = 'skyblue')
st.image(img, caption='Sample Image', use_container_width=True)

data = pd.DataFrame(np.random.randn(20, 3), columns=['x', 'y','z'])
st.line_chart(data)

st.video("https://www.youtube.com/watch?v=eAgONwZ_dKM")

st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")