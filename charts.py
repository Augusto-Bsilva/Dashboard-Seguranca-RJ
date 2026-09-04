import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Built in charts")

data = pd.DataFrame(np.random.randn(20,3),columns=['A', 'B', 'C'])

st.subheader("Line chart")
st.line_chart(data)

st.subheader("Area chart")
st.area_chart(data)

st.subheader("Bar chart")
st.bar_chart(data)

st.title("Plotly Demo")
fig = px.scatter(data, x='A', y='B', color='C', title='Plotly Scatter')
st.plotly_chart(fig)

st.title("Seaborn Example")
fig, ax = plt.subplots()
sns.histplot(data['A'], kde=True, ax=ax)
st.pyplot(fig)