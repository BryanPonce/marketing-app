
# **to display streamlit: streamlit run app.py **

import streamlit as st
from analyze_business import show_analyze_business
from analyze_marketing import show_analyze_marketing
#from about_page import show_about_page
#from predict_page import show_predict

# ------ streamlit configuration --------

st.set_page_config(page_title= 'Dashboard All In One',
                   page_icon= ':bar_chart:',
                   layout= 'wide'   
)

# main page sidebar

page = st.sidebar.selectbox('What do you want to see?', 
    ('About the Project',
    'Analyze Business', 
    'Analyze Marketing', 
    'Predict Marketing'
    )
)
#if page == 'About the Project':
    #show_about_page()
if page == 'Analyze Business':
    show_analyze_business()
elif page == 'Analyze Marketing':
    show_analyze_marketing() 
#else:
    #show_predict_page()