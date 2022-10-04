
# **to display streamlit app use this command in 
# your terminal: streamlit run app.py **

import streamlit as st
from about_page import show_about_page
from analyze_business import show_analyze_business
from analyze_marketing import show_analyze_marketing
from analyze_call_center import show_analyze_call_center
from predict_page import show_predict_page

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
    'Analyze Call Center', 
    'Predict Marketing'    
    )
)
if page == 'About the Project':
    show_about_page()
elif page == 'Analyze Business':
    show_analyze_business()
elif page == 'Analyze Marketing':
    show_analyze_marketing()
elif page == 'Analyze Call Center':
    show_analyze_call_center()      
else:
    show_predict_page()
