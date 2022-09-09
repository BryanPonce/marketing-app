
import streamlit as st
from PIL import Image

def show_about_page():
    st.title('Welcome to this Dashboard for Business and Marketing Analysis + Marketing Prediction Web App')
    #image = Image.open('cecut.jpg')
    #st.image(image, caption = 'Going to Tijuana Cultural Center (CECUT) is always a great idea.')
    
    st.write('My name is [Bryan Ponce](https://www.linkedin.com/in/bryan-fernando-ponce/) and I present to you the Dashboard for Business and Marketing Analysis + Marketing Prediction Web App.')
    
    st.write('I decided to develop this application with the goal of automating metric analysis for decision making and a prediction page where you can see allocation suggestions that could be helpful for you to maximize your marketing results.')   
    
    st.write("""### Original Data""")
    st.write('* This project started with a spreadsheet that gathers a year of information from different platforms, such as Facebook Ads, Google Ads, Hubspot and more with more than 45k observations. This Dataset was used to create visualizations in Marketing and Business analysis pages.')
    st.write('* After crossing information using a pivot table, the number of observations reduced to 5,444, which is the Dataset I will be using for my modeling.')
    #st.write("* Most important feature for calculating price was the number of bathrooms with 0.56 Pearson Correlation Score.")
    #st.write("* 9 regression models were used for this project being XGBoost Regressor the model with best performance on test data with 0.77 R2 score, which is the model that we can use in the Predict page.")
    #st.write("* The plots shown on the Explore page are made with outliers except the Price for location plot.")
    
    #st.write("""### Considerations for further versions""")
    #st.write("* As with any data project, the more data that we have the better. Surely, with more than 517 houses we could build better models.")
    #st.write("* We missed a better way to sectorialize the houses. A cluster was made in order to classify the houses as West, Mid-West, Mid-East and East but once they were included in the models they failed to improve these.")
    #st.write("* Having more features like the materials of which the house is made or the time since the house was built could significantly improve the models.")
    #st.write("* An Artificial Neural Network was implemented, however in didn't gave a better performance than previous models. As I'm currently studying TensorFlow and Deep Learning, in the future we could retry this ANN approach, however in the case still we don't get better results it won't be a surprise because [tree-based models are still better than neural nets when working with tabular data.](https://arxiv.org/abs/2207.08815)")
    
    
    #st.write("I learned a lot and had some fun doing this project. Hope to look it again in the future with more knowledge in order to improve it. Thank you for reading this far and have fun using this app.")
    #st.write("I'm always open to hear feedback and I would deeply appreciate it! You can contact me through [LinkedIn](https://www.linkedin.com/in/ivanverdugo-analytics/) or you can shoot me an email to jesusivan.vc21@gmail.com")
    #st.write("You can see the full code required to do this app in its [GitHub repo.](https://github.com/IvanVC21/Tijuana-House-Prices)")
    
