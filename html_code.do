** Create HTML file using STATA
* Write Dyndoc script
dyndoc \\myweb.ttu.edu\users\jkemper\ncaa_odds.html, replace

* Insert HTML header and style
{{"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>NCAA Game Predictions</title>
<style>
    /* Add your CSS styles here */
    body {
        margin: 0 auto;
        font-family: 'Charter', 'Times New Roman', serif;
        background-color: white;
        color: #333;
        line-height: 1.6;
        padding: 0 5%;
    }

    a {
        color: #cc0000; 
        text-decoration: underline;
    }

    img {
        max-width: 100%;
        height: auto;
    }

    nav {
        text-align: center;
        margin-top: 20px;
        background-color: white;
    }

    .navLinks a {
        display: inline-block;
        padding: 10px 15px; 
        background-color: #cc0000;
        color: #ffffff; 
        font-weight: bold;
        text-decoration: underline; 
        margin-right: 10px;
        margin-left: 10px; 
        border-radius: 5px;
    }

    .profileSection {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 20px;
        border-bottom: 1px solid #666;
    }

    .profilePhoto {
        width: 40%; 
        padding-right: 20px;
    }

    .contactInfo {
        text-align: left;
    }

    .contactInfo p {
        font-size: 1em;
    }

    .welcomeSection, .mainContent {
        padding: 20px;
        text-align: left;
        border-bottom: 1px solid #666;
    }

    .welcomeSection h3, .mainContent h3 {
        font-size: 1.2em;
    }

    .welcomeSection p, .mainContent ul {
        font-size: 1em;
    }

    footer {
        text-align: center;
        padding: 20px;
    }

    @media screen and (max-width: 768px) {
        .profileSection {
            flex-direction: column;
            align-items: center;
        }

        .navLinks a {
            padding: 8px;
            font-size: 0.8em;
        }

        body, .contactInfo p, .welcomeSection p, .mainContent ul {
            padding: 0 10px;
        }
    }

    /* Additions for the NCAA Predictions Table */
    .predictions-table {
        border-collapse: collapse;
        width: 100%;
        font-family: 'Charter', 'Times New Roman', serif; /* Ensuring font consistency */
        color: #333; /* Text color */
    }

    .predictions-table th, .predictions-table td {
        text-align: left;
        padding: 8px;
        border: 1px solid #ddd; /* Lighter border for a subtle look */
    }

    .predictions-table th {
        background-color: #f2f2f2; /* Light grey background for headers */
    }

    /* Custom class adjustments */
    .winner {
        font-weight: bold;
        color: #cc0000; /* Link color for winners to highlight */
    }

    .probability {
        color: green; /* No change here, but ensure it fits with your design */
    }
</style>
</head>
<body>
<h2>NCAA Game Predictions</h2>
<table class='predictions-table'>
    <thead>
        <tr>
            <th>Date</th>
            <th>Team</th>
            <th>Opponent</th>
            <th>Predicted Winner</th>
            <th>Win Probability</th>
        </tr>
    </thead>
    <tbody>
"}}

* Insert Stata code to generate table rows
{{
    foreach i of numlist 1/`=_N' {
        local date = date[`i']
        local team = team[`i']
        local oppteam = oppteam[`i']
        local predicted_winner = predicted_winner[`i']
        local percentage_sim_win = percentage_sim_win[`i']

        echo "<tr>"
        echo "<td>`date'</td>"
        echo "<td>`team'</td>"
        echo "<td>`oppteam'</td>"
        echo "<td class='winner'>`predicted_winner'</td>"
        echo "<td class='probability'>`percentage_sim_win'</td>"
        echo "</tr>"
    }
}}

* Insert HTML footer
{{"
</tbody>
</table>
</body
