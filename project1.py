import streamlit as st
import pandas as pd

st.sidebar.title('Navigation')
section = st.sidebar.radio('Go to', ['About', 'Skills', 'Experience', 'Education', 'Contact'])

skills = {
    'Python': 90,
    'Machine Learning': 80,
    'Data Analysis': 85,
    'Web Development': 70,
}

st.title("Augusto")
st.subheader("Data Scientist")

if section == 'About':
    st.markdown(f"""
       Experienced Data Scientist with strong skills in analytics, machine learning, and storytelling with data.Passionate about turning data into actionable insights
    """)
elif section == 'Skills':
    st.header("Skills Overview")
    for skill, level in skills.items():
        st.write(f"{skill}")
        st.progress(level)
    df_skills = pd.DataFrame({
        "Skill": list(skills.keys()),
        "proficiency": list(skills.values())
    })
    st.bar_chart(df_skills.set_index("Skill"))
    
elif section == 'Experience':
    st.header("Work Experience")

    with st.expander(f"Data Scientist | Company | August 2026"):
          st.write(f"""
            - Built 5 Streamlit Apps in production
            - Built 30+ Dashboards for risk and underwriting
            - Developed 20 DBT Models 
                """)
    with st.expander(f"Batman | Justice | Since born"):
          st.write(f"""
            - Always prepared 
            - Trained with ra's al ghul
            - Brought justice for Ghotam 
                    """)
    with st.expander(f"Data Analyst | IBM | September 2026"):
          st.write(f"""
            - Work with Exec team in software pricing and sales
            - Sold +2000 IBM products
            -Developed +30 AI intrgrations
                """)

          
elif section == 'Education':
        st.header("Education")
        st.write("B.S. In Information Systems, University Federal Fluminense, 2025")

elif section == 'Contact':
        st.header("Get in touch")
        col1, col2 = st.columns(2)
        with col1:
               email = st.text_input("Email")
               phone = st.text_input("Phone")
        with col2:
               linkedin = st.text_input("Linkedin")
               portfolio = st.text_input("Portfolio URL")
               discord = st.text_input("Discord")

        message = st.text_area("Message")

        if st.button("Send"):
            st.success("Thanks for reaching out! I will get back to you soon.")