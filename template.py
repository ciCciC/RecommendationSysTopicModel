import streamlit as st
from random import random


def select_show(show_id):
    st.session_state['SHOWID'] = show_id

def select_diversity(percentage):
    st.session_state['DIVERSITY'] = int(percentage/10)

def select_category(category):
    st.session_state['category'] = category


def show_episodes(df_episodes):
    L = 10 if len(df_episodes) > 10 else len(df_episodes)
    columns = st.columns(L)

    for idx in range(L):
        df_episode = df_episodes.iloc[idx]
        with columns[idx]:
            tile_item(df_episode)


def show_diversity_buttons():
    columns_buttons = st.columns(4)
    for idx in range(len(columns_buttons)):
        with columns_buttons[idx]:
            percentage = (idx + 2) * 10
            st.button(f'{percentage}%', key=random(), on_click=select_diversity, args=(percentage,))


def show_options(options):
    columns = st.columns(len(options))
    for idx, option in enumerate(options):
        with columns[idx]:
            st.button(option, key=random(), on_click=select_category, args=(option,))


def tile_item(item, state=None, diverse=None):
    title = f'{item["title"] if len(item["title"]) < 30 else item["title"][:30] + "..."}'
    title = title.split(',')[-1] if 'season' in title.lower() else title

    uni_key = item['tv_program_id'] if state else f"{item['tv_program_id']}x{item['season']}x{item['episode_id']}"

    description = item["description"]
    description = description[:int((len(description) / 100) * 20)]
    description = f'{description}...'

    if diverse:
        st.button('😊' if item['diverse'] == 1 else '📺', key=random(), on_click=select_show, args=(uni_key, ))
    else:
        st.button('▶️', key=random(), on_click=select_show, args=(uni_key, ))

    st.image(item['image_url'])
    st.markdown(f"**{title.strip()}**")
    st.caption(description)


def tile_find(item, state=None):
    title = f'{item["title"] if len(item["title"]) < 30 else item["title"][:30] + "..."}'
    description = item["description"]

    description = description[:int((len(description)/100) * 50)]
    description = f'{description}...'

    st.image(item['image_url'])
    st.caption(title)
    st.caption(description)

    uni_key = item['tv_program_id'] if state else f"{item['tv_program_id']}x{item['season']}x{item['episode_id']}"
    st.button('▶️', key=random(), on_click=select_show, args=(uni_key,))


def recommendations(df, diverse=None):
    columns = st.columns(len(df))

    for idx in range(len(df)):
        item = df.iloc[idx]
        with columns[idx]:
            tile_item(item, state=True, diverse=diverse)


def recommendations_content(df):
    columns = st.columns(len(df))

    for idx in range(len(df)):
        item = df.iloc[idx]
        with columns[idx]:
            tile_find(item, state=True)
