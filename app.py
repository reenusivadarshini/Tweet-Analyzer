
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import re
import nltk
import spacy
import string
import cv2
import easyocr

from fer import FER

import matplotlib.pyplot as plt

import matplotlib.image as mpimg

import tweepy
import csv
import sys
reader=easyocr.Reader(['en','ch_tra'])


consumer_key = "pTivamyKt0GtxZiFizMMhsouj"
consumer_secret = "HEkXmzyaALIAD1AfTHLdRnegC8rstIY2AUHbrzvRGIjoJl3PCo"
access_key = "1490018179690602500-6dR6g69GHBE1fMZICvqyDMKrJINNyS"
access_secret = "ZAjbICteZd6FsbWEHeP2SIlmmdIycSEvgoOfJaXjf9wTs"


def get_all_tweets(screen_name):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
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
        im=[]
        s=0
        s1=0
        for i in p:
          results=reader.readtext(i)
          emotion_detector = FER()
          im.append(emotion_detector.detect_emotions(i))
          emotion_detector = FER()
          result=emotion_detector.detect_emotions(i)
          detector = FER(mtcnn=True)

          emotion, score = detector.top_emotion(i) 
          im.append(score)
          if(emotion=='sad' or emotion=='angry'):
            st.write(score)
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
        print("\nPOLARITY OF THE IMAGES(IN TEXT) POSTED BY THE USER")
        print("\n",*pol)
	st.write(pol)
        print("\nPOLARITY OF THE IMAGES POSTED BY THE USER")
         #print(score)        
        print("\n",*im)
        d= pd.DataFrame([tweet for tweet in tet], columns=['Tweets'])
        ##print(d)
        d
        #print("\n",s)
        if(s+s1<0):
          print("\nThe Images posted by",screen_name,"are depressing")
        else:
          print("\nThe Images posted by",screen_name,"are not depressing")      

if __name__ == '__main__':
        get_all_tweets("@depresson_666")
