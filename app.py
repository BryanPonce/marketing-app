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

page = st.sidebar.selectbox('Elige la opción deseada', (
    'Sobre el Proyecto','Analizar Negocio', 
    'Analizar Marketing', 
    'Predecir Marketing'
    )
)
#if page == 'Sobre el proyecto':
    #show_about_page()
if page == 'Analizar Negocio':
    show_analyze_business()
elif page == 'Analizar Marketing':
    show_analyze_marketing() 
#else:
    #show_predict_page()