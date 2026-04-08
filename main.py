import streamlit as st
from modules.proccessor import process_data
import pandas as pd

# Set the page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

# Introduction text
st.markdown("Welcome to the *FitSync* dashboard! Dive into your personal health analytics with ease and modern visuals.")

# Sidebar for dynamic time filtering
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select time range",
    options=["Last 7 days", "Last 30 days", "All time"],
    index=2
)

# Load the data
df = process_data()

# Filter the DataFrame based on the time range selection
if time_range == "Last 7 days":
    df = df[df['Date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
elif time_range == "Last 30 days":
    df = df[df['Date'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]

# Calculate metrics from the filtered DataFrame
average_steps = df['Steps'].mean()
average_sleep_hours = df['Sleep_Hours'].mean()
average_recovery_score = df['Recovery_Score'].mean()

# Create a 3-column layout for displaying key metrics
col1, col2, col3 = st.columns(3)

# Display metrics in the columns
col1.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)
col2.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)
col3.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Health Data Overview Section
st.subheader("Health Data Overview")
data = df

# Display the data
# st.dataframe(data)

# Add more sophisticated visuals or analysis as needed below
# st.line_chart(data['Some_Column'])
# st.bar_chart(data['Another_Column'])

# Footer or additional information
st.markdown("---")
st.markdown("Developed by [Your Name]. Empowering you with data-driven health insights.")

