import streamlit as st
import pandas as pd
import numpy as np
import requests as requests

# miguel was here

# Young Money

st.title("NBA Stats Tracker")

option = st.radio("Please select what data you would like to see:",('Player stats', 'Team Stats'))

if option == 'Player stats':
    player_searched = st.text_input('Please write a player name')
    player_url = "https://www.balldontlie.io/api/v1/players?search={0}".format(player_searched)
    player_dict = requests.get(player_url).json()
    if not player_dict["data"]:
        st.error("Player does not exist!")
    else:
        st.write(player_dict)





