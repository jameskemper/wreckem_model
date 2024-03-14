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

** Scarpping and importing the current results for NCAA games

* Capture the current date
clear
local year = year(date(c(current_date), "DMY"))
local month = month(date(c(current_date), "DMY"))
local day = day(date(c(current_date), "DMY"))

* Concatenate to form the full URL for the CSV file without leading zeros in month and day
local base_url "https://raw.githubusercontent.com/lbenz730/NCAA_Hoops/master/3.0_Files/Results/2023-24/NCAA_Hoops_Results_"
local full_url "`base_url'`month'_`day'_`year'.csv"

* Display the full URL for verification (Optional)
display "`full_url'"

* Import the CSV file from the dynamically generated URL
import delimited "`full_url'", clear

* Drop game scores that are not available (NA)
replace teamscore ="" if teamscore =="NA"
replace oppscore ="" if oppscore =="NA"
drop if year == 2023 & oppscore ==""
drop if year == 2023 & teamscore ==""

* Convert scores from string to numeric
destring teamscore, replace
destring oppscore, replace

* Create a variable for games that are upcoming
gen upcoming_game = teamscore==.

* Drop unused string variables
drop canceled postponed ot

* Change opponent to oppvariables
rename opponent oppteam

* Encode and generate Home/Away variables
encode location, generate(location_encoded)
drop location
rename location_encoded location

* Drop past games with no scores
drop if year == 2023 & teamscore ==.

** Merging Team IDs data with game results

* Create and save tempfile for game results
tempfile game_results
save `game_results', replace

*Merge data with team_ids tempfile and reorder
merge m:m team using "`team_ids'"
keep if _merge ==3
drop _merge
order teamid teamconf teamconfid, after(team)

*Merge data with opp_team_ids tempfile and reorder
merge m:m oppteam using "`opp_team_ids'"
keep if _merge ==3
drop _merge
order oppteamid oppteamconf oppteamconfid, after(oppteam)

* Save current game rsults
save `game_results', replace

** Collect, clean, and combine team stats

* Collect offense and defense rankings
import delimited "https://raw.githubusercontent.com/lbenz730/NCAA_Hoops/master/3.0_Files/Power_Rankings/power_rankings.csv", clear

* Calculate scaling factor for offense and generate ajdusted offense efficiency 
sort off_coeff
summarize off_coeff, detail
local off_dif = 100- r(max)
gen adj_off = off_coeff + `off_dif'

* Calculate scaling factor for defense and generate ajdusted defense efficiency 
sort def_coeff
summarize def_coeff, detail
local def_dif = 100- r(max)
gen adj_def = def_coeff + `def_dif'

* Combine adjusted stats with Team IDS
merge m:m team using `team_ids'
keep if _merge ==3
drop _merge
order teamid teamconf teamconfid , after(team)
drop conference

* Create and save adjusted stats tempfile
keep team teamid teamconf teamconfid adj_off adj_def
tempfile adj_stats
save `adj_stats', replace

* Loop through each variable and add the prefix "opp"
foreach var of varlist _all {
    rename `var' opp`var'
}

* Create and save opponent adjusted stats tempfile
tempfile opp_adj_stats
save `opp_adj_stats', replace

* Merge adjusted team stats with game results
use `game_results', clear
drop _merge
merge m:m team teamid using `adj_stats'
keep if _merge == 3
drop _merge

* Merge adjusted opponent team stats with game results
merge m:m oppteam oppteamid using `opp_adj_stats'
keep if _merge == 3
drop _merge
save `game_results', replace

** Import, clean, and edit KenPom statistics

import delimited "https://raw.githubusercontent.com/Owenbb2/KenPom-Exploration-March-2024/main/KenPomStats_2024.csv", clear

* Create adjusted scaler for luck
sort luck 
summarize luck , detail
local luck = 400- r(max)
gen adj_luck = luck + `luck'

keep team conf adjem adjo adjd adjtempo adj_luck

*Merge data with team_ids tempfile and reorder
merge m:m team using "`team_ids'"
keep if _merge ==3
drop _merge
order teamid teamconf teamconfid, after(team)

* Create tempfile for KenPom statistics
tempfile team_KenPom_stats
save `team_KenPom_stats', replace

* Loop through each variable and add the prefix "opp"
foreach var of varlist _all {
    rename `var' opp`var'
}

* Create and save opponent adjusted stats tempfile
tempfile opp_KenPom_stats
save `opp_KenPom_stats', replace

* Merge adjusted team stats with game results
use `game_results', clear
merge m:m team teamid using `team_KenPom_stats'
keep if _merge == 3
drop _merge

merge m:m oppteam oppteamid using `opp_KenPom_stats'
keep if _merge == 3
drop _merge
save `game_results', replace

** Import, clean, and edit NCAA Tournament Statistics 2021 - 2023

* Collect NCAA stats from dataset
import delimited "https://raw.githubusercontent.com/jameskemper/wreckem_model/main/Data/NCAA_stats.csv", clear

* Convert WLs into winning percentages, clean, and format
split wl, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate wl_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format wl_wl %9.3f
replace wl_wl = 0 if wl_wl ==.
drop wl quadrant_split1 quadrant_split2

split confrecord, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate confrecord_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format confrecord_wl %9.3f
replace confrecord_wl = 0 if confrecord_wl ==.
drop confrecord quadrant_split1 quadrant_split2

split nonconferencerecord, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate nonconferencerecord_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format nonconferencerecord_wl %9.3f
replace nonconferencerecord_wl = 0 if nonconferencerecord_wl ==.
drop nonconferencerecord quadrant_split1 quadrant_split2

split roadwl, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate roadwl_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format roadwl_wl %9.3f
replace roadwl_wl = 0 if roadwl_wl ==.
drop roadwl quadrant_split1 quadrant_split2


* Convert quadrant WLs into winning percentages, clean, and format
split quadrant1, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate quadrant1_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format quadrant1_wl %9.3f
replace quadrant1_wl = 0 if quadrant1_wl ==.
drop quadrant1 quadrant_split1 quadrant_split2

split quadrant2, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate quadrant2_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format quadrant2_wl %9.3f
replace quadrant2_wl = 0 if quadrant2_wl ==.
drop quadrant2 quadrant_split1 quadrant_split2

split quadrant3, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate quadrant3_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format quadrant3_wl %9.3f
replace quadrant3_wl = 0 if quadrant3_wl ==.
drop quadrant3 quadrant_split1 quadrant_split2

split quadrant4, parse("-") gen(quadrant_split)
destring quadrant_split1 quadrant_split2, replace
generate quadrant4_wl = quadrant_split1 / (quadrant_split1 + quadrant_split2)
format quadrant4_wl %9.3f
replace quadrant4_wl = 0 if quadrant4_wl ==.
drop quadrant4 quadrant_split1 quadrant_split2

* Rename and label variables
rename wl_wl wl
rename confrecord_wl confrecord
rename nonconferencerecord_wl nonconferencerecord
rename roadwl_wl roadwl
rename quadrant1_wl quadrant1
rename quadrant2_wl quadrant2
rename quadrant3_wl quadrant3
rename quadrant4_wl quadrant4
label variable wl "Win Loss %"
label variable confrecord "Conference Record %"
label variable nonconferencerecord "Non Conference Record %"
label variable roadwl "Road Win Loss %"
label variable quadrant1 "Quandrant 1 Win Loss %"
label variable quadrant2 "Quandrant 2 Win Loss %"
label variable quadrant3 "Quandrant 3 Win Loss %"
label variable quadrant4 "Quandrant 4 Win Loss %"

* Calculate scaling factors
sort avgoppnetrank 
summarize avgoppnetrank , detail
local avgoppnetrank = 400- r(max)
gen adj_avgoppnetrank = avgoppnetrank + `avgoppnetrank'

sort avgoppnet 
summarize avgoppnet , detail
local avgoppnet = 400- r(max)
gen adj_avgoppnet = avgoppnet + `avgoppnet'

sort quadrant1 
summarize quadrant1 , detail
local quadrant1 = 100- r(max)
gen adj_q1 = quadrant1 + `quadrant1'

sort quadrant2 
summarize quadrant2 , detail
local quadrant2 = 200- r(max)
gen adj_q2 = quadrant2 + `quadrant2'

sort quadrant3 
summarize quadrant3 , detail
local quadrant3 = 300- r(max)
gen adj_q3 = quadrant3 + `quadrant3'

sort quadrant4 
summarize quadrant4 , detail
local quadrant4 = 400- r(max)
gen adj_q4 = quadrant4 + `quadrant4'

sort netsos 
summarize netsos , detail
local netsos = 400- r(max)
gen adj_netsos = netsos + `netsos'

sort netnonconfsos 
summarize netnonconfsos , detail
local netnonconfsos = 400- r(max)
gen adj_netnonconfsos = netnonconfsos + `netnonconfsos'

*keep adjusted scalers and indentifiers
keep team conference adj_q1 adj_q2 adj_q3 adj_q4 adj_netsos adj_netnonconfsos adj_avgoppnetrank adj_avgoppnet

* Combine adjusted stats with Team IDS
merge m:m team using `team_ids'
keep if _merge == 3
order teamid teamconf teamconfid, after(team)
drop _merge

* Create tempfile and save data
tempfile NCAA_stats
save `NCAA_stats', replace

* Merge NCAA_stats with gamne results and save game_results
use `game_results', clear
merge m:m team teamid using `NCAA_stats'
keep if _merge ==3
drop _merge
save `game_results', replace

* Create tempfile for opponent NCAA stats
use `NCAA_stats', clear
tempfile opp_NCAA_stats
save `opp_NCAA_stats', replace
 
 * Loop through each variable and add the prefix "opp"
foreach var of varlist _all {
    rename `var' opp`var'
}
save `opp_NCAA_stats', replace

* Merge opp_NCAA_stats with gamne results and save game_results
use `game_results', replace
merge m:m oppteam oppteamid using `opp_NCAA_stats'
keep if _merge ==3
drop _merge
save `game_results', replace

** Model Analysis

* Creat date variable and xtset confid
gen date = mdy(month, day, year)
order date, before(year)
format %tdNN/DD/CCYY date
drop oppconference conference

* Create point_differential measurment and drop unused string variables

drop month day d1 location

* Create tempfile for model simulations

tempfile sims_stats
save `sims_stats', replace
 
* Create the point differential variable
gen point_differential = teamscore - oppscore

* Sort by teamid and date to ensure order
sort teamid date

* Create a variable to identify the last game of the day for each team
by teamid date: gen last_game = _n == _N

* Keep only the last game of the day
keep if last_game == 1
drop last_game

* Generate weight variables

gen month = month(date)
gen weight = month + (2024-year)
egen max_wieght = max(weight)
replace weight = weight/max_wieght
drop max_wieght
drop conf oppconf

* Run the regression model
by teamid, sort : regress point_differential adj_off adj_def oppadj_off oppadj_def adjem adjo adjd adjtempo adj_luck oppadjem oppadjo oppadjd oppadjtempo oppadj_luck adj_avgoppnetrank adj_avgoppnet adj_q1 adj_q2 adj_q3 adj_q4 adj_netsos adj_netnonconfsos oppadj_avgoppnetrank oppadj_avgoppnet oppadj_q1 oppadj_q2 oppadj_q3 oppadj_q4 oppadj_netsos oppadj_netnonconfsos if upcoming_game ==0 [iweight = weight]

* Calculate and store the standard deviation of the residuals
predict predicted_point_differential
predict residuals, residuals
summarize residuals, detail
scalar sd_resid = r(sd)

* Perform the simulations
local num_sims 850

* Loop to generate simulated outcomes for each game
forvalues i = 1/`num_sims' {
    gen error_term_`i' = rnormal(0, sd_resid)
    gen simulated_differential_`i' = cond(missing(point_differential), predicted_point_differential, point_differential) + error_term_`i'
}

* Calculate the mean of the simulated differentials
egen mean_simulated_differential = rowmean(simulated_differential_*)

* Initialize the count variable for team wins
gen teamwins = 0

* Loop through each simulation and increment the count if the team was predicted to win
forvalues i = 1/850 {
    replace teamwins =teamwins + (simulated_differential_`i' > 0)
}

* Initialize the count variable for oppteam wins
gen oppwins = 0

* Loop through each simulation and increment the count if the oppteam was predicted to win
forvalues i = 1/850 {
    replace oppwins =oppwins + (simulated_differential_`i' < 0)
}

* Drop All simulations
ds simulated_differential_*
drop `r(varlist)'

ds error_term_*
drop `r(varlist)'

* Calculate the percentage of simulations where the team/opponent wins
gen percentage_team_wins = teamwins / 850
gen percentage_opp_wins = oppwins / 850


* Gen predicted winning team variables
gen predicted_winner = team
replace predicted_winner = oppteam if mean_simulated_differential <0

gen percentage_sim_win = percentage_team_wins
replace percentage_sim_win = percentage_opp_wins if percentage_opp_wins > percentage_team_wins
replace percentage_sim_win = .999 if percentage_sim_win == 1

* Generate prediction message

gen threshold = " by more than 10 points."
replace threshold = " by less than 10 points." if abs(mean_simulated_differential) <10
replace threshold = " a very a close game." if abs(mean_simulated_differential) <5

generate message = predicted_winner + " is predicted to win" + threshold

* Keep only predictions
keep date team teamid teamconf teamconfid oppteam oppteamid oppteamconf oppteamconfid predicted_winner upcoming_game message percentage_sim_win
drop if upcoming_game ==0 
drop upcoming_game

* Create tempfile for predictions
tempfile `wreckem_predictions'
save `wreckem_predictions', replace

sort predicted_winner date
duplicates drop predicted_winner date, force
sort date teamconf team

* Export predictions (one works depending on desktop or latop)
export delimited using "C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Predictions\predictions.csv", replace
export delimited using "C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Predictions\predictions.csv", replace

* Get the current date in Stata's internal format
local cdate = date(c(current_date), "DMY")

* Extract year, month, and day as separate components
local year = year(`cdate')
local month = month(`cdate')
local day = day(`cdate')

* Convert numeric year, month, and day to string and concatenate them with underscores
local fdate = "`month'_`day'_`year'"

* Construct the file path with the current date in the filename
local filepath1 `"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Predictions\Predictions`fdate'.csv"'
local filepath2`"C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Predictions\Predictions`fdate'.csv"'


* Export the dataset to the constructed file path
export delimited using "`filepath1'", replace
export delimited using "`filepath2'", replace

