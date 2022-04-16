import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import requests
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

st.set_page_config(
    page_title="NBA Tracker App",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("NBA Stats Tracker 🏀")

st.write("APIs used: [https://www.balldontlie.io]"
         "(https://www.balldontlie.io) and [https://"
         "github.com/swar/nba_api](https://github.com/swar/nba_api)")

st.sidebar.header("Options")

add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ['Player Stats', 'Team Stats', 'Stadium Locations']
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
            player_searched_id = \
            players.find_players_by_full_name(player_info["first_name"] + " " + player_info["last_name"])[0]["id"]
            metric_con = st.checkbox("Convert to Metric System.")
            # st.write(player_info)

            # creating columns to split the info:
            col1, col2 = st.columns(2)

            with col1:
                # Player's full name
                st.subheader(player_info["first_name"] + " " + player_info["last_name"])

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
                    st.write("Height : ", str(height_cm), "cm")
                else:
                    st.write("Height : {0}' {1}''".format(player_info["height_feet"], player_info["height_inches"]))

                # Player's team
                st.write('Team: ', player_info["team"]["full_name"])

                # Player's weight
                if player_info["weight_pounds"] is None:
                    st.write('Weight: N/A')
                elif metric_con:
                    weight_kg = "{:.2f}".format(float(player_info["weight_pounds"]) / 2.205)
                    st.write("Weight: ", str(weight_kg), "kg")
                else:
                    st.write("Weight: ", str(player_info["weight_pounds"]), "lbs")

                # Player's headline stats
                # getting player headline stats such as ppg, rpg, and apg through nba_api
                selected_player_headline_dict = commonplayerinfo.CommonPlayerInfo(
                    player_id=player_searched_id).player_headline_stats.get_dict()
                PPG = selected_player_headline_dict["data"][0][3]
                RPG = selected_player_headline_dict["data"][0][4]
                APG = selected_player_headline_dict["data"][0][5]
                st.write("PPG: " + str(PPG))
                st.write("RPG: " + str(RPG))
                st.write("APG: " + str(APG))

            with col2:
                # using nba_api to get right player id and then the player headshot image
                player_image = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{0}.png".format(
                    player_searched_id)
                st.image(player_image, caption="Player headshot")

            player_searched2 = st.text_input('If you want to compare, search for second player by their name.')
            player_url_2 = "https://www.balldontlie.io/api/v1/players?search={0}".format(player_searched2)
            player_dict2 = requests.get(player_url_2).json()
            if player_searched2:
                # If player name not found
                if not player_dict2["data"]:
                    st.error("Player does not exist!")
                else:
                    st.success('Player found')
                    player_info2 = player_dict2["data"][0]
                    player_searched_id2 = \
                        players.find_players_by_full_name(
                            player_info2["first_name"] + " " + player_info2["last_name"])[0]["id"]

                    # creating columns to split the info:
                    col1, col2 = st.columns(2)

                    with col1:
                        # Player's full name
                        st.subheader(player_info2["first_name"] + " " + player_info2["last_name"])

                        # Player's position
                        if player_info2["position"] == "":
                            st.write("Position: Retired/Inactive")
                        else:
                            st.write('Position:', player_info["position"])

                        # Player's height
                        if player_info2["height_feet"] is None:
                            st.write('Height: N/A')
                        elif metric_con:
                            height_inches2 = (player_info2["height_feet"] * 12) + player_info2["height_inches"]
                            height_cm2 = float(height_inches2) * 2.54
                            st.write("Height : ", str(height_cm2), "cm")
                        else:
                            st.write("Height : {0}' {1}''".format(player_info2["height_feet"],
                                                                  player_info2["height_inches"]))

                        # Player's team
                        st.write('Team: ', player_info2["team"]["full_name"])

                        # Player's weight
                        if player_info2["weight_pounds"] is None:
                            st.write('Weight: N/A')
                        elif metric_con:
                            weight_kg2 = "{:.2f}".format(float(player_info2["weight_pounds"]) / 2.205)
                            st.write("Weight: ", str(weight_kg2), "kg")
                        else:
                            st.write("Weight: ", str(player_info2["weight_pounds"]), "lbs")

                        # Player's headline stats
                        # getting player headline stats such as ppg, rpg, and apg through nba_api
                        selected_player_headline_dict2 = commonplayerinfo.CommonPlayerInfo(
                            player_id=player_searched_id2).player_headline_stats.get_dict()
                        PPG2 = selected_player_headline_dict2["data"][0][3]
                        RPG2 = selected_player_headline_dict2["data"][0][4]
                        APG2 = selected_player_headline_dict2["data"][0][5]
                        st.write("PPG: " + str(PPG2))
                        st.write("RPG: " + str(RPG2))
                        st.write("APG: " + str(APG2))

                    with col2:
                        # using nba_api to get right player id and then the player headshot image
                        player_image2 = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{0}.png".format(
                            player_searched_id2)
                        st.image(player_image2, caption="Player headshot")

                    compare_button = st.button('Compare with a bar chart?')

                    if compare_button:
                        player1 = player_info["first_name"] + " " + player_info["last_name"]
                        player2 = player_info2["first_name"] + " " + player_info2["last_name"]
                        player1_stats = [PPG,RPG,APG]
                        player2_stats = [PPG2,RPG2,APG2]
                        compare_players = pd.DataFrame({
                                "Point Categories": ['PPG', 'RPG', 'APG'],
                                player1: player1_stats,
                                player2: player2_stats
                        })


                        altair_chart_players = alt.Chart(compare_players)\
                            .transform_fold([player1, player2], as_=["key", "value"])\
                            .mark_bar()\
                            .encode(
                                    alt.X("key:N", axis=None),
                                    alt.Y("value:Q"),
                                    alt.Color("key:N", legend=alt.Legend(title=None, orient='bottom')),
                                    alt.Column("Point Categories",
                                               sort=['PPG', 'RPG' 'APG'],
                                               header=alt.Header(labelOrient="top", title=None)
                                    )
                                )

                        st.altair_chart(altair_chart_players)

elif add_selectbox == 'Team Stats':
    team_url = "https://www.balldontlie.io/api/v1/teams"
    team_dict = requests.get(team_url).json()
    #st.write(team_dict)

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
                st.write("Team ID: ", str(new["id"]))
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

            season = st.number_input('Input a year', step=1, min_value=1979, max_value=2021, value=2021)

            if season:
                st.subheader("Season {0} stats for {1}".format(season, team_selected))

                games = "https://www.balldontlie.io/api/v1/games?seasons[]={0}&team_ids[]={1}&per_page=100".format(season, team_id)
                new = requests.get(games).json()


                if not 'data' in new or len(new['data']) == 0:
                    st.info("N/A")
                else:
                    # st.write(new["data"])

                    # All the searched team's scores
                    team_scores = []

                    other_team_scores = []

                    # Get the scores for both teams
                    for i in range(len(new["data"])):
                        if new["data"][i]["home_team"]["id"] == team_id:
                            team_scores.append(new["data"][i]["home_team_score"])
                        elif new["data"][i]["visitor_team"]["id"] == team_id:
                            team_scores.append(new["data"][i]["visitor_team_score"])

                    for i in range(len(new["data"])):
                        if new["data"][i]["home_team"]["id"] == team_id:
                            other_team_scores.append(new["data"][i]["visitor_team_score"])
                        elif new["data"][i]["visitor_team"]["id"] == team_id:
                            other_team_scores.append(new["data"][i]["home_team_score"])


                    team_scores_table = pd.DataFrame(
                        {
                            team_selected + "'s Score:": team_scores,
                            "Opposing Team's Scores": other_team_scores
                        }
                    )

                    team_scores_table_NO_OPPOSING = pd.DataFrame(
                        {
                            team_selected + "'s Score:": team_scores
                        }
                    )

                    team_scores_table_ONLY_OPPOSING = pd.DataFrame(
                        {
                            "Opposing Team's Scores": other_team_scores
                        }
                    )

                    #st.dataframe(team_scores_table, height=500)

                    option = st.radio("Please select what line chart information you would like to see:",
                                            [team_selected + "'s Scores", "Opposing Team's Scores",
                                             "Scores for both teams"])
                    if option == "Opposing Team's Scores":
                        st.line_chart(team_scores_table_ONLY_OPPOSING, height=500)
                    elif option == "Scores for both teams":
                        st.line_chart(team_scores_table, height=500)
                    else:
                        st.line_chart(team_scores_table_NO_OPPOSING, height=500)

            st.title("Season Score Comparison")
            yob = st.slider("Select a Season", 1979, 2021)
            st.write("You selected {}".format(yob))
            if yob:
                     st.subheader("Season {0} stats for {1}".format(yob, team_selected))
            games = "https://www.balldontlie.io/api/v1/games?seasons[]={0}&team_ids[]={1}&per_page=100".format(
                            yob, team_id)
            new = requests.get(games).json()

            if not 'data' in new or len(new['data']) == 0:
                st.info("N/A")
            else:
                            # st.write(new["data"])

                            # All the searched team's scores
                        team_scores = []

                        other_team_scores = []

                            # Get the scores for both teams
                        for i in range(len(new["data"])):
                            if new["data"][i]["home_team"]["id"] == team_id:
                                team_scores.append(new["data"][i]["home_team_score"])
                            elif new["data"][i]["visitor_team"]["id"] == team_id:
                                team_scores.append(new["data"][i]["visitor_team_score"])

                        for i in range(len(new["data"])):
                            if new["data"][i]["home_team"]["id"] == team_id:
                                other_team_scores.append(new["data"][i]["visitor_team_score"])
                            elif new["data"][i]["visitor_team"]["id"] == team_id:
                                other_team_scores.append(new["data"][i]["home_team_score"])

                        slider_scores_table = pd.DataFrame(
                            {
                                team_selected + "'s Score:": team_scores,
                                "Opposing Team's Scores": other_team_scores
                            }
                        )
                        slider_scores_table_NO_OPPOSING = pd.DataFrame(
                            {
                                team_selected + "'s Score:": team_scores
                            }
                        )

                        slider_scores_table_ONLY_OPPOSING = pd.DataFrame(
                            {
                                "Opposing Team's Scores": other_team_scores
                            }
                        )

                        select = st.radio("Please select what information you would like to compare:",
                                          [team_selected + "'s Scores", "Opposing Team's Scores",
                                           "Scores for both teams"])
                        if select == "Opposing Team's Scores":
                            st.line_chart(slider_scores_table_ONLY_OPPOSING, height=500)
                        elif select == "Scores for both teams":
                            st.line_chart(slider_scores_table, height=500)
                        else:
                            st.line_chart(slider_scores_table_NO_OPPOSING, height=500)

                        #st.line_chart(slider_scores_table, height=500)




elif add_selectbox == 'Stadium Locations':
    st.subheader("NBA Stadium Locations")

    col1, col2 = st.columns(2)

    # Populating each column
    with col1:
        # creating a dataframe for the geological periods
        geological_periods = pd.DataFrame(
            {
                "Team Name": ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
                              "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
                              "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
                              "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks",
                              "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
                              "Oklahoma City Thunder",
                              "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
                              "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz",
                              "Washington Wizards"],

                "Arena Name": ["State Farm Arena", "TD Garden", "Barclays Center", "Spectrum Center", "United Center",
                               "Rocket Mortgage FieldHouse", "American Airlines Center", "Ball Arena",
                               "Little Caesars Arena",
                               "Chase Center", "Toyota Center", "Gainbridge Fieldhouse", "Crypto.com Arena",
                               "Crypto.com Arena",
                               "FedExForum", "America Airlines", "Fiserv Forum", "Target Center",
                               "Smoothie King Center",
                               "Madison Square Garden", "Paycom Center", "Amway Center", "Wells Fargo Center",
                               "Footprint Center", "Moda Center", "Golden 1 Center", "AT&T Center", "Scotiabank Arena",
                               "Vivint Arena", "Capital One Arena"],

                "Arena Location": ["Atlanta, Georgia", "Boston, Massachusetts", "Brooklyn, New York",
                                   "Charlotte, North Carolina", "Chicago, Illinois", "Cleveland, Ohio", "Dallas, Texas",
                                   "Denver, Colorado", "Detroit, Michigan", "San Francisco, California",
                                   "Houston, Texas",
                                   "Indianapolis, Indiana", "Los Angeles, California", "Los Angeles, California",
                                   "Memphis, Tennessee", "Miami, Florida", "Milwaukee, Wisconsin",
                                   "Minneapolis, Minnesota", "New Orleans, Louisiana", "New York City, New York",
                                   "Oklahoma City, Oklahoma", "Orlando, Florida", "Philadelphia, Pennsylvania",
                                   "Phoenix, Arizona", "Portland, Oregon", "Sacramento, California",
                                   "San Antonio, Texas",
                                   "Toronto, Ontario", "Salt Lake City, Utah", "Washington, D.C."]
            }
        )
        # Displaying the dataframe
        st.dataframe(geological_periods, height=500)

    with col2:
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
        st.map(map_data)
        st.caption("A map displaying the stadium Locations for all 30 NBA teams.")