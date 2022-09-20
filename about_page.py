
import streamlit as st
from PIL import Image

def show_about_page():
    st.title('Welcome to this Dashboard for Business and Marketing Analysis + Marketing Prediction Web App')
    #image = Image.open('cecut.jpg')
    #st.image(image, caption = 'Going to Tijuana Cultural Center (CECUT) is always a great idea.')
    
    st.write('My name is [Bryan Ponce](https://www.linkedin.com/in/bryan-fernando-ponce/) and I present to you the Dashboard for Business and Marketing Analysis + Marketing Prediction Web App.')
    
    st.write('I decided to develop this application with the goal of automating metric analysis for decision making and a prediction page where you can see allocation suggestions that could be helpful for you to maximize your marketing results.')   
    
    st.write("""### Original Data""")
    st.write('* This project started with a spreadsheet that gathers a year of information from different platforms, such as Facebook Ads, Google Ads, Hubspot and more with more than 46k observations. This Dataset was used to create visualizations in Marketing and Business analysis pages.')
    st.write('* After crossing information using a pivot table, the number of observations reduced to 1,890, which is the Dataset I will be using for my modeling.')
    st.write('* Most important feature for calculating assistants was the number of Eventbrite registrations with 0.89 Pearson Correlation Score.')
    st.write("* 9 regression models were used for this project being Random Forest Regressor the model with best performance on test data with 0.73 R2 score, which is the model that we can use in the Predict page.")
    
    st.write("""### Considerations for further versions""")
    st.write("* It's important to consider optimize our campaign labeling. I didn't use these labels because we have more than 60 different labels.")
    st.write("* I would like to include new features such as sex, city and age. I think this could help to improve the model performance.")
    
    
    #st.write("I learned a lot and had some fun doing this project. Hope to look it again in the future with more knowledge in order to improve it. Thank you for reading this far and have fun using this app.")
    #st.write("I'm always open to hear feedback and I would deeply appreciate it! You can contact me through [LinkedIn](https://www.linkedin.com/in/ivanverdugo-analytics/) or you can shoot me an email to jesusivan.vc21@gmail.com")
    #st.write("You can see the full code required to do this app in its [GitHub repo.](https://github.com/IvanVC21/Tijuana-House-Prices)")
    
