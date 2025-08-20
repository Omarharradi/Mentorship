import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page config
st.set_page_config(
    page_title="Ivy Leadership & Mentorship Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Nesma-inspired orange and white light theme
st.markdown("""
<style>
    /* Force light theme and prevent dark mode */
    .main {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f0 100%) !important;
        color: #2d3748 !important;
    }
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f0 100%) !important;
        color: #2d3748 !important;
    }
    .css-1d391kg {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f0 100%) !important;
        color: #2d3748 !important;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f0 100%) !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    .stSelectbox > div > div {
        background-color: white !important;
        color: #2d3748 !important;
        border: 2px solid #fed7aa !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(255, 165, 0, 0.1);
    }
    .stMetric {
        background: white !important;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 0.5rem 0;
        border: 1px solid #fed7aa !important;
        box-shadow: 0 4px 12px rgba(255, 165, 0, 0.15);
        color: #2d3748 !important;
    }
    .metric-card {
        background: white !important;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(255, 165, 0, 0.15);
        border: 1px solid #fed7aa !important;
        color: #2d3748 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        color: #2d3748 !important;
        border-radius: 12px 12px 0 0;
        border: 1px solid #fed7aa !important;
        box-shadow: 0 2px 4px rgba(255, 165, 0, 0.1);
    }
    .stTabs [aria-selected="true"] {
        background: #ff6b35 !important;
        color: white !important;
        border-color: #ff6b35 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2d3748 !important;
        font-weight: 700;
    }
    h1 {
        color: #ff6b35 !important;
    }
    .stDataFrame {
        background-color: white !important;
        border-radius: 12px;
        border: 1px solid #fed7aa !important;
        box-shadow: 0 4px 6px rgba(255, 165, 0, 0.1);
        color: #2d3748 !important;
    }
    .stSidebar {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px);
        border-right: 2px solid #fed7aa !important;
        color: #2d3748 !important;
    }
    .stButton > button {
        background: #ff6b35 !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }
    .stButton > button:hover {
        background: #e55a2b !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
    }
    .stExpander {
        background: white !important;
        border-radius: 12px;
        border: 1px solid #fed7aa !important;
        box-shadow: 0 2px 8px rgba(255, 165, 0, 0.1);
        color: #2d3748 !important;
    }
    .stSuccess {
        background: linear-gradient(90deg, #48bb78, #38a169) !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    .stWarning {
        background: linear-gradient(90deg, #ff6b35, #e55a2b) !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    .stError {
        background: linear-gradient(90deg, #f56565, #e53e3e) !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    .stInfo {
        background: linear-gradient(90deg, #ff6b35, #e55a2b) !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    /* Navigation button styling */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #2d3748 !important;
        border: 2px solid #fed7aa !important;
        box-shadow: 0 2px 4px rgba(255, 165, 0, 0.1);
    }
    .stButton > button[kind="secondary"]:hover {
        background: #fff5f0 !important;
        border-color: #ff6b35 !important;
        color: #ff6b35 !important;
    }
    /* Additional light theme enforcement */
    .stMarkdown {
        color: #2d3748 !important;
    }
    .stText {
        color: #2d3748 !important;
    }
    div[data-testid="metric-container"] {
        background: white !important;
        color: #2d3748 !important;
        border: 1px solid #fed7aa !important;
        border-radius: 12px;
    }
    /* Force text inputs to be light */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #2d3748 !important;
        border: 1px solid #fed7aa !important;
    }
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #2d3748 !important;
    }
    /* Make all tables transparent */
    .stDataFrame {
        background-color: transparent !important;
        border-radius: 12px;
        border: 1px solid #fed7aa !important;
        box-shadow: 0 4px 6px rgba(255, 165, 0, 0.1);
        color: #2d3748 !important;
    }
    .stDataFrame > div {
        background-color: transparent !important;
    }
    .stDataFrame table {
        background-color: transparent !important;
    }
    .stDataFrame thead tr th {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #2d3748 !important;
        border-bottom: 2px solid #fed7aa !important;
    }
    .stDataFrame tbody tr td {
        background-color: rgba(255, 255, 255, 0.6) !important;
        color: #2d3748 !important;
        border-bottom: 1px solid #fed7aa !important;
    }
    .stDataFrame tbody tr:nth-child(even) td {
        background-color: rgba(255, 245, 240, 0.8) !important;
    }
    /* Ensure all text is dark and readable */
    * {
        color: #2d3748 !important;
    }
    .stApp > header {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'selected_mentor' not in st.session_state:
    st.session_state.selected_mentor = None
 
# Load data function
@st.cache_data
def load_data():
    """Load all CSV data files"""
    data = {}
    data_dir = "data"
    
    try:
        data['mentors'] = pd.read_csv(f"{data_dir}/mentors.csv")
        data['pairings'] = pd.read_csv(f"{data_dir}/pairings.csv")
        data['goals'] = pd.read_csv(f"{data_dir}/goals.csv")
        data['engagement'] = pd.read_csv(f"{data_dir}/engagement.csv")
        data['resources'] = pd.read_csv(f"{data_dir}/resources.csv")
        data['participation'] = pd.read_csv(f"{data_dir}/participation.csv")
        data['leadership_profiles'] = pd.read_csv(f"{data_dir}/leadership_profiles.csv")
        data['all_participants'] = pd.read_csv(f"{data_dir}/all_participants.csv")
        data['enhanced_engagement'] = pd.read_csv(f"{data_dir}/enhanced_engagement.csv")
        data['session_notes'] = pd.read_csv(f"{data_dir}/session_notes.csv")
        data['mentees_real_data'] = pd.read_csv(f"{data_dir}/mentees_real_data.csv")
        data['mentors_real_data'] = pd.read_csv(f"{data_dir}/mentors_real_data.csv")
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        return None
    
    return data

# Authentication simulation
def show_login():
    st.title("🎯 Ivy Leadership & Mentorship Dashboard")
    st.markdown("### *Empowering leadership through connected, data-driven mentorship*")

    _, logo1, logo2, _ = st.columns([1, 1, 1, 1])
    with logo1:
        st.image('assets/nesma2.png', width=200)
    with logo2:
        st.image('assets/Ivy Logo copy.png', width=200)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        # Only HR/Admin login available
        st.markdown("**HR/Admin Access**")
        
        if st.button("Login as HR/Admin", type="primary"):
            st.session_state.user_role = "HR"
            st.rerun()

def show_sidebar():
    """Show navigation sidebar"""
    with st.sidebar:
        st.title("🎯 Ivy Dashboard")
        
        # User info
        st.success("👤 Logged in as: **HR/Admin**")
        
        if st.button("Logout"): 
            st.session_state.user_role = None
            st.rerun()
        
        st.markdown("---")
        
        # Navigation menu - HR/Admin only
        pages = {
            "HR Dashboard": "hr_dashboard",  
            "All Participants": "mentor_eligibility", 
            "Progress Tracker": "progress_tracker",
            "Resource Library": "resource_library"
        }
        
        # Initialize selected page in session state if not exists
        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = "hr_dashboard"
        
        # Create navigation buttons
        for page_name, page_key in pages.items():
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.selected_page = page_key
                st.rerun()
        
        return st.session_state.selected_page

def main():
    # Check if user is logged in
    if st.session_state.user_role is None:
        show_login()
        return
    
    # Load data
    data = load_data()
    if data is None:
        st.error("Unable to load application data. Please check data files.")
        return
    
    # Show sidebar and get selected page
    selected_page = show_sidebar()
    
    # Import and show selected page
    if selected_page == "hr_dashboard":
        from modules.hr_dashboard import show_hr_dashboard
        show_hr_dashboard(data)
    elif selected_page == "mentor_eligibility":
        from modules.mentor_eligibility import show_mentor_eligibility
        show_mentor_eligibility(data)
    elif selected_page == "progress_tracker":
        from modules.progress_tracker import show_progress_tracker
        show_progress_tracker(data)
    elif selected_page == "smart_goals":
        from modules.smart_goals import show_smart_goals
        show_smart_goals(data)
    elif selected_page == "resource_library":
        from modules.resource_library import show_resource_library
        show_resource_library(data)
    elif selected_page == "mentor_community":
        from modules.mentor_community import show_mentor_community
        show_mentor_community(data)
        show_resources(data)


if __name__ == "__main__":
    main()
