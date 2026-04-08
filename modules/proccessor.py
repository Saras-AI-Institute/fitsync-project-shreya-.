import pandas as pd
from datetime import datetime

# Function to load and clean the data

def load_data():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('data/health_data.csv')
    
    # Fill missing 'steps' with the median value
    df['Steps'].fillna(df['Steps'].median(), inplace=True)
    
    # Fill missing 'Sleep_Hours' with 7.0
    df['Sleep_Hours'].fillna(7.0, inplace=True)
    
    # Fill missing 'Heart_Rate_bpm' with 68
    df['Heart_Rate_BPM'].fillna(68, inplace=True)
    
    # Fill other columns with their median value
    for column in df.columns:
        if df[column].isnull().any() and column not in ['Steps', 'Sleep_Hours', 'Heart_Rate_BPM']:
            df[column].fillna(df[column].median(), inplace=True)
    
    # Convert 'date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Return the cleaned DataFrame
    return df

# The above function provides a comprehensive approach to cleaning the data by addressing missing values intelligently and ensuring the 'date' column is in datetime format. This prepares the data for further analysis or modeling.

# Function to calculate the recovery score for each day and add it to the DataFrame
def calculate_recovery_score(df):

    def get_recovery_score(row):
        score = 50  # Start with a baseline score of 50

        # Adjust the score based on Sleep Hours
        if row['Sleep_Hours'] >= 7:
            score += 30  # Good sleep significantly boosts the score
        elif row['Sleep_Hours'] < 6:
            score -= 20  # Poor sleep heavily reduces the score

        # Adjust the score based on Heart Rate
        if row['Heart_Rate_BPM'] < 70:
            score += 10  # Lower heart rate is better for recovery
        elif row['Heart_Rate_BPM'] > 85:
            score -= 10  # Higher heart rate may indicate stress

        # Adjust the score based on Steps
        if row['Steps'] > 12000:
            score -= 5  # Very high activity might induce strain
        elif row['Steps'] < 4000:
            score -= 5  # Very low activity might indicate poor health

        # Ensure the score is between 0 and 100
        score = max(0, min(100, score))
        return score

    # Apply the calculation to each row of the DataFrame
    df['Recovery_Score'] = df.apply(get_recovery_score, axis=1)

    # Return the DataFrame with the new Recovery_score column
    return df

# Example logic: a balanced approach to score calculation based on realistic ranges and conditions for Sleep_Hours, Heart_Rate_BPM, and Steps.

def process_data():
    df = load_data()
    df = calculate_recovery_score(df)
    return df

