import streamlit as st
import pandas as pd
import numpy as np
import template
from random import random

name = 'Home'

file_tv_programs_and_episodes = './data/tv_programs_and_episodes.csv'
file_recommendation_cosine = './data/recommendation_cosine_similarity.csv'
file_user_favorites = './data/user_x_tvprogram_favorites.csv'
file_user_dislikes = './data/user_x_tvprogram_dislikes.csv'

current_user_id = 2

def app():
    df_user_x_favorite = pd.read_csv(file_user_favorites)
    df_user_x_dislikes = pd.read_csv(file_user_dislikes)
    df_recommendation_cosine = pd.read_csv(file_recommendation_cosine)
    df_tv_programs = pd.read_csv(file_tv_programs_and_episodes)

    if 'SHOWID' not in st.session_state:
        st.session_state['SHOWID'] = 311

    if 'SEASON_ID' not in st.session_state:
        st.session_state['SEASON_ID'] = 1

    if 'DIVERSITY' not in st.session_state:
        st.session_state['DIVERSITY'] = 5

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

    st.title("Similarity - diversity")
    template.show_diversity_buttons()

    similarity(df_tv_programs, df_recommendation_cosine)

    st.title("You might also like")
    might_like(df_user_x_favorite, df_recommendation_cosine, df_tv_programs)

    st.title("Want to reconsider these again?")
    something_hate(df_user_x_dislikes, df_user_x_favorite, df_recommendation_cosine, df_tv_programs)

    st.title("See what others are watching")
    recommend_random_user(df_user_x_favorite, df_recommendation_cosine, df_tv_programs)


def similarity(df_tv_programs, df_recommendation_cosine):
    similar_tv_ids = df_recommendation_cosine[df_recommendation_cosine.tv_show_idx == st.session_state['SHOWID']].sort_values(by='score', ascending=False).head(10)

    df_tv_programs = df_tv_programs[df_tv_programs.is_season == 0]

    similarity = df_tv_programs.tv_program_id.isin(similar_tv_ids.tv_show_idy)
    similar_content = df_tv_programs[similarity]

    similar_content = similar_content[:10-st.session_state['DIVERSITY']]
    similar_content['diverse'] = 0

    dissimilar_content = df_tv_programs[~similarity].sample(10)
    dissimilar_content = dissimilar_content[:st.session_state['DIVERSITY']]
    dissimilar_content['diverse'] = 1

    df_to_display = pd.concat([similar_content, dissimilar_content])

    template.recommendations(df_to_display, diverse=True)


def might_like(df_user_x_favorite, df_recommendation_cosine, df_tv_programs):
    df_favorites = df_user_x_favorite.iloc[current_user_id]
    likes = df_favorites[df_favorites == 1].index.astype(int)
    similar_tv_ids = df_recommendation_cosine[df_recommendation_cosine.tv_show_idx.isin(likes)].sort_values(by='score', ascending=False).head(10)

    df_tv_programs = df_tv_programs[df_tv_programs.is_season == 0]

    similarity = df_tv_programs.tv_program_id.isin(similar_tv_ids.tv_show_idy)
    similar_content = df_tv_programs[similarity]

    also_liked = list(df_tv_programs[df_tv_programs.tv_program_id.isin(likes)].title)

    st.caption(f"Because you liked '{', '.join(also_liked[:5])}'")

    template.recommendations(similar_content)


def something_hate(df_user_x_dislikes, df_user_x_likes, df_recommendation_cosine, df_tv_programs):
    df_dislikes = df_user_x_dislikes.iloc[current_user_id]
    df_likes = df_user_x_likes.iloc[current_user_id]

    dislikes = df_dislikes[df_dislikes == -1].index.astype(int)
    likes = df_likes[df_likes == 1].index.astype(int)

    similar_tv_ids = df_recommendation_cosine[df_recommendation_cosine.tv_show_idx.isin(dislikes)].sort_values(by='score',
                                                                                                            ascending=False)

    similar_tv_ids = similar_tv_ids[~df_recommendation_cosine.tv_show_idx.isin(likes)].head(10)

    df_tv_programs = df_tv_programs[df_tv_programs.is_season == 0]

    similarity = df_tv_programs.tv_program_id.isin(similar_tv_ids.tv_show_idy)
    similar_content = df_tv_programs[similarity]

    template.recommendations(similar_content)


def recommend_random_user(df_user_x_favorite, df_recommendation_cosine, df_tv_programs):
    random_user = df_user_x_favorite.sample(10)
    random_user = random_user[~random_user.index.isin([0,1,current_user_id])].iloc[0]

    likes = random_user[random_user == 1].index.astype(int)

    similar_tv_ids = df_recommendation_cosine[df_recommendation_cosine.tv_show_idx.isin(likes)].sort_values(by='score',
                                                                                                            ascending=False).head(
        10)

    df_tv_programs = df_tv_programs[df_tv_programs.is_season == 0]

    similarity = df_tv_programs.tv_program_id.isin(similar_tv_ids.tv_show_idy)
    similar_content = df_tv_programs[similarity]

    template.recommendations(similar_content)