
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
import csv
import sys
import easyocr
reader = easyocr.Reader(['ch_sim','en'])


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


twid = st.text_input('Enter the id the person( Eg. @userhandle )', 'your_id')
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

consumer_key1 = "pTivamyKt0GtxZiFizMMhsouj"
consumer_secret1 = "HEkXmzyaALIAD1AfTHLdRnegC8rstIY2AUHbrzvRGIjoJl3PCo"
access_key1 = "1490018179690602500-6dR6g69GHBE1fMZICvqyDMKrJINNyS"
access_secret1 = "ZAjbICteZd6FsbWEHeP2SIlmmdIycSEvgoOfJaXjf9wTs"


def get_all_tweets(screen_name):
        auth = tweepy.OAuthHandler(consumer_key1, consumer_secret1)
        auth.set_access_token(access_key1, access_secret1)
        api = tweepy.API(auth)
        alltweets = []
        new_tweets = api.user_timeline(screen_name = screen_name,count=1)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        while len(new_tweets) > 0:
          new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
          alltweets.extend(new_tweets)
          oldest = alltweets[-1].id - 1
        outtweets = [] 
        p=[]
        for tweet in alltweets:
                try:
                        print (tweet.entities['media'][0]['media_url'])
                        p.append(tweet.entities['media'][0]['media_url'])
                        
                except (NameError, KeyError):                     
                        pass
                else:                        
                        outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
        pol=[]
        tet=[]
        s=0
        for i in p:
          results=reader.readtext(i)
          text=''
          for result in results:
            text+=result[1]+ ' ' 
            tet.append(text)
          #print(tet)
          def getSubjectivity(i):
            return TextBlob(text).sentiment.subjectivity
          def getPolarity(i):
            return  TextBlob(text).sentiment.polarity
          o=getPolarity(i)
          s+=o
          pol.append(o)
          #print("\nPolarity---->",o)
        print("\n",*pol)
        d= pd.DataFrame([tweet for tweet in tet], columns=['Tweets'])
        print(d)
        d
        #print("\n",s)
        if(s<0):
          print("The Images posted by",screen_name,"are depressing")
        else:
          print("The Images posted by",screen_name,"are not depressing")
get_all_tweets("@depressingmsgs")


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

from PIL import Image
image = Image.open('footer.png')

st.image(image, caption=' ')

