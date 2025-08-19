import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page config
st.set_page_config(
    page_title="Ivy Leadership & Mentorship Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional, modern theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2d3748;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stSelectbox > div > div {
        background-color: white;
        color: #2d3748;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 0.5rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: white;
        color: #4a5568;
        border-radius: 12px 12px 0 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stTabs [aria-selected="true"] {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2d3748 !important;
        font-weight: 700;
    }
    h1 {
        color: #667eea !important;
    }
    .stDataFrame {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .stSidebar {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: 2px solid #e2e8f0;
    }
    .stButton > button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        background: #5a67d8;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    .stExpander {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .stSuccess {
        background: linear-gradient(90deg, #48bb78, #38a169);
        color: white;
        border-radius: 12px;
        border: none;
    }
    .stWarning {
        background: linear-gradient(90deg, #ed8936, #dd6b20);
        color: white;
        border-radius: 12px;
        border: none;
    }
    .stError {
        background: linear-gradient(90deg, #f56565, #e53e3e);
        color: white;
        border-radius: 12px;
        border: none;
    }
    .stInfo {
        background: linear-gradient(90deg, #4299e1, #3182ce);
        color: white;
        border-radius: 12px;
        border: none;
    }
    /* Navigation button styling */
    .stButton > button[kind="secondary"] {
        background: white;
        color: #4a5568;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stButton > button[kind="secondary"]:hover {
        background: #f7fafc;
        border-color: #667eea;
        color: #667eea;
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
        
        if st.button("🚪 Logout"): 
            st.session_state.user_role = None
            st.rerun()
        
        st.markdown("---")
        
        # Navigation menu - HR/Admin only
        pages = {
            "📊 HR Dashboard": "hr_dashboard",  
            "🔍 Mentor Eligibility": "mentor_eligibility", 
            "👥 Pairings & Progress": "pairings_progress",
            "📈 Engagement Insights": "engagement_insights",
            "📚 Resource Library": "resource_library"
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
    elif selected_page == "pairings_progress":
        from modules.pairings_progress import show_pairings_progress
        show_pairings_progress(data)
    elif selected_page == "smart_goals":
        from modules.smart_goals import show_smart_goals
        show_smart_goals(data)
    elif selected_page == "engagement_insights":
        from modules.engagement_insights import show_engagement_insights
        show_engagement_insights(data)
    elif selected_page == "resource_library":
        from modules.resource_library import show_resource_library
        show_resource_library(data)
    elif selected_page == "mentor_community":
        from modules.mentor_community import show_mentor_community
        show_mentor_community(data)
        show_resources(data)


if __name__ == "__main__":
    main()
