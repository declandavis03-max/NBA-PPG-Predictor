# NBA-PPG-Predictor
Built a Python-based NBA Points per Game (ppg) predicator using live web data such as PPG, Defensive Rating (DRtg) from NBA basketball-reference, all while factoring in home and away games.

# Research Question
Can you build a model that accurately predicts an NBA players points per game on any given night during the NBA season?

# Data 
    Defensive/Offesnive Team Statistics:
    https://www.basketball-reference.com/leagues/NBA_2026.html
    Individual Player Statistics:
    https://www.basketball-reference.com/leagues/NBA_2026_per_game.html 

# Tools Used
Python | Pandas (pd)

# Approach 

Phase 1: Data Collection and Inputs

    1. In Depth, Live Web Scrpaing:  From basektball reference
    (Team PPG, Indidiual PPG, Team Defensive Rating)
   
    2. Defined User Parameters:
        Added guided user parameters for the user to provide the model with the players name, 
        his team (abbreviations if needed via dictionary), and location of the game (Home or Away). 

Phase 2: Prediction Formula

    3. Home Court Factor:
        Appilies a home court factor on points scored depending on where the selted player is playing.
        Home: +1 Points
        Away: -1 Points 

    4. Defensive Rating Adjustment:
        Adjusts the score by comparing opponent's defensive rating compared to league average DRtg, all based on player share of their team's points. 
        (Opp DRtg - League Avg DRtg) * (Player PPG / Team PPG)

    5. Final Rounded Forecast:
    Sums the base player's PPG and the DRtg adjustment, as well as Game location to include a final prediction.
    
# Key Insights 
    1. 
    2. 
    3. 

# Limitations & Next Steps




