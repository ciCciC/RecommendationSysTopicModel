import streamlit as st
import pandas as pd
import numpy as np
import template

name = 'Home'

file_episodes = './data/episodes.csv'


def app():

    # load the dataset with the books
    df_episodes = pd.read_csv(file_episodes)

    st.image(df_episodes.image_dump.iloc[0])
