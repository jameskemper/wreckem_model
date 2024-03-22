** Importing and creating tempfile for team IDS and conf

* Import team ID dataset
import delimited "https://raw.githubusercontent.com/jameskemper/wreckem_model/main/Data/MasterTeamSpellings.csv", clear

* Rename variables to match "team"
rename conference teamconf
rename confid teamconfid

* Create and save tempfile for Team IDS
tempfile team_ids
save `team_ids', replace

* Loop through each variable and add the prefix "opp"
foreach var of varlist _all {
    rename `var' opp`var'
}

* Create and save tempfile for Team IDS
tempfile opp_team_ids
save `opp_team_ids', replace


import delimited "https://raw.githubusercontent.com/jameskemper/wreckem_model/main/Data/schedule.csv", clear
rename v1 date
rename v2 team
rename v3 oppteam
generate new_date = date(date, "YDM")
order new_date, before(date)
drop date
rename new_date date

* Create and save tempfile for prev_scores
tempfile game_schedule
save `game_schedule', replace


* Import scores prior to tournament
import delimited "https://raw.githubusercontent.com/jameskemper/wreckem_model/main/Data/before_tournament.csv", clear
generate new_date = date(date, "MDY")
drop date
rename new_date date
format date %td
order date, before(team)
merge m:m team date using `game_schedule'

* Import scores upcoming_games
import delimited ""