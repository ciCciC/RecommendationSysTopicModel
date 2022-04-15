import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

name = 'Metrics'

file_user_logs = 'data/users_logs.csv'


def app():
    st.title(name)

    user_logs = pd.read_csv(file_user_logs)
    grouped = user_logs[['date', 'recom_type']].groupby(['date', 'recom_type']).agg(len)
    grouped = grouped.reset_index().rename(columns={0: 'freq'})
    date_x_recom_matrix = grouped.pivot(index='date', columns='recom_type')
    date_x_recom_matrix.columns = ['diverse', 'hate', 'random', 'similar']

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(date_x_recom_matrix)
    ax.set_title('Click behavior over time')
    ax.legend(date_x_recom_matrix.columns)
    plt.xticks(rotation=45)
    st.pyplot(fig)
