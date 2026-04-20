import streamlit as st
import plotly.express as px
from modules.proccessor import process_data
import pandas as pd

# Set the page configuration
st.set_page_config(layout="wide", page_title="Trends & Insights")

# Title of the page
st.title("Trends & Insights")

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

# Show summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].describe().loc[['mean', 'min', 'max']])

# Average Recovery Score Month-wise
st.subheader("Average Recovery Score Month-wise")
# Add month column
filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
monthly_avg_recovery = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()

# Convert 'Month' to string for JSON serialization compatibility
monthly_avg_recovery['Month'] = monthly_avg_recovery['Month'].astype(str)

fig1 = px.line(monthly_avg_recovery, x='Month', y='Recovery_Score', 
               labels={'Recovery_Score':'Average Recovery Score', 'Month':'Month'}, 
               title='Monthly Average Recovery Score')
st.plotly_chart(fig1, use_container_width=True)

# Distribution Histograms
st.subheader("Distribution Histograms")
# Create a 2-column layout for histograms
hist_col1, hist_col2 = st.columns(2)

# Histograms
with hist_col1:
    st.subheader("Distribution of Steps")
    fig2 = px.histogram(filtered_df, x='Steps', nbins=30, title='Steps Distribution')
    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Distribution of Recovery Score")
    fig3 = px.histogram(filtered_df, x='Recovery_Score', nbins=30, title='Recovery Score Distribution')
    st.plotly_chart(fig3, use_container_width=True)

with hist_col2:
    st.subheader("Distribution of Calories Burned")
    fig4 = px.histogram(filtered_df, x='Calories_Burned', nbins=30, title='Calories Burned Distribution')
    st.plotly_chart(fig4, use_container_width=True)
    st.subheader("Distribution of Sleep Hours")
    fig5 = px.histogram(filtered_df, x='Sleep_Hours', nbins=30, title='Sleep Hours Distribution')
    st.plotly_chart(fig5, use_container_width=True)

# Footer or additional information
st.markdown("---")
st.markdown("Deep dive into your data trends with detailed insights.")