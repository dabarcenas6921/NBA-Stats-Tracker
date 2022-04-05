import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(
    page_title="NBA Tracker App",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("NBA Stats Tracker 🏀")
df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))


st.table(df)
st.sidebar.header("Options")

add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ['Player Stats', 'Team Stats', 'Season Stats', 'Stadium Locations']
)

if add_selectbox == 'Player Stats':
    st.write("This section displays player information of the NBA.")
    player_searched = st.text_input('Please write a player name')
    player_url = "https://www.balldontlie.io/api/v1/players?search={0}".format(player_searched)
    player_dict = requests.get(player_url).json()
    if not player_dict["data"]:
        st.error("Player does not exist!")
    else:
        st.success('Player found')
        player_info = player_dict["data"][0]
        metric_con = st.checkbox("Convert to Metric System.")
        st.write(player_info)
        st.write('Name: ',player_info["first_name"] + " " + player_info["last_name"])
        if player_info["position"] == "":
            st.write("Position: Retired/Inactive")
        else:
            st.write('Position:', player_info["position"])

        if player_info["height_feet"] is None:
            st.write('Height: N/A')
        elif metric_con:
            height_inches = (player_info["height_feet"]*12) + player_info["height_inches"]
            height_cm = float(height_inches) * 2.54
            st.write("Height : ", height_cm, "cm")
        else:
            st.write("Height : {0}' {1}''".format(player_info["height_feet"], player_info["height_inches"]))
        st.write('Team: ',player_info["team"]["full_name"])
        if metric_con:
            weight_kg = "{:.2f}".format(float(player_info["weight_pounds"]) / 2.205)
            st.write("Weight: ", weight_kg, "kg")
        else:
            st.write("Weight: ", player_info["weight_pounds"], "lbs")

# PROTOTYPE DATAFRAME(below): use dataframe to show several statistics for players
    #df = pd.DataFrame([player_searched, player_dict])
    #st.map(df)

elif add_selectbox == 'Team Stats':
    team_url = "https://www.balldontlie.io/api/v1/teams"
    team_dict = requests.get(team_url).json()
    #st.write(team_dict)

    # Store the list of team IDs
    team_ids = []

    # Get the Team IDs
    for i in team_dict["data"]:
        team_ids.append(i["id"])

    #st.write(team_ids)

    # Store the list of teams
    team_list = []

    for i in team_dict["data"]:
        team_list.append(i["full_name"])
    #st.write(team_list)

    team_list.insert(0,"")

    # Display the team names as a drop down menu
    team_selected = st.selectbox("Select a team", options=team_list)

    # Team ID of selected team
    team_id = None

    # If user selected a team
    if team_selected:
        # Iterate through the team IDs to find each team info
        for i in team_ids:
            ateam_dict = "https://www.balldontlie.io/api/v1/teams/{0}".format(i)
            new = requests.get(ateam_dict).json()

            # Find the ID of the team the user selected
            if new["full_name"] == team_selected:
                st.write("Team ID: ", new["id"])
                st.write("Abbreviation: ", new["abbreviation"])
                st.write("City: ",new["city"])
                st.write("Conference: ",new["conference"])
                st.write("Division: ",new["division"])
                st.write("Full Name: ",new["full_name"])
                st.write("Name: ",new["name"])
                team_id = new["id"]
                break;

        # If the team ID of the selected team is found
        if team_id:
            st.header("Season Stats For " + team_selected)

            #season = 2018

            season = st.text_input('Input a year')

            #df = pd.DataFrame(
            #    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            #    columns=['lat', 'lon'])

            #st.map(df)



            if season:
                st.subheader("Season {0} stats for {1}".format(season, team_selected))

                games = "https://www.balldontlie.io/api/v1/games?seasons[]={0}&team_ids[]={1}".format(season, team_id)
                new = requests.get(games).json()

                if not 'data' in new or len(new['data']) == 0:
                    st.info("N/A")
                else:
                    st.write(new["data"])
                    #st.write(new["data"][0])
elif add_selectbox == 'Stadium Locations':
    # idea -
    map_data = pd.DataFrame(
        np.array([
            [25.775496898, -80.186],
            ]),
        columns=['lat', 'lon'])
    st.map(map_data)

