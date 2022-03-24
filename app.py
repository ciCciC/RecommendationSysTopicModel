import streamlit as st
import metricpage, homepage
from routercontroller import RouterController


st.set_page_config(page_title='TVNZ Recommender System', layout="wide")

# Initialize router
app = RouterController()
app.add_page(homepage.name, homepage.app)
app.add_page(metricpage.name, metricpage.app)
app.run()