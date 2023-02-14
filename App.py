import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.static import players
from nba_api.stats.static import teams

st.write(""" # NBA Stats """)

st.info('Seperate Up to four players, OR two teams with a comma', icon="ℹ️")

option1 = st.selectbox('Label',('Player','Team'),label_visibility="collapsed")

option2 = st.selectbox('Label',('Regular Season','Post Season'),label_visibility="collapsed")

stat_input = st.selectbox('Label',('PTS', 'REB', 'AST', 'STL','BLK'),label_visibility="collapsed")

format = st.selectbox('Label',('Line Graph','Bar Graph','Table'),label_visibility="collapsed")

user_input = st.text_input('Label',label_visibility='collapsed')

button = st.button('Add',on_click=getData)