import streamlit as st
import pandas as pd
from io import BytesIO
import base64
from fpdf import FPDF

st.title("Export Data Demo")

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Miles': [10, 20, 30],
    'Races': [5,10,15]
})

st.dataframe(df)

#CSV dowload
csv = df.to_csv(index=False).encode()
st.download_button("Download CSV", csv, "data.csv", "text/csv")

#Excel dowload
def to_excel(df):
    output=BytesIO()
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()   
    return processed_data

excel_data = to_excel(df)
st.download_button("Dowload Excel", excel_data, "data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") 

#PDF dowload
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', size=12)
for i, row in df.iterrows():
    pdf.cell(200,10,txt=f"{row['Name']}, {row['Miles']}, {row['Races']}", ln=True,)

pdf_bytes = pdf.output(dest='S').encode('latin1')#Corect way to get bytes from FPDF object
st.download_button("Dowload PDF", pdf_bytes, "report.pdf", "application/pdf")

########################################################

st.title("File Upload History")

if 'uploads' not in st.session_state:
    st.session_state.uploads = []

uploaded_file = st.file_uploader("Upload a File")

if uploaded_file:
    st.session_state.uploads.append({
        'filename': uploaded_file.name,
        'size': uploaded_file.size,
        'type': uploaded_file.type
    })
    st.success(f"Uploaded {uploaded_file.name}")
st.write("Upload History:")
st.table(st.session_state.uploads)