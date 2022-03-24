import streamlit as st
from random import random


def select_show(show_id):
    st.session_state['SHOWID'] = show_id


def select_category(category):
    st.session_state['category'] = category


def show_episodes(df_show):
    L = 10
    columns = st.columns(L)

    df_show['diverse'] = 0

    for idx in range(L):
        with columns[idx]:
            tile_item(df_show, f'Episode {idx + 1}')


def show_options(options):
    columns = st.columns(len(options))
    for idx, option in enumerate(options):
        with columns[idx]:
            st.button(option, key=random(), on_click=select_category, args=(option,))


def tile_item(item, global_text=None):
    st.button('😊' if item['diverse'] == 1 else '📺', key=random(), on_click=select_show, args=(item['show_id'],))

    st.image(item['image_url'], use_column_width=True)
    broadcast_name = f'{item["broadcast_name"]}'.upper()

    if global_text is None:
        title = f'{item["title"] if len(item["title"]) < 30 else item["title"][:30] + "..."}'
        st.text(broadcast_name)
        st.caption(title)
    else:
        st.caption(global_text)  # <-- for rendering episodes


def recommendations(df):
    columns = st.columns(len(df))

    for idx in range(len(df)):
        item = df.iloc[idx]
        with columns[idx]:
            tile_item(item)
