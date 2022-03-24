import streamlit as st


class RouterController:
    # Creates a router for changing from page

    def __init__(self):
        self.pages = []

    # store page and related app() function
    def add_page(self, title, func) -> None:
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        # initiate function app() based on selection
        page = st.sidebar.selectbox(
            'Navigation',
            self.pages,
            format_func=lambda page: page['title']
        )

        page['function']()
