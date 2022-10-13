
import streamlit as st
from PIL import Image

def show_about_page():
    st.title('Welcome to this Dashboard for Business and Marketing Analysis + Marketing Prediction Web App')
    #image = Image.open('cecut.jpg')
    #st.image(image, caption = 'Going to Tijuana Cultural Center (CECUT) is always a great idea.')
    
    st.write('My name is [Bryan Ponce](https://www.linkedin.com/in/bryan-fernando-ponce/) and I present to you the Dashboard for Business and Marketing Analysis + Marketing Prediction Web App.')
    
    st.write('I decided to develop this application with the goal of automating metric analysis for decision making and a prediction page where you can see allocation suggestions that could be helpful for you to maximize your marketing results.')   
    
    st.write("""### Original Data""")
    st.write('* This project started with a spreadsheet that gathers a year of information from different platforms, such as Facebook Ads, Google Ads, Hubspot and more with more than 66k observations. This Dataset was used to create visualizations in Marketing, Business and Call Center analysis pages.')
    st.write('* After crossing information using a pivot table, the number of observations reduced to 4,599, which is the Dataset I will be using for my modeling.')
    st.write('* Most important feature to calculate budget was the number of paid leads with 0.79 Pearson Correlation Score.')
    st.write('* 9 regression models were used for this project being XGBoost the model with best performance on test data with 0.75 R2 score, which is the model that I used in the predict page.')
    st.write('* I included important Data in the predict page that can help the user find realistic goals based on the last cycle of campaigns. A cool feature here is that the metrics are dynamic and they change as you filter and select your objectives.')
    
    st.write("""### Considerations for further versions""")
    st.write("* It's important to consider optimize our campaign labeling. I didn't use these labels because we have more than 60 different labels.")
    st.write('* I would like to include new features such as sex, city and age. I think this could help to improve the model performance.')
    st.write("* The most important feature I would like to include is the connection to my platforms' APIs, to keep my Data updated and not fixed as it is Today.")
    
    st.write("""### What I loved of this project""")
    st.write("I am a marketer since 2015, and I've been hearing more and more about algorithms, Artifficial Intelligence, Machine Learning and much more in the roles I worked on, so to me was a big step deciding to learn Data Science. I feel really excited for all the upcoming challenges, applying what I've learn.")
    st.write("It's amazing to find out how much you actually know and how much you can build from all the knowledge you got in the last year of programming experience. I must say I'm surprised I was capable of creating this web app and I encourage you to learn a programming language that can help you create tools for your everyday tasks.")
    
    st.write('If you want to give me some feedback, you can always contact me in [Linked In](https://www.linkedin.com/in/bryan-fernando-ponce/) or via email: bryanponce93@yahoo.com')
    st.write("You can see the full code required to do this app in its [GitHub repo.](https://github.com/BryanPonce/marketing-app)")  
    
    # hide streamlit style---------------

    hide_style= """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

    st.markdown(hide_style, unsafe_allow_html=True)

