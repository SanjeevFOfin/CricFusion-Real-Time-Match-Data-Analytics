import streamlit as st
import pandas as pd
import mysql.connector

# Database connection config
DB_KWARGS = dict(
    host="localhost",
    user="root",
    password="blacky1996",
    database="Cricbuzz"
)

# Define run_query function
@st.cache_data
def run_query(query, params=None):
    try:
        conn = mysql.connector.connect(**DB_KWARGS)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        conn.close()
        return pd.DataFrame(result)
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


# Page config
st.set_page_config(page_title="SQL_Queries", layout="wide")

import streamlit as st

def app():
    st.title("Top SQL Stats Page")
    st.write("Analyze top SQL stats here.")


# Cricket-themed background CSS
page_bg_img = """
<style>
.stApp {
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3e27JXBz4kaDoSoQcXXILSOYuj3SzuP4ePA&s");
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .css-18e3th9 {  
        display: flex;
        justify-content: center;
    }
    .main-container {
        max-width: 1200px;
        width: 100%;
        margin: auto;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .css-10trblm {  
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏏 CricFusion – Real-Time Match Data Analytics")

# === Raw Dataset Viewer Dropdown ===
st.header("📊 Raw Dataset Viewer")
raw_dataset = st.selectbox(
    "Select Dataset to View",
    ["Match Summaries", "Batsman Data", "Bowler Data", "Player Descriptions"]
)

if st.button("View Dataset"):
    if raw_dataset == "Match Summaries":
        query = "SELECT * FROM match_summaries;"
    elif raw_dataset == "Batsman Data":
        query = "SELECT * FROM batsman_data;"
    elif raw_dataset == "Bowler Data":
        query = "SELECT * FROM bowler_data;"
    else:
        query = "SELECT * FROM player_descriptions;"

    df = run_query(query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data found or database connection issue.")

# === Structured Analysis Questions Below ===

# Q1
st.header("Q1: Find all players who represent India.")
st.write("Display their full name, playing role, batting style, and bowling style.")
if st.button("Run Q1"):
    query = """
        SELECT DISTINCT pd.player_id, pd.player_name, pd.description
        FROM player_descriptions pd
        LEFT JOIN batsman_data bd ON pd.player_id = bd.player_id
        WHERE bd.team_name = 'India' OR bd.team_name IS NULL;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q2
st.header("Q2: Show all matches played in the last 30 days.")
st.write("Include match description, team names, venue name, city, group, and match date.")
if st.button("Run Q2"):
    query = """
        SELECT description, team1, team2, venue AS venue_name, city, group_name, Date AS match_date
        FROM match_summaries
        WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        ORDER BY Date DESC;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q3
st.header("Q3: Calculate how many matches each team has won.")
st.write("Show team name and total number of wins in descending order.")
if st.button("Run Q3"):
    query = """
        SELECT winner AS team_name, 
               CASE WHEN winner = team1 THEN team2 ELSE team1 END AS opponent_team,
               COUNT(matchId) AS total_wins
        FROM match_summaries
        GROUP BY winner, opponent_team
        ORDER BY total_wins DESC;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q4
st.header("Q4: Find the highest individual batting score achieved in Asia Cup 2025.")
if st.button("Run Q4"):
    query = """
        SELECT team_name, player_name, runs, balls, fours, sixes, strike_rate
        FROM batsman_data
        WHERE runs = (SELECT MAX(runs) FROM batsman_data);
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q5
st.header("Q5: Details of last 20 completed matches.")
st.write("Show description, teams, winner, victory margin/type, and date.")
if st.button("Run Q5"):
    query = """
        SELECT description, team1, team2, winner, 
               CASE WHEN win_by_runs = 'TRUE' THEN margin ELSE margin END AS victory_margin,
               CASE WHEN win_by_runs = 'TRUE' THEN 'Runs' ELSE 'Wickets' END AS victory_type,
               Date
        FROM match_summaries
        ORDER BY Date DESC
        LIMIT 20;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q6
st.header("Q6: Bowling performance at different venues.")
st.write("Calculate average economy and total wickets by team and venue.")
if st.button("Run Q6"):
    query = """
        SELECT 
            bd.team_name, 
            ms.venue AS venue_name,
            ms.group_name,
            COUNT(DISTINCT ms.matchId) AS matches_played,
            AVG(bd.economy) AS avg_economy,
            SUM(bd.wickets) AS total_wickets
        FROM bowler_data bd
        JOIN match_summaries ms ON bd.matchId = ms.matchId
        GROUP BY bd.team_name, ms.venue, ms.group_name
        HAVING COUNT(DISTINCT ms.matchId) >= 1
        ORDER BY bd.team_name, ms.venue, ms.group_name;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q7
st.header("Q7: Bowler status based on performance.")
st.write("Show top 10 bowlers by wickets, with matches played, overs bowled, and economy.")
if st.button("Run Q7"):
    query = """
        SELECT 
            player_name,
            team_name,
            COUNT(DISTINCT matchId) AS matches_played,
            SUM(overs) AS total_overs_bowled,
            SUM(wickets) AS total_wickets,
            AVG(economy) AS avg_economy
        FROM bowler_data
        GROUP BY player_name, team_name
        HAVING COUNT(DISTINCT matchId) >= 1
        ORDER BY total_wickets DESC
        LIMIT 10;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q8
st.header("Q8: Investigate toss advantage.")
st.write("What % of matches are won by the team that wins the toss?")
if st.button("Run Q8"):
    query = """
        SELECT toss_winner, toss_decision, 
               SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS matches_won_after_toss,
               COUNT(matchId) AS total_matches,
               ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(matchId) * 100, 2) AS win_percentage
        FROM match_summaries
        GROUP BY toss_winner, toss_decision;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q9
st.header("Q9: Most economical bowlers in T20 format.")
st.write("Only those who bowled at least 2 overs and economy ≤ 6.")
if st.button("Run Q9"):
    query = """
        SELECT 
            player_name,
            team_name,
            COUNT(DISTINCT bd.matchId) AS matches_played,
            SUM(overs) AS total_overs_bowled,
            SUM(wickets) AS total_wickets,
            AVG(economy) AS avg_economy
        FROM bowler_data bd
        JOIN match_summaries ms ON bd.matchId = ms.matchId
        WHERE ms.format = 'T20'
        GROUP BY player_name, team_name
        HAVING SUM(overs) >= 2 AND AVG(economy) <= 6
        ORDER BY avg_economy ASC;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q10
st.header("Q10: Top Player Performance Ranking.")
st.write("Combined batting & bowling points, ranked by performance score.")
if st.button("Run Q10"):
    query = """
        WITH BattingStats AS (
            SELECT bd.player_id, bd.player_name, bd.team_name,
                   SUM(bd.runs) AS total_runs,
                   AVG(bd.strike_rate) AS avg_strike_rate,
                   AVG(bd.runs) AS batting_average
            FROM batsman_data bd
            JOIN match_summaries ms ON bd.matchId = ms.matchId
            GROUP BY bd.player_id, bd.player_name, bd.team_name
        ),
        BowlingStats AS (
            SELECT bd.player_id, bd.player_name, bd.team_name,
                   SUM(bd.wickets) AS total_wickets,
                   AVG(bd.economy) AS avg_economy,
                   AVG(bd.wickets) AS bowling_average
            FROM bowler_data bd
            JOIN match_summaries ms ON bd.matchId = ms.matchId
            GROUP BY bd.player_id, bd.player_name, bd.team_name
        ),
        PlayerPerformance AS (
            SELECT b.player_id, b.player_name, b.team_name,
                   (b.total_runs * 0.01 + b.batting_average * 0.5 + b.avg_strike_rate * 0.3) AS batting_points,
                   (bo.total_wickets * 2 + (50 - bo.bowling_average) * 0.5 + (6 - bo.avg_economy) * 2) AS bowling_points
            FROM BattingStats b
            LEFT JOIN BowlingStats bo ON b.player_id = bo.player_id AND b.team_name = bo.team_name
        )
        SELECT player_id, player_name, team_name, batting_points, bowling_points,
               (batting_points + bowling_points) AS total_performance_score
        FROM PlayerPerformance
        ORDER BY total_performance_score DESC
        LIMIT 15;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# Q11
st.header("Q11: Analyze players scoring 50+ runs.")
st.write("Show player, team, opponent, runs, balls, strike rate, and venue.")
if st.button("Run Q11"):
    query = """
        SELECT bd.player_name, bd.team_name,
               CASE WHEN bd.team_name = ms.team1 THEN ms.team2 ELSE ms.team1 END AS opponent_name,
               bd.runs AS runs_scored,
               bd.balls,
               bd.strike_rate,
               ms.venue AS venue_name
        FROM batsman_data bd
        JOIN match_summaries ms ON bd.matchId = ms.matchId
        WHERE bd.runs >= 50
        ORDER BY bd.runs DESC;
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)
