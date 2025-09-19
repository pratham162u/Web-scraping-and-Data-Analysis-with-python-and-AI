import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

def plot_sentiment(score):
    fig, ax = plt.subplots()
    ax.bar(["Sentiment"], [score], color='skyblue')
    ax.set_ylim(-1, 1)
    st.pyplot(fig)

def display_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)