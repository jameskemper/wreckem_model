import pandas as pd
from datetime import datetime

# Corrected path to the CSV file
input_file_path = r"C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\game_results\raw_games.csv"

# Load the CSV data into a DataFrame
try:
    data = pd.read_csv(input_file_path)

    # Convert the 'date' column to datetime objects for comparison
    data['date'] = pd.to_datetime(data['date'])

    # Get today's date as a datetime object
    today = datetime.now().date()

    # Filter out the games from today's date
    filtered_data = data[data['date'].dt.date != today]

    # Define the output file path
    output_file_path = r"C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\game_results\upcoming_games.csv"

    # Save the filtered data to a new CSV file
    filtered_data.to_csv(output_file_path, index=False)

    print(f"Filtered CSV saved to {output_file_path}")
except FileNotFoundError as e:
    print(f"The file was not found: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
