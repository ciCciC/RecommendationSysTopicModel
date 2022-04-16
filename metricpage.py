import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name = 'Metrics 2021-2022'

file_user_logs = 'data/users_logs.csv'


def app():
    st.title(name)

    # user click behavior
    user_logs = pd.read_csv(file_user_logs)
    grouped = user_logs[['date', 'recom_type']].groupby(['date', 'recom_type']).agg(len)
    grouped = grouped.reset_index().rename(columns={0: 'freq'})
    date_x_recom_matrix = grouped.pivot(index='date', columns='recom_type')
    date_x_recom_matrix.columns = ['diverse', 'hate', 'random', 'similar']

    fig1, ax1 = plt.subplots(figsize=(7, 3))
    ax1.plot(date_x_recom_matrix)
    ax1.set_title('Click behavior over time')
    ax1.legend(date_x_recom_matrix.columns)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # user clicked but not watched
    subset_clicks = user_logs[['date', 'recom_type', 'watched']]
    subset_clicks = subset_clicks[subset_clicks.watched == 0]
    not_watched_grouped = subset_clicks.groupby(['date', 'recom_type']).agg(len)
    not_watched_grouped = not_watched_grouped.reset_index().rename(columns={0: 'freq'})
    date_x_not_watched_matrix = not_watched_grouped.pivot(index='date', columns='recom_type')
    date_x_not_watched_matrix.columns = ['diverse', 'hate', 'random', 'similar']

    fig2, ax2 = plt.subplots(figsize=(7, 3))
    ax2.plot(date_x_not_watched_matrix)
    ax2.set_title('Clicked but not watched over time')
    ax2.legend(date_x_not_watched_matrix.columns)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # user clicked but not watched
    subset_clicks_watch = user_logs[['date', 'recom_type', 'watched']]
    subset_clicks_watch = subset_clicks_watch[subset_clicks_watch.watched == 1]
    watched_grouped = subset_clicks_watch.groupby(['date', 'recom_type']).agg(len)
    watched_grouped = watched_grouped.reset_index().rename(columns={0: 'freq'})
    date_x_watched_matrix = watched_grouped.pivot(index='date', columns='recom_type')
    date_x_watched_matrix.columns = ['diverse', 'hate', 'random', 'similar']

    fig2, ax2 = plt.subplots(figsize=(7, 3))
    ax2.plot(date_x_watched_matrix)
    ax2.set_title('Clicked and watched over time')
    ax2.legend(date_x_watched_matrix.columns)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # user clicked and watch time
    subset_clicks_watchtime = user_logs[['date', 'recom_type', 'watched', 'watch_time']]
    subset_clicks_watchtime = subset_clicks_watchtime[subset_clicks_watchtime.watched == 1]
    subset_clicks_watchtime = subset_clicks_watchtime[['date', 'recom_type', 'watch_time']]
    watchedtime_grouped = subset_clicks_watchtime.groupby(['date', 'recom_type']).agg(np.mean)
    watchedtime_grouped = watchedtime_grouped.reset_index().rename(columns={0: 'freq'})
    date_x_watchedtime_matrix = watchedtime_grouped.pivot(index='date', columns='recom_type')
    date_x_watchedtime_matrix.columns = ['diverse', 'hate', 'random', 'similar']

    fig3, ax3 = plt.subplots(figsize=(7, 3))
    ax3.boxplot(date_x_watchedtime_matrix)
    ax3.set_title('Mean watch time after clicking on content')
    plt.xticks([1,2,3,4], labels=date_x_watchedtime_matrix.columns)
    st.pyplot(fig3)

