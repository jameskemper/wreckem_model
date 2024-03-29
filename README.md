# WRECKEM: NCAA Men's Basketball Game Predictor

## Overview
Welcome to the WRECKEM repository, a predictive model named in honor of Texas Tech University, designed to forecast outcomes of NCAA Men's Basketball games. Leveraging the principles of the ELO ranking system, this model integrates NCAA quad wins statistics and KenPom efficiency scores to predict game outcomes with enhanced accuracy.

## Model Description
WRECK_EM is rooted in the ELO ranking system, a method for calculating the relative skill levels of players in competitor-versus-competitor games. The model adapts this system to the dynamic and competitive world of NCAA Men's Basketball by incorporating:

- **NCAA Quad Wins Statistics**: A key metric reflecting the quality of wins based on the location and opponent's ranking, available [here](https://stats.ncaa.org/selection_rankings/nitty_gritties).
- **KenPom Efficiency Scores**: Critical for assessing the offensive and defensive efficiency of teams, available [here](https://kenpom.com/).

By running 850 simulations for every game based on various regressions, WRECK_EM aims to provide a detailed probabilistic forecast for each matchup.

## ELO Ranking System
Click [here](https://en.wikipedia.org/wiki/Elo_rating_system) or [here](https://link.springer.com/article/10.1007/s11257-016-9185-7) for more information on the ELO ranking system and adaptive maodels, which forms the basis of the model. 

## License
WRECK_EM is open-sourced under the MIT License. See the LICENSE file for more details.

