# NBA-PPG-Predictor
Built a Python-based NBA Points per Game (ppg) predicator using live web data such as PPG, Defensive Rating (DRtg) from NBA basketball-reference, all while factoring location of the game.

## Table of Contents

- [Research Question](#Research-Question)
- [ Data Pipeline and Data](#Data-Pipeline-and-Data)
- [Tools Used](#tools-used)
- [Approach](#Approach)
- [Overall Insights](#Overall-Insights)

# Research Question
Using online data from Sports Reference, Can there be a model that accurately predicts an NBA players points per game on any given night during the NBA season?

# Data Pipeline and Data

### Data Pipeline
WIth Sports Reference Data, the goal is create a points per game predictor using these steps

```
Websites Used for Data --> Creation of Forumla --> Data Collection and Building Functions --> Testing --> Overall Insights
```

### Websites Used for Data
Found Player and Team Statistics for the model. 
    
    -Defensive/Offesnive Team Statistics:
    https://www.basketball-reference.com/leagues/NBA_2026.html
    
    -Individual Player Statistics:
    https://www.basketball-reference.com/leagues/NBA_2026_per_game.html 

Tools Used
    Python | Pandas (pd)


# Creation of Formula

### Prediction Formula

    1. Home Court Factor:
        Appilies a home court factor on points scored depending on where the selted player is playing.
        Home: +1 Points
        Away: -1 Points 

    2. Defensive Rating Adjustment:
        Adjusts the score by comparing opponent's defensive rating compared to league average DRtg, all based on player share of their team's points. 
        (Opp DRtg - League Avg DRtg) * (Player PPG / Team PPG)

    3. Final Rounded Forecast:
    Sums the base player's PPG and the DRtg adjustment, as well as Game location to include a final prediction.

### Final Formula
### Predicted_PPG = Current_PPG - (DRtg_ADJ) +- (Home Court Factor)

# Data Collection and Building of Functions
   
    1. Defined User Parameters:
        Added guided user parameters for the user to provide the model with the players name, 
        his team (abbreviations if needed via dictionary), and location of the game (Home or Away). 

    2.  In Depth, Live Web Scraping:  From basektball reference
    (Team PPG, Indidiual PPG, Team Defensive Rating)

    3. 

# Testing
    
# Key Insights 
    1. 
    2. 
    3. 

# Limitations & Next Steps




