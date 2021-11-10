from os import write
import boto3
import json
from google.protobuf.symbol_database import Default 
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout='wide')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 




st.sidebar.title("NLP Services")
st.sidebar.image('img/sidepic.png', width=None)
st.sidebar.subheader('Choose your service :bulb:')
nav = st.sidebar.selectbox(" ",['Translate','Medical NER','Sentiment Detection','Text-Speech'])
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.subheader('About')


st.sidebar.write(''' This webapp was developed by Archer Rozario J 3MDS''')
if nav == 'Translate':

    st.subheader("TRANSLATION SERVICE")
    st.image('img/translation-service-image.png', width=None)

    st.subheader("Enter input text")
    sampText = st.text_area('')
    st.subheader('Enter Input Language Code')
    inpLang = st.text_input('')
    st.subheader('Output Language Code')
    outLang = st.text_input(' ')
    client = boto3.client('translate', region_name = "us-east-1")

    trans_button = st.button("Translate")
    if trans_button:
        response = client.translate_text(Text = sampText,
                                            SourceLanguageCode = inpLang,
                                            TargetLanguageCode = outLang)

        output = response['TranslatedText']
        st.write(output)

if nav == "Medical NER":
    st.subheader("Medical NER Service")
    st.image('img/NER.png', width=None)
    client = boto3.client(service_name='comprehendmedical', region_name="us-east-1")
    st.subheader('Enter input text')            
    text1 = st.text_area(" ")
    ner = st.button("Analyze Medical NER")
    if ner:
        result = json.dumps(client.detect_entities(Text= text1, LanguageCode='en'), sort_keys=True, indent=4)
        res = json.loads(result)
        resEntities = res["body"]["Entities"]
        resText = [i['Text'] for i in resEntities]
        resCategories = [i['Category'] for i in resEntities]
        entDict = dict(zip(resText, resCategories))
        st.write(entDict) 
    
    

if nav == "Sentiment Detection":
    st.subheader("SENTIMENT DETECTION")
    st.image('img/sentiment-analysis.png', width=None)
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    st.subheader('Enter text for detection')            
    text = st.text_area(" ")

    analyze = st.button("Analyze Sentiment")
    if analyze:
        resp = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
        resp_dict = json.loads(resp)
        st.subheader("Sentimet")
        st.write(resp_dict['Sentiment'])
        st.subheader("Sentiment Score")
        st.write(resp_dict["SentimentScore"])

if nav == 'Text-Speech':
    st.subheader("Text-Speech")
    st.image('img/t2s.jpg')
    polly = boto3.client(service_name='polly',region_name='us-east-1')
    st.subheader("Enter the text for speech conversion")
    text2=st.text_area(" ")
    audio = st.button("Generate Audio")
    if audio:
        response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',
                    Text=text2)

        file = open('static/audio/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        audio_file = open('static/audio/speech.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    