import streamlit as st
import pandas as pd
import numpy as np
import template
import matplotlib.pyplot as plt

name = 'Metrics'

file_tv_programs_and_episodes = './data/tv_programs_and_episodes.csv'


def app():
    st.title(name)

    # df_tv_programs = pd.read_csv(file_tv_programs_and_episodes)

    # grouped_category = df_tv_programs[df_tv_programs.is_season == 0]['category'].value_counts().sort_values()
    # st.caption('Distribution of Categories in TV programs')
    # st.bar_chart(grouped_category)
    #
    # grouped_ratings = df_tv_programs[df_tv_programs.is_season == 1]['rating'].value_counts()
    # st.caption('Distribution of Ratings in episodes')
    # st.bar_chart(grouped_ratings)

    chart_data = pd.DataFrame(
        np.random.randn(10, 2),
        columns=['leftwing content', 'rightwing content'])

    st.line_chart(chart_data)
