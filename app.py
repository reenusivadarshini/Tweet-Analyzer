
import tweepy
from  textblob import TextBlob 
import pandas as pd
import numpy as np
import re
import string
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def navigation():
    try:
        path = st.experimental_get_query_params()['p'][0]
    except Exception as e:
        st.error('Please use the main ')
        return None
    return path


if navigation() == "home":
    st.title('Home')
    st.write('This is the home page.')

elif navigation() == "results":
    st.title('Results List')
    for item in range(25):
        st.write(f'Results {item}')

elif navigation() == "analysis":
    st.title('Analysis')
    x, y = st.number_input('Input X'), st.number_input('Input Y')
    st.write('Result: ' + str(x+y))

elif navigation() == "examples":
    st.title('Examples Menu')
    st.write('Select an example.')


elif navigation() == "logs":
    st.title('View all of the logs')
    st.write('Here you may view all of the logs.')


elif navigation() == "verify":
    st.title('Data verification is started...')
    st.write('Please stand by....')


elif navigation() == "config":
    st.title('Configuration of the app.')
    st.write('Here you can configure the application')
    
 
