
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
import plotly.express as px
import emoji


from PIL import Image
image = Image.open('header!.png')

st.image(image, caption=' ')




consumer_key = "pTivamyKt0GtxZiFizMMhsouj"
consumer_sec = "HEkXmzyaALIAD1AfTHLdRnegC8rstIY2AUHbrzvRGIjoJl3PCo"

# from proxy server we need to connect
access_token = "1490018179690602500-6dR6g69GHBE1fMZICvqyDMKrJINNyS"
access_token_sec = "ZAjbICteZd6FsbWEHeP2SIlmmdIycSEvgoOfJaXjf9wTs"
dir(tweepy)

auth=tweepy.OAuthHandler(consumer_key,consumer_sec)

auth.set_access_token(access_token,access_token_sec)

api_connect=tweepy.API(auth)

auth = tweepy.OAuthHandler(consumer_key,consumer_sec)
auth.set_access_token(access_token,access_token_sec)
api = tweepy.API(auth)

add_selectbox = st.sidebar.selectbox("Rate the app ",("😁", "😊", "😑","😖","😡"))

from PIL import Image
image = Image.open('sidebar1.png')

st.sidebar.image(image)


twid = st.text_input('Enter the id of the person( Eg. @elonmusk )', 'your_id')
st.write('The id is', twid)


posts = api.user_timeline(screen_name=twid, count = 10, lang ="en", tweet_mode="extended")
print("Show the 6 recent tweets:\n")
i=1
for tweet in posts[:9]:
    print(str(i) +') '+ tweet.full_text + '\n')
    i= i+1

d= pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


def cleanTxt(text):
 text = re.sub('@[A-Za-z0–9]+', '', text)
 text = re.sub('#', '', text)
 text = re.sub('https?:\/\/\S+', '', text)
 text = re.sub(':', '  ', text)
 text = re.sub('_','  ', text)
 text = re.sub('RT[\s]+', '', text)
 text=emoji.demojize(text)


 return text

d['Tweets'] = d['Tweets'].apply(cleanTxt)


def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity
def getPolarity(text):
   return  TextBlob(text).sentiment.polarity
d['Subjectivity'] = d['Tweets'].apply(getSubjectivity)
d['Polarity'] = d['Tweets'].apply(getPolarity)

net=0
neg=0
pos=0
def getAnalysis(score):
 global net,neg,pos
 if score < 0:
  neg+=1
  return 'Negative'
 elif score == 0:
  net+=1
  return 'Neutral'
 else:
  pos+=1
  return 'Positive'
d['Analysis'] = d['Polarity'].apply(getAnalysis)
(
 d
 .style
 .background_gradient(cmap="PuRd_r")

)

if(neg>pos):
  st.header("Sentimental Analysis of Tweets")
  st.header("The person is depressed!!!")
else:
  st.header("Sentimental Analysis of Tweets")
  st.header("The person is not depressed!!")
page_bg_img = '''
<style>
body {
background-image: url("https://img.freepik.com/free-photo/pastel-background-sky-feminine-style_53876-104862.jpg?size=626&ext=jpg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
d


st.subheader('Scatterplot analysis')
selected_x_var = st.selectbox('What do you want the x variable to be?', d.columns)
selected_y_var = st.selectbox('What do you want the y variable to be?', d.columns)
selected_c_var = st.selectbox('Color?', d.columns)


#fig = px.scatter(d, x="Subjectivity", y="Polarity",color="Analysis")
fig1 = px.scatter(d, x = d[selected_x_var], y = d[selected_y_var],color=d[selected_c_var])
st.plotly_chart(fig1)


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

from PIL import Image
image = Image.open('footer.png')

st.image(image, caption=' ')
