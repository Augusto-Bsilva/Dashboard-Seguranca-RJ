import pandas as pd
import streamlit as st
import numpy as np

data = pd.DataFrame({
    "Category": ["A", "A", "B","B", "C", "C"],
    "Subcategory": ["A1", "A2", "B1", "B2", "C1", "C2"],
    "Value": np.random.randint(10,100,6)
})

category = st.selectbox("select category",data['Category'].unique())

filtered = data[data['Category']==category]

st.write(f'Values for Category {category}')

st.table(filtered)