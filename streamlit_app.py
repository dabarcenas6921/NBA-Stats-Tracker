import streamlit as st
import pandas as pd
import numpy as np
import requests
from nba_api.stats.static import players

st.set_page_config(
    page_title="NBA Tracker App",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("NBA Stats Tracker 🏀")

st.write("APIs used: [https://www.balldontlie.io](https://www.balldontlie.io) and [https://github.com/swar/nba_api](https://github.com/swar/nba_api)")
# df = pd.DataFrame(
#    np.random.randn(10, 5),
#    columns=('col %d' % i for i in range(5)))


# st.table(df)
st.sidebar.header("Options")

add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ['Player Stats', 'Team Stats', 'Season Stats', 'Stadium Locations']
)

if add_selectbox == 'Player Stats':
    st.write("This section displays information about a player from all seasons.")

    st.warning("Note: Not all players will have their height or weight provided.")

    player_searched = st.text_input('Search for players by their name. (Ex: LeBron James)')

    player_url = "https://www.balldontlie.io/api/v1/players?search={0}".format(player_searched)

    player_dict = requests.get(player_url).json()

    if player_searched:
        # If player name not found
        if not player_dict["data"]:
            st.error("Player does not exist!")
        else:
            st.success('Player found')
            player_info = player_dict["data"][0]
            metric_con = st.checkbox("Convert to Metric System.")
            # st.write(player_info)

            #creating columns to split the info:
            col1, col2 = st.columns(2)

            with col1:
                # Player's full name
                st.write('Name: ', player_info["first_name"] + " " + player_info["last_name"])

                # Player's position
                if player_info["position"] == "":
                    st.write("Position: Retired/Inactive")
                else:
                    st.write('Position:', player_info["position"])

                # Player's height
                if player_info["height_feet"] is None:
                    st.write('Height: N/A')
                elif metric_con:
                    height_inches = (player_info["height_feet"] * 12) + player_info["height_inches"]
                    height_cm = float(height_inches) * 2.54
                    st.write("Height : ", height_cm, "cm")
                else:
                    st.write("Height : {0}' {1}''".format(player_info["height_feet"], player_info["height_inches"]))

                # Player's team
                st.write('Team: ', player_info["team"]["full_name"])

                # Player's weight
                if player_info["weight_pounds"] is None:
                    st.write('Weight: N/A')
                elif metric_con:
                    weight_kg = "{:.2f}".format(float(player_info["weight_pounds"]) / 2.205)
                    st.write("Weight: ", weight_kg, "kg")
                else:
                    st.write("Weight: ", str(player_info["weight_pounds"]), "lbs")

            with col2:
                player_searched_id = players.find_players_by_full_name(player_info["first_name"] + " " + player_info["last_name"])[0]["id"]
                player_image = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{0}.png".format(player_searched_id)
                st.image(player_image, caption="Player headshot")


# PROTOTYPE DATAFRAME(below): use dataframe to show several statistics for players
# df = pd.DataFrame([player_searched, player_dict])
# st.map(df)

elif add_selectbox == 'Team Stats':
    team_url = "https://www.balldontlie.io/api/v1/teams"
    team_dict = requests.get(team_url).json()
    # st.write(team_dict)

    # Store the list of team IDs
    team_ids = []

    # Get the Team IDs
    for i in team_dict["data"]:
        team_ids.append(i["id"])

    # st.write(team_ids)

    # Store the list of teams
    team_list = []

    for i in team_dict["data"]:
        team_list.append(i["full_name"])
    # st.write(team_list)

    team_list.insert(0, "")

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
                st.write("City: ", new["city"])
                st.write("Conference: ", new["conference"])
                st.write("Division: ", new["division"])
                st.write("Full Name: ", new["full_name"])
                st.write("Name: ", new["name"])
                team_id = new["id"]
                break;

        # If the team ID of the selected team is found
        if team_id:
            st.header("Season Stats For " + team_selected)

            # season = 2018

            season = st.text_input('Input a year')

            # df = pd.DataFrame(
            #    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            #    columns=['lat', 'lon'])

            # st.map(df)

            if season:
                st.subheader("Season {0} stats for {1}".format(season, team_selected))

                games = "https://www.balldontlie.io/api/v1/games?seasons[]={0}&team_ids[]={1}".format(season, team_id)
                new = requests.get(games).json()

                if not 'data' in new or len(new['data']) == 0:
                    st.info("N/A")
                else:
                    st.write(new["data"])
                    # st.write(new["data"][0])
elif add_selectbox == 'Stadium Locations':
    st.subheader("NBA Stadium Locations")
    st.write("A map displaying the stadium Locations for all 30 NBA teams.")
    map_data = pd.DataFrame(
        np.array([
            [33.7573, -84.3963],  # Atlanta Hawks - State Farm Arena
            [42.3662, -71.0621],  # Boston Celtics - TD Garden
            [40.6826, -73.9754],  # Brooklyn Nets - Barclays Center
            [35.2251, -80.8392],  # Charlotte Hornets - Spectrum Center
            [41.8807, -87.6742],  # Chicago Bulls - United Center
            [41.4967, -81.6885],  # Cleveland Cavaliers - Rocket Mortgage FieldHouse
            [32.7905, -96.8103],  # Dallas Mavericks - American Airlines Center
            [39.7486, -105.0075],  # Denver Nuggets - Ball Arena
            [42.3409, -83.0552],  # Detroit Pistons - Little Caesars Arena
            [37.7679, -122.3874],  # Golden State Warriors - Chase Center
            [29.7507, -95.3622],  # Houston Rockets - Toyota Center
            [39.7641, -86.1555],  # Indiana Pacers - Gainbridge Fieldhouse
            [34.043, -118.2668],  # LA Clippers - Crypto.com Arena
            [34.043, -118.2668],  # Los Angeles lakers - Crypto.com Arena
            [35.1382, -90.0507],  # Memphis Grizzlies - FedExForum
            [25.78136, -80.18794],  # Miami Heat - America Airlines
            [43.0451, -87.9172],  # Milwaukee Bucks - Fiserv Forum
            [44.9795, -93.2761],  # Minnesota Timberwolves - Target Center
            [29.9490, -90.0821],  # New Orleans Pelicans - Smoothie King Center
            [40.7505, -73.9934],  # New York Knicks - Madison Square Garden
            [35.4634, -97.5151],  # Oklahoma City Thunder - Paycom Center
            [28.5392, -81.3839],  # Orlando Magic - Amway Center
            [39.9012, -75.1720],  # Philadelphia 76ers - Wells Fargo Center
            [33.4457, -112.0712],  # Phoenix Suns - Footprint Center
            [45.5316, -122.6668],  # Portland Trail Blazers - Moda Center
            [38.5802, -121.4997],  # Sacramento Kings - Golden 1 Center
            [29.4270, -98.4375],  # San Antonio Spurs - AT&T Center
            [43.6435, -79.3791],  # Toronto Raptors - Scotiabank Arena
            [40.7683, -111.9011],  # Utah Jazz - Vivint Arena
            [38.8982, -77.0209]  # Washington Wizards - Capital One Arena
        ]),
        columns=['lat', 'lon'])
    st.map(map_data, zoom=3)