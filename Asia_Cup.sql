create database Cricbuzz;
use Cricbuzz;
SELECT * FROM batsman_data;
select* from bowler_data;

UPDATE bowler_data
SET player_name = CASE 
              WHEN player_name = 'Axar' THEN 'Axar Patel'
              WHEN player_name = 'Bumrah' THEN 'Jasprit Bumrah'
           END
WHERE player_name IN ('Axar', 'Bumrah');

INSERT INTO match_summaries
(matchId, description, format, type, series, Date, team1, team2, toss_winner, toss_decision, winner, win_by_runs, margin, status)
VALUES
(130008, '1st Match,Group B', 'T20', 'International', 'Asia Cup 2025',
 STR_TO_DATE('09/09/2025 20:00:00','%d/%m/%Y %H:%i:%s'),
 'Afghanistan', 'Hong Kong', 'Afghanistan', 'Batting', 'Afghanistan', 1, 94, 'Afghanistan won by 94 runs'),

(130019, '2nd Match,Group A', 'T20', 'International', 'Asia Cup 2025',
 STR_TO_DATE('10/09/2025 20:00:00','%d/%m/%Y %H:%i:%s'),
 'United Arab Emirates', 'India', 'India', 'Bowling', 'India', 0, 9, 'India won by 9 wkts'),

(130030, '3rd Match,Group B', 'T20', 'International', 'Asia Cup 2025',
 STR_TO_DATE('11/09/2025 20:00:00','%d/%m/%Y %H:%i:%s'),
 'Hong Kong', 'Bangladesh', 'Bangladesh', 'Bowling', 'Bangladesh', 0, 7, 'Bangladesh won by 7 wkts');
 
 ALTER TABLE match_summaries MODIFY Date DATETIME;
 
 SELECT matchId, description, 
       DATE_FORMAT(Date, '%d/%m/%Y %h:%i %p') AS match_datetime,
       team1, team2, winner, status
FROM match_summaries;

UPDATE match_summaries
SET Venue = 'Sheikh Zayed Stadium',
    City = 'Abu Dhabi, United Arab Emirates',
    Group_name = 'B'
WHERE matchId = 130008;

UPDATE match_summaries
SET Venue = 'Dubai International Cricket Stadium',
    City = 'Dubai, United Arab Emirates',
    Group_name = 'A'
WHERE matchId = 130019;

UPDATE match_summaries
SET Venue = 'Sheikh Zayed Stadium',
    City = 'Abu Dhabi, United Arab Emirates',
    Group_name = 'B'
WHERE matchId = 130030;

ALTER TABLE match_summaries
ADD COLUMN win_by_runs BOOLEAN;

UPDATE match_summaries
SET win_by_runs = FALSE
WHERE matchId = 130008;
UPDATE match_summaries
SET win_by_runs = TRUE
WHERE matchId = 130019;
UPDATE match_summaries
SET win_by_runs = TRUE
WHERE matchId = 130030;

ALTER TABLE batsman_data CHANGE `ï»¿matchId` matchId INT;
ALTER TABLE bowler_data CHANGE `ï»¿matchId` matchId INT;

select* from bowler_data;
select * from batsman_data;
select* from player_descriptions;
select* from match_summaries;

#Q1.Find all players who represent India. Display their full name, playing role, batting style, and bowling style?
SELECT DISTINCT pd.player_id, pd.player_name, pd.description
FROM player_descriptions pd
LEFT JOIN batsman_data bd ON pd.player_id = bd.player_id
WHERE bd.team_name = 'India' OR bd.team_name IS NULL;

#Q2.Show all cricket matches that were played in the last 30 days. Include the match description, both team names,
# venue name with city, and the match date. Sort by most recent matches first?
SELECT description, team1, team2, venue AS venue_name, city, group_name, Date AS match_date
FROM match_summaries
WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY Date DESC;

#Q3.Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first?
SELECT winner AS team_name, 
       CASE 
           WHEN winner = team1 THEN team2 
           ELSE team1 
       END AS opponent_team,
       COUNT(matchId) AS total_wins
FROM match_summaries
GROUP BY winner, opponent_team
ORDER BY total_wins DESC;

#Q4.Find the highest individual batting score achieved in Asia Cup 2025 so far?
SELECT team_name, player_name, runs, balls, fours, sixes, strike_rate
FROM batsman_data
WHERE runs = (SELECT MAX(runs) FROM batsman_data);

#Q5.Get details of the last 20 completed matches.Show match description, both team names, winning team,
# victory margin, victory type (runs/wickets), and venue name. Display most recent matches first.
SELECT description, team1, team2, winner, 
       CASE 
            WHEN win_by_runs = 'TRUE' THEN margin
            ELSE margin
       END AS victory_margin,
       CASE 
            WHEN win_by_runs = 'TRUE' THEN 'Runs'
            ELSE 'Wickets'
       END AS victory_type,
       Date
FROM match_summaries
ORDER BY Date DESC
LIMIT 20;

#Q6.Bowling performance at different venues: average economy, total wickets?
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

#Q7.create bowler status with player_name ,team_name, matches_played, overs bowled minimum of 3,wickets,economy based on maximum wickets?
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
ORDER BY total_wickets DESC Limit 10;

#Q8.Question 17 Investigate whether winning the toss gives teams an advantage in winning matches.
# Calculate what percentage of matches are won by the team that wins the toss, broken down by their toss decision (choosing to bat first or bowl first).
SELECT toss_winner, toss_decision, 
               SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS matches_won_after_toss,
               COUNT(matchId) AS total_matches,
               ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(matchId) * 100, 2) AS win_percentage
        FROM match_summaries
        GROUP BY toss_winner, toss_decision;

#Q9.Find the most economical bowlers in limited-overs cricket in T20 formats. Calculate each bowler's overall economy rate and total wickets taken.
#Only consider bowlers who have bowled in at least a matche and bowled at least 2 overs per match on average.
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
HAVING SUM(overs) >= 2
   AND AVG(economy) <= 6
ORDER BY avg_economy ASC;

#Q10.Create a comprehensive performance ranking system for players. Combine their batting performance (runs scored, batting average, strike rate), 
#bowling performance (wickets taken, bowling average, economy rate) into a single weighted score. Use this formula and rank players:
# ●	Batting points: (runs_scored × 0.01) + (batting_average × 0.5) + (strike_rate × 0.3)
# ●	Bowling points: (wickets_taken × 2) + (50 - bowling_average) × 0.5) + ((6 - economy_rate) × 2)
#  Rank the top performers in each cricket format?

WITH BattingStats AS (
    SELECT 
        bd.player_id,
        bd.player_name,
        bd.team_name,
        SUM(bd.runs) AS total_runs,
        AVG(bd.strike_rate) AS avg_strike_rate,
        AVG(bd.runs) AS batting_average
    FROM batsman_data bd
    JOIN match_summaries ms ON bd.matchId = ms.matchId
    GROUP BY bd.player_id, bd.player_name, bd.team_name
),

BowlingStats AS (
    SELECT 
        bd.player_id,
        bd.player_name,
        bd.team_name,
        SUM(bd.wickets) AS total_wickets,
        AVG(bd.economy) AS avg_economy,
        AVG(bd.wickets) AS bowling_average
    FROM bowler_data bd
    JOIN match_summaries ms ON bd.matchId = ms.matchId
    GROUP BY bd.player_id, bd.player_name, bd.team_name
),

PlayerPerformance AS (
    SELECT 
        b.player_id,
        b.player_name,
        b.team_name,
        (b.total_runs * 0.01 + b.batting_average * 0.5 + b.avg_strike_rate * 0.3) AS batting_points,
        (bo.total_wickets * 2 + (50 - bo.bowling_average) * 0.5 + (6 - bo.avg_economy) * 2) AS bowling_points
    FROM BattingStats b
    LEFT JOIN BowlingStats bo ON b.player_id = bo.player_id AND b.team_name = bo.team_name
)

SELECT 
    player_id,
    player_name,
    team_name,
    batting_points,
    bowling_points,
    (batting_points + bowling_points) AS total_performance_score
FROM PlayerPerformance
ORDER BY total_performance_score DESC
LIMIT 15;

#Q11.Analyze batting performance with players scored 50+ runs?
SELECT 
    bd.player_name,
    bd.team_name,
    CASE 
        WHEN bd.team_name = ms.team1 THEN ms.team2
        ELSE ms.team1
    END AS opponent_name,
    bd.runs AS runs_scored,
    bd.balls,
    bd.strike_rate,
    ms.Venue AS Venue_name
FROM batsman_data bd
JOIN match_summaries ms ON bd.matchId = ms.matchId
WHERE bd.runs >= 50
ORDER BY bd.runs DESC;
















 






