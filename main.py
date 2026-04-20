# import streamlit as st

# st.set_page_config(layout="wide", page_title="FitSync")

# st.title("Welcome to FitSync")
# st.write("Your personal health analytics dashboard")
# st.write("Use the sidebar to navigate between pages")



import streamlit as st

# Page config
st.set_page_config(layout="wide", page_title="FitSync")

# ------------------ THEME STATE ------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Toggle button
theme_toggle = st.sidebar.toggle("🌙 Dark Mode")

# Update theme
st.session_state.theme = "dark" if theme_toggle else "light"

# ------------------ CUSTOM CSS ------------------
def apply_theme(theme):
    if theme == "dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #0E1117;
                color: white;
            }
            [data-testid="stSidebar"] {
                background-color: #1a1f2e;
            }
            h1, h2, h3, h4, p {
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #FFFFFF;
                color: black;
            }
            [data-testid="stSidebar"] {
                background-color: #f0f2f6;
            }
            h1, h2, h3, h4, p {
                color: black !important;
            }
            </style>
        """, unsafe_allow_html=True)

apply_theme(st.session_state.theme)

# ------------------ HERO SECTION ------------------
st.markdown("""
    <h1 style='text-align: center;'>🏃‍♀️ Welcome to FitSync</h1>
    <p style='text-align: center; font-size:18px;'>
        Your Personal Health Analytics Dashboard
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------ FEATURES SECTION ------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Dashboard")
    st.write("Track your daily health metrics like steps, sleep, and recovery.")

with col2:
    st.markdown("### 📈 Trends")
    st.write("Analyze patterns and insights over time with powerful visuals.")

with col3:
    st.markdown("### ⚡ Insights")
    st.write("Make smarter health decisions using your personal data.")

st.markdown("---")

# ------------------ CALL TO ACTION ------------------
st.markdown("""
    <div style='text-align: center;'>
        <h3>🚀 Get Started</h3>
        <p>Use the sidebar to explore your dashboard and trends.</p>
    </div>
""", unsafe_allow_html=True)