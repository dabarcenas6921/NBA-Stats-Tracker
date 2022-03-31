import streamlit as st
import pandas as pd
import numpy as np
import requests as requests

st.title("NBA Stats Tracker")

option = st.radio("Please select what data you would like to see:",("Player stats", "Team Stats"))