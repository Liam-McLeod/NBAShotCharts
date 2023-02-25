import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

def drawCourt():
    
    # Get Current Axis
    ax = plt.gca()

    # Line Color and Width
    color = "black"
    lw = 2

    # Basketball Hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # outer box
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # inner box
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

    # Free Bottom Top Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color,linestyle='dashed')

    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # Outer Lines
    outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)

    # list of court shapes
    court_elements = [hoop, backboard, outer_box, inner_box, 
                      top_free_throw, bottom_free_throw, restricted, 
                      corner_three_a, corner_three_b, three_arc, 
                      center_outer_arc, center_inner_arc,outer_lines]

    # Drawing Court Shapes
    for element in court_elements:
        ax.add_patch(element)

def getPlayerID(playerDict,playerName):
    playerName = playerName.strip()
    for player in playerDict:
        if player['full_name'].lower() == playerName.lower():
            return player['id']
    return -1

def getData():

    #Load Player Dict
    playerDict = players.get_players()
    # Get Player ID from playerName
    player_id = getPlayerID(playerDict,playerName)
    # Check if Player Found
    if player_id == -1:
        st.error('No Player Found', icon="🚨")
        return
    # Player Career DF
    careerData = playercareerstats.PlayerCareerStats(player_id)
    career_df = careerData.get_data_frames()[0]
    # Season ID 
    season_id = seasonInput
    # TEAM ID during Season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']

    # Get shot data from Player id, Team id and Season id
    try:
        shotchartData = shotchartdetail.ShotChartDetail(team_id,player_id,season_type_all_star='Regular Season',season_nullable=season_id,context_measure_simple='FGA')
    # Data not found (Invalid Season)
    except ValueError:
        st.error('No Data Found (Check Season Input)', icon="🚨")
        return

    shotchart_df = shotchartData.get_data_frames()[0]
    


    # Figure
    fig = plt.figure(figsize=(12,11))

    # Scatter Plot
    if plotType == "Scatter Plot":
        # Separate Made and Missed Shots
        x_missed = shotchart_df[shotchart_df['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
        y_missed = shotchart_df[shotchart_df['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

        x_made = shotchart_df[shotchart_df['EVENT_TYPE'] == 'Made Shot']['LOC_X']
        y_made = shotchart_df[shotchart_df['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

        # Plot Missed Shots
        plt.scatter(x_missed, y_missed, c='r', marker="x", s=300, linewidths=3)
        # Plot Made Shots
        plt.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker='o', s=100, linewidths=3)

    # Heat Map
    if plotType == "Heat Map":
        sns.kdeplot(x=shotchart_df.LOC_X,y=shotchart_df.LOC_Y,fill=True,cmap='YlOrRd_r',levels=50)

    # HexBin
    if plotType == "HexBin":
        plt.hexbin(x=shotchart_df.LOC_X,y=shotchart_df.LOC_Y,cmap='gist_heat_r',gridsize=25)

    # Draw Court
    drawCourt()
    # Adjust plot limits, remove ticks and labels
    plt.xlim(-250,250)
    plt.ylim(422.5, -47.5)
    plt.xlabel('')
    plt.ylabel('')
    plt.tick_params(axis='both', left=False, bottom=False, labelleft=False, labelbottom=False)
    # Title of Plot
    plt.title(playerName.upper() + " " + season_id,fontsize=18)
    # Plot Figure to Streamlit
    st.pyplot(fig)

# WEB PAGE

st.title("NBA Shot Charts")

st.subheader("Enter the name of an NBA player and a season to generate a shot chart")

plotType = st.selectbox(
    'Plot Type',
    ('Scatter Plot', 'Heat Map', "HexBin"))

playerName = st.text_input('Player name (Eg. LeBron James) or Team name (Eg. Miami Heat)')

seasonInput = st.text_input('Season (Eg. 2013-14)')

button = st.button('Add',on_click=getData)