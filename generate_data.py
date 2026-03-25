import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate dates for the year 2025
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Generate fitness data
steps = np.random.normal(loc=8500, scale=2000, size=365).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1, size=365).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=365).clip(48, 110)
calories_burned = np.random.uniform(1800, 4200, size=365)
active_minutes = np.random.uniform(20, 180, size=365)

# Introduce 5% missing values (NaN)
for column in [steps, sleep_hours, heart_rate_bpm, calories_burned, active_minutes]:
    indices = np.random.choice(range(365), size=int(365 * 0.05), replace=False)
    column[indices] = np.nan

# Create a DataFrame
fitness_data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_BPM': heart_rate_bpm,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Save to CSV
fitness_data.to_csv('data/health_data.csv', index=False)

print("Fitness data generated and saved to data/health_data.csv")