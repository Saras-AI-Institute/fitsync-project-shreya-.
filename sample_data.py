import pandas as pd

def load_and_print_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Print the first 5 rows
    print("First 5 rows:")
    print(data.head())
    
    # Print the number of missing values in each column
    print("\nNumber of missing values in each column:")
    print(data.isnull().sum())

# Define the path to the CSV file
file_path = 'data/health_data.csv'

# Load the data and perform the operations
load_and_print_data(file_path)
