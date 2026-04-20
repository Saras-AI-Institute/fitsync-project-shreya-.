import streamlit as st
from modules.proccessor import process_data
import pandas as pd
import plotly.express as px

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
    filtered_df = df[df['Date'] >= df['Date'].max() - pd.Timedelta(days=7)]
elif time_range == "Last 30 days":
    filtered_df = df[df['Date'] >= df['Date'].max() - pd.Timedelta(days=30)]
else:
    filtered_df = df

# Calculate metrics from the filtered DataFrame
average_steps = filtered_df['Steps'].mean()
average_sleep_hours = filtered_df['Sleep_Hours'].mean()
average_recovery_score = filtered_df['Recovery_Score'].mean()

# Create a 3-column layout for displaying key metrics
col1, col2, col3 = st.columns(3)

# Display metrics in the columns
col1.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)
col2.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)
col3.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Create two columns for the first set of visualizations
left_col1, right_col1 = st.columns(2)

# Recovery Score & Sleep Trend: Dual line chart
with left_col1:
    st.subheader("Recovery Score & Sleep Trend")
    fig1 = px.line(filtered_df, x='Date', y=['Recovery_Score', 'Sleep_Hours'],
                   labels={'value':'Metrics'}, title='Recovery Score & Sleep Trend')
    st.plotly_chart(fig1, use_container_width=True)

# Recovery Score vs Daily Steps: Scatter Plot
with right_col1:
    st.subheader("Recovery Score vs Daily Steps")
    fig2 = px.scatter(filtered_df, x='Steps', y='Recovery_Score', color='Sleep_Hours',
                      title='Recovery Score vs Daily Steps',
                      labels={'Steps':'Daily Steps', 'Recovery_Score':'Recovery Score'},
                      color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig2, use_container_width=True)

# Create two columns for the second set of visualizations
left_col2, right_col2 = st.columns(2)

# Recovery Score vs Resting Heart Rate: Scatter Plot
with left_col2:
    st.subheader("Recovery Score vs Resting Heart Rate")
    fig3 = px.scatter(filtered_df, x='Heart_Rate_BPM', y='Recovery_Score',
                      title='Recovery Score vs Resting Heart Rate',
                      labels={'Heart_Rate_BPM':'Resting Heart Rate', 'Recovery_Score':'Recovery Score'})
    st.plotly_chart(fig3, use_container_width=True)

# Daily Calories Burned Trend: Line chart
with right_col2:
    st.subheader("Daily Calories Burned Trend")
    fig4 = px.line(filtered_df, x='Date', y='Calories_Burned',
                   labels={'Calories_Burned':'Calories Burned', 'Date':'Date'},
                   title='Daily Calories Burned Trend')
    st.plotly_chart(fig4, use_container_width=True)
# Footer or additional information
st.markdown("---")
st.markdown("Developed by [Your Name]. Empowering you with data-driven health insights.")

