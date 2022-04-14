import streamlit as st
import pandas as pd
import numpy as np
import template
from random import random

name = 'Home'

file_tv_programs_and_episodes = './data/sample_tv_programs_and_episodes.csv'


def app():

    df_tv_programs = pd.read_csv(file_tv_programs_and_episodes)

    if 'SHOWID' not in st.session_state:
        st.session_state['SHOWID'] = 311

    if 'SEASON_ID' not in st.session_state:
        st.session_state['SEASON_ID'] = 1

    df_chosen = ''
    df_content = ''

    if 'x' in str(st.session_state['SHOWID']):
        splitted = st.session_state['SHOWID'].split('x')
        tv_program_id = int(splitted[0])
        season = int(splitted[1])
        episode_id = int(splitted[2])

        df_chosen = df_tv_programs[(df_tv_programs['tv_program_id'] == tv_program_id) & (df_tv_programs['season'] == season)]
        df_content = df_chosen[df_chosen['episode_id'] == episode_id].iloc[0]
        st.session_state['SHOWID'] = tv_program_id
        st.session_state['SEASON_ID'] = season
    else:
        df_chosen = df_tv_programs[(df_tv_programs['tv_program_id'] == st.session_state['SHOWID'])]
        df_content = df_chosen[df_chosen['is_season'] == 0].iloc[0]
        st.session_state['SEASON_ID'] = df_chosen[df_chosen['is_season'] == 1].season.unique()[0]

    cover, info = st.columns([2, 3])

    with cover:
        st.image(df_content['image_url'])

    with info:
        st.title(df_content['title'])
        st.markdown(df_content['description'])
        st.caption(df_content['category'].upper())

    likes = st.columns(20)
    with likes[0]:
        st.button('❤️', key=random())
    with likes[1]:
        st.button('💔', key=random())

    df_episodes = ''
    c3 = st.columns(4)
    with c3[0]:

        selectables = df_chosen[df_chosen['is_season'] == 1].season.unique()
        pre_select = np.where(selectables == st.session_state['SEASON_ID'])[0][0]

        season_choice = st.selectbox('Season', selectables, index=int(pre_select))
        df_episodes = df_tv_programs[
            (df_tv_programs['tv_program_id'] == st.session_state['SHOWID']) & (df_tv_programs['season'] == season_choice)].sort_values(
            by='episode_id', ascending=False)

    template.show_episodes(df_episodes)

    st.title("Similarity - Diversity")

    columns_buttons = st.columns(4)
    for idx in range(len(columns_buttons)):
        with columns_buttons[idx]:
            st.button(f'asdasd {(idx + 1) * 10}%')

    st.title("Something U HATE!")
    st.title("Random user")
