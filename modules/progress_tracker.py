import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def create_random_mentor_mentee_mapping(data):
    """Create random mapping between mentors and mentees from real data"""
    mentors_real = data['mentors_real_data'].copy()
    mentees_real = data['mentees_real_data'].copy()
    
    # Clean column names
    mentors_real.columns = mentors_real.columns.str.strip()
    mentees_real.columns = mentees_real.columns.str.strip()
    
    # Get mentor and mentee names
    mentor_names = mentors_real['Mentors from LDP'].dropna().tolist()
    mentee_names = mentees_real['Name'].dropna().tolist()
    
    # Create random mappings - each mentor gets 2-3 mentees
    mappings = []
    mentee_index = 0
    
    for mentor in mentor_names:
        # Assign 2-3 mentees per mentor randomly
        num_mentees = random.randint(2, min(3, len(mentee_names) - mentee_index))
        
        for i in range(num_mentees):
            if mentee_index < len(mentee_names):
                mappings.append({
                    'Mentor_Name': mentor,
                    'Mentee_Name': mentee_names[mentee_index],
                    'Session_Date': '2025-08-15',
                    'Session_Notes': f'Session between {mentor} and {mentee_names[mentee_index]}'
                })
                mentee_index += 1
    
    return pd.DataFrame(mappings)

def show_progress_tracker(data):
    """Detailed Progress Tracker - Mentor and Mentee Overview with Session Details"""
    st.title("Detailed Progress Tracker")
    st.markdown("### Comprehensive Mentor-Mentee Progress Monitoring")
    
    # Create random mapping if not exists in session state
    if 'mentor_mentee_mapping' not in st.session_state:
        st.session_state.mentor_mentee_mapping = create_random_mentor_mentee_mapping(data)
    
    # Top selector: Mentor or Mentee
    st.subheader("Select View Type")
    view_type = st.selectbox("Choose view:", ["Mentor View", "Mentee View"])
    
    st.markdown("---")
    
    if view_type == "Mentor View":
        show_mentor_view(data)
    else:
        show_mentee_view(data)

def show_mentor_view(data):
    """Mentor Selection & Overview with Mentee Details"""
    
    # 1. Mentor Selection & Overview
    st.subheader("Mentor Selection & Overview")
    
    # Get mentor data from real data files
    mentors_real = data['mentors_real_data'].copy()
    mentees_real = data['mentees_real_data'].copy()
    
    # Clean column names
    mentors_real.columns = mentors_real.columns.str.strip()
    mentees_real.columns = mentees_real.columns.str.strip()
    
    # Use real mentor names
    mentor_names = mentors_real['Mentors from LDP'].dropna().tolist()
    
    # Also get real mentee names for demo purposes
    mentee_names_real = mentees_real['Name'].dropna().tolist()
    
    participants_data = data['all_participants'].copy()
    
    # Add mock engagement data for tracker metrics
    participants_data['Total_Sessions'] = [24, 18, 12, 22, 28, 8, 16, 6, 20, 14, 12, 8, 15, 10, 6, 9, 11, 7, 13, 5]
    participants_data['Sessions_This_Month'] = [4, 3, 2, 5, 6, 1, 3, 1, 4, 2, 2, 1, 3, 2, 0, 2, 2, 1, 3, 1]
    participants_data['Last_Session_Date'] = ['2025-08-15', '2025-08-12', '2025-07-20', '2025-08-18', '2025-08-19', 
                                            '2025-08-05', '2025-08-14', '2025-07-25', '2025-08-16', '2025-08-10',
                                            '2025-08-15', '2025-07-28', '2025-08-17', '2025-08-12', '2025-07-15',
                                            '2025-08-14', '2025-08-11', '2025-08-08', '2025-08-16', '2025-08-06']
    participants_data['Engagement_Status'] = ['Active', 'Active', 'At Risk', 'Active', 'Active', 'At Risk', 'Active', 'At Risk', 'Active', 'Active',
                                             'Active', 'At Risk', 'Active', 'Active', 'Dropped', 'Active', 'Active', 'At Risk', 'Active', 'At Risk']
    participants_data['Goal_Progress'] = [85, 92, 65, 88, 95, 45, 78, 35, 82, 70, 75, 40, 85, 60, 20, 68, 72, 45, 80, 35]
    participants_data['Mentor_Satisfaction'] = [4.5, 4.8, 4.2, 4.7, 4.9, 3.9, 4.3, 3.7, 4.6, 4.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    participants_data['Mentee_Satisfaction'] = [4.2, 4.6, 3.8, 4.4, 4.7, 3.5, 4.1, 3.2, 4.3, 4.0, 4.5, 3.8, 4.6, 4.2, 2.5, 4.3, 4.1, 3.6, 4.4, 3.9]
    
    # Convert numeric columns to proper types
    participants_data['Goal_Progress'] = pd.to_numeric(participants_data['Goal_Progress'], errors='coerce').fillna(0)
    participants_data['Total_Sessions'] = pd.to_numeric(participants_data['Total_Sessions'], errors='coerce').fillna(0)
    participants_data['Sessions_This_Month'] = pd.to_numeric(participants_data['Sessions_This_Month'], errors='coerce').fillna(0)
    participants_data['Mentor_Satisfaction'] = pd.to_numeric(participants_data['Mentor_Satisfaction'], errors='coerce').fillna(0)
    participants_data['Mentee_Satisfaction'] = pd.to_numeric(participants_data['Mentee_Satisfaction'], errors='coerce').fillna(0)
    
    engagement_data = participants_data
    # Use real mentor data instead of filtered participants
    if not mentor_names:
        # Fallback to original data if real data is empty
        mentors_data = engagement_data[engagement_data['Role'] == 'Mentor']
        mentor_names = mentors_data['Name'].tolist()
    
    if not mentor_names:
        st.warning("No mentors found in the system.")
        return
    
    # Add search functionality for mentor selection
    mentor_search = st.text_input("Search for a mentor:", placeholder="Type mentor name...")
    
    # Filter mentors based on search
    if mentor_search:
        filtered_mentors = [name for name in mentor_names if mentor_search.lower() in name.lower()]
        if filtered_mentors:
            mentor_names = filtered_mentors
        else:
            st.warning("No mentors found matching your search.")
            return
    
    selected_mentor = st.selectbox("Select a mentor:", mentor_names)
    
    # Get selected mentor data - create mock data for real mentors
    # Since we're using real mentor names, we need to create mock engagement data
    mock_mentor_data = {
        'Total_Sessions': 24,
        'Sessions_This_Month': 4,
        'Goal_Progress': 85
    }
    mentor_info = mock_mentor_data
    
    # Display mentor summary
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Sessions", mentor_info['Total_Sessions'])
    
    with col2:
        avg_sessions_month = round(mentor_info['Sessions_This_Month'], 1)
        st.metric("Avg Sessions/Month", avg_sessions_month)
    
    with col3:
        # Calculate active mentees percentage (mock calculation)
        active_mentees_pct = 85  # This would be calculated from actual pairing data
        st.metric("% Active Mentees", f"{active_mentees_pct}%")
    
    with col4:
        completion_rate = round(mentor_info['Goal_Progress'], 1)
        st.metric("Program Completion Rate", f"{completion_rate}%")
    
    with col5:
        # Fixed mentor rating to show 5/5.0 as requested
        st.metric("Mentor Rating", "5.0/5.0")
    
    st.markdown("---")
    
    # 2. Mentor's Mentee Overview
    st.subheader("Mentor's Mentee Overview")
    
    # Get mentees for this mentor from random mapping
    mapping_data = st.session_state.mentor_mentee_mapping
    mentor_sessions = mapping_data[mapping_data['Mentor_Name'] == selected_mentor]
    
    if len(mentor_sessions) == 0:
        st.info(f"No mentees assigned to {selected_mentor} in the current mapping.")
        return
    
    # Create mentee overview table
    mentee_overview = []
    for _, session in mentor_sessions.iterrows():
        mentee_name = session['Mentee_Name']
        
        # Create mock data for each mentee since we're using real names
        import random
        random.seed(hash(mentee_name))  # Consistent random data for each mentee
        
        mentee_overview.append({
            'Mentee Name': mentee_name,
            'Sessions Completed': random.randint(8, 25),
            'Avg Sessions/Month': random.randint(2, 6),
            'Goal Progress (%)': random.randint(60, 95),
            'Last Session Date': '2025-08-15',
            'Engagement Status': random.choice(['Active', 'Active', 'Active', 'At Risk'])
        })
    
    if mentee_overview:
        mentee_df = pd.DataFrame(mentee_overview)
        
        # Style the dataframe
        def style_engagement(val):
            if val == 'Active':
                return 'background-color: #10B981; color: white'
            elif val == 'At Risk':
                return 'background-color: #F59E0B; color: white'
            elif val == 'Dropped':
                return 'background-color: #EF4444; color: white'
            return ''
        
        styled_df = mentee_df.style.applymap(style_engagement, subset=['Engagement Status'])
        st.dataframe(styled_df, use_container_width=True)
        
        # 3. Mentee Detail View (when clicked)
        st.markdown("---")
        st.subheader("Mentee Detail View")
        
        selected_mentee = st.selectbox("Select mentee for detailed view:", 
                                     [m['Mentee Name'] for m in mentee_overview])
        
        show_mentee_detail(data, selected_mentee, selected_mentor)

def show_mentee_view(data):
    """Mentee Selection & Overview"""
    
    st.subheader("Mentee Selection & Overview")
    
    # Get mentee data from real data files
    mentors_real = data['mentors_real_data'].copy()
    mentees_real = data['mentees_real_data'].copy()
    
    # Clean column names
    mentors_real.columns = mentors_real.columns.str.strip()
    mentees_real.columns = mentees_real.columns.str.strip()
    
    # Use real mentee names
    mentee_names_real = mentees_real['Name'].dropna().tolist()
    
    participants_data = data['all_participants'].copy()
    
    # Add mock engagement data for tracker metrics
    participants_data['Total_Sessions'] = [24, 18, 12, 22, 28, 8, 16, 6, 20, 14, 12, 8, 15, 10, 6, 9, 11, 7, 13, 5]
    participants_data['Sessions_This_Month'] = [4, 3, 2, 5, 6, 1, 3, 1, 4, 2, 2, 1, 3, 2, 0, 2, 2, 1, 3, 1]
    participants_data['Last_Session_Date'] = ['2025-08-15', '2025-08-12', '2025-07-20', '2025-08-18', '2025-08-19', 
                                            '2025-08-05', '2025-08-14', '2025-07-25', '2025-08-16', '2025-08-10',
                                            '2025-08-15', '2025-07-28', '2025-08-17', '2025-08-12', '2025-07-15',
                                            '2025-08-14', '2025-08-11', '2025-08-08', '2025-08-16', '2025-08-06']
    participants_data['Engagement_Status'] = ['Active', 'Active', 'At Risk', 'Active', 'Active', 'At Risk', 'Active', 'At Risk', 'Active', 'Active',
                                             'Active', 'At Risk', 'Active', 'Active', 'Dropped', 'Active', 'Active', 'At Risk', 'Active', 'At Risk']
    participants_data['Goal_Progress'] = [85, 92, 65, 88, 95, 45, 78, 35, 82, 70, 75, 40, 85, 60, 20, 68, 72, 45, 80, 35]
    participants_data['Mentor_Satisfaction'] = [4.5, 4.8, 4.2, 4.7, 4.9, 3.9, 4.3, 3.7, 4.6, 4.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    participants_data['Mentee_Satisfaction'] = [4.2, 4.6, 3.8, 4.4, 4.7, 3.5, 4.1, 3.2, 4.3, 4.0, 4.5, 3.8, 4.6, 4.2, 2.5, 4.3, 4.1, 3.6, 4.4, 3.9]
    
    # Convert numeric columns to proper types
    participants_data['Goal_Progress'] = pd.to_numeric(participants_data['Goal_Progress'], errors='coerce').fillna(0)
    participants_data['Total_Sessions'] = pd.to_numeric(participants_data['Total_Sessions'], errors='coerce').fillna(0)
    participants_data['Sessions_This_Month'] = pd.to_numeric(participants_data['Sessions_This_Month'], errors='coerce').fillna(0)
    participants_data['Mentor_Satisfaction'] = pd.to_numeric(participants_data['Mentor_Satisfaction'], errors='coerce').fillna(0)
    participants_data['Mentee_Satisfaction'] = pd.to_numeric(participants_data['Mentee_Satisfaction'], errors='coerce').fillna(0)
    
    engagement_data = participants_data
    
    # Use real mentee names instead of filtered participants
    if mentee_names_real:
        mentee_names = mentee_names_real
    else:
        # Fallback to original data if real data is empty
        mentees_data = engagement_data[engagement_data['Role'] == 'Mentee']
        mentee_names = mentees_data['Name'].tolist()
    
    if not mentee_names:
        st.warning("No mentees found in the system.")
        return
    
    # Add search functionality for mentee selection
    mentee_search = st.text_input("Search for a mentee:", placeholder="Type mentee name...")
    
    # Filter mentees based on search
    if mentee_search:
        filtered_mentees = [name for name in mentee_names if mentee_search.lower() in name.lower()]
        if filtered_mentees:
            mentee_names = filtered_mentees
        else:
            st.warning("No mentees found matching your search.")
            return
    
    selected_mentee = st.selectbox("Select a mentee:", mentee_names)
    
    # Find mentor for this mentee from random mapping
    mapping_data = st.session_state.mentor_mentee_mapping
    mentee_sessions = mapping_data[mapping_data['Mentee_Name'] == selected_mentee]
    
    if len(mentee_sessions) > 0:
        mentor_name = mentee_sessions.iloc[0]['Mentor_Name']
        
        # Show mentor profile first as requested
        st.markdown("---")
        st.subheader("Assigned Mentor Profile")
        
        # Get mentor details from real data
        mentors_real = data['mentors_real_data'].copy()
        mentors_real.columns = mentors_real.columns.str.strip()
        mentor_data = mentors_real[mentors_real['Mentors from LDP'] == mentor_name]
        
        if len(mentor_data) > 0:
            mentor_info = mentor_data.iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Name", f"{mentor_info['Mentors from LDP']}")
                st.metric("Position", "Senior Leader")  # Mock position
            with col2:
                st.metric("Location", mentor_info.get('Location', 'N/A'))
                # Mock years of service data
                years_of_service = 5 + hash(mentor_name) % 10
                st.metric("Years of Service", f"{years_of_service} years")
            with col3:
                st.markdown("**Leadership Dashboard Link:**")
                st.markdown(f"[View Dashboard](https://dashboard.example.com/mentor/{mentor_name.replace(' ', '_')})")
                
        show_mentee_detail(data, selected_mentee, mentor_name)
    else:
        st.info("No mentor assigned to this mentee in the current mapping.")

def show_mentee_detail(data, mentee_name, mentor_name):
    """Detailed view for a specific mentee"""
    
    # Get mentee data from all_participants
    participants_data = data['all_participants'].copy()
    
    # Add mock engagement data
    participants_data['Total_Sessions'] = [24, 18, 12, 22, 28, 8, 16, 6, 20, 14, 12, 8, 15, 10, 6, 9, 11, 7, 13, 5]
    participants_data['Last_Session_Date'] = ['2025-08-15', '2025-08-12', '2025-07-20', '2025-08-18', '2025-08-19', 
                                            '2025-08-05', '2025-08-14', '2025-07-25', '2025-08-16', '2025-08-10',
                                            '2025-08-15', '2025-07-28', '2025-08-17', '2025-08-12', '2025-07-15',
                                            '2025-08-14', '2025-08-11', '2025-08-08', '2025-08-16', '2025-08-06']
    participants_data['Engagement_Status'] = ['Active', 'Active', 'At Risk', 'Active', 'Active', 'At Risk', 'Active', 'At Risk', 'Active', 'Active',
                                             'Active', 'At Risk', 'Active', 'Active', 'Dropped', 'Active', 'Active', 'At Risk', 'Active', 'At Risk']
    participants_data['Goal_Progress'] = [85, 92, 65, 88, 95, 45, 78, 35, 82, 70, 75, 40, 85, 60, 20, 68, 72, 45, 80, 35]
    participants_data['Mentor_Satisfaction'] = [4.5, 4.8, 4.2, 4.7, 4.9, 3.9, 4.3, 3.7, 4.6, 4.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    participants_data['Mentee_Satisfaction'] = [4.2, 4.6, 3.8, 4.4, 4.7, 3.5, 4.1, 3.2, 4.3, 4.0, 4.5, 3.8, 4.6, 4.2, 2.5, 4.3, 4.1, 3.6, 4.4, 3.9]
    
    # Since we're using real mentee names, create mock data for them
    import random
    random.seed(hash(mentee_name))  # Consistent data for each mentee
    
    # Create mock mentee info
    mentee_info = {
        'Name': mentee_name,
        'Total_Sessions': random.randint(8, 25),
        'Last_Session_Date': '2025-08-15',
        'Engagement_Status': random.choice(['Active', 'Active', 'Active', 'At Risk']),
        'Goal_Progress': random.randint(60, 95),
        'Mentor_Satisfaction': random.uniform(4.0, 5.0),
        'Mentee_Satisfaction': random.uniform(3.8, 4.8)
    }
    
    # A. Snapshot
    st.subheader(f"{mentee_name} - Snapshot")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sessions with Mentor", mentee_info['Total_Sessions'])
    
    with col2:
        # Mock first session date
        first_session = "2025-01-15"  # This would come from actual session data
        last_session = mentee_info['Last_Session_Date']
        st.metric("Session Date Range", f"{first_session} to {last_session}")
    
    with col3:
        engagement_status = mentee_info['Engagement_Status']
        status_color = {"Active": "🟢", "At Risk": "🟡", "Dropped": "🔴"}.get(engagement_status, "⚪")
        st.metric("Engagement Status", f"{status_color} {engagement_status}")
    
    # B. Goals & Progress
    st.subheader("🎯 Goals & Progress")
    
    # Mock goals data (this would come from actual goals database)
    goals_data = [
        {"Goal": "Improve Leadership Skills", "Progress": mentee_info['Goal_Progress'], "Status": "In Progress"},
        {"Goal": "Develop Communication", "Progress": 75, "Status": "In Progress"},
        {"Goal": "Strategic Thinking", "Progress": 60, "Status": "In Progress"}
    ]
    
    for goal in goals_data:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{goal['Goal']}**")
        with col2:
            st.progress(goal['Progress'] / 100)
        with col3:
            st.write(f"{goal['Progress']}%")
    
    # C. Session Notes
    st.subheader("📝 Session Notes")
    
    # Get session notes for this mentee
    session_notes = data['session_notes'][
        (data['session_notes']['Mentee_Name'] == mentee_name) &
        (data['session_notes']['Mentor_Name'] == mentor_name)
    ]
    
    if len(session_notes) > 0:
        for _, session in session_notes.iterrows():
            with st.expander(f"Session on {session['Session_Date']} ({session['Duration_Minutes']} min)"):
                st.write("**Key Takeaways:**")
                st.write(session['Key_Takeaways'])
                st.write("**Action Items:**")
                st.write(session['Action_Items'])
                st.write("**Mentor Notes:**")
                st.write(session['Mentor_Notes'])
                if pd.notna(session['Next_Session_Date']):
                    st.write(f"**Next Session:** {session['Next_Session_Date']}")
    else:
        st.info("No session notes available for this mentee.")
    
    # D. Feedback & Risks
    st.subheader("💬 Feedback & Risks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Mentor Feedback:**")
        if pd.notna(mentee_info['Mentor_Satisfaction']):
            mentor_satisfaction = data['enhanced_engagement'][
                data['enhanced_engagement']['Participant_Name'] == mentor_name
            ]['Mentor_Satisfaction'].iloc[0] if len(data['enhanced_engagement'][
                data['enhanced_engagement']['Participant_Name'] == mentor_name
            ]) > 0 else 0
            st.metric("Mentor Rating", "5.0/5.0")
        else:
            st.info("No mentor feedback available.")
    
    with col2:
        st.write("**Mentee Feedback:**")
        if pd.notna(mentee_info['Mentee_Satisfaction']):
            st.metric("Mentee Satisfaction", 5.0/5.0)
        else:
            st.info("No mentee feedback available.")
    
    # Automated Alerts
    st.subheader("🚨 Automated Alerts")
    
    alerts = []
    
    # Check for no session in last 30 days
    risk_flag = mentee_info.get('Risk_Flag', '')
    if risk_flag == 'No session in 30 days':
        alerts.append("**No session in last 30 days** - Immediate attention required")
    
    # Check for goals not updated
    if risk_flag == 'Goals not updated':
        alerts.append("**Goals not updated** - Goal progress needs review")
    
    # Check for low engagement
    if mentee_info['Engagement_Status'] == 'At Risk':
        alerts.append("**Low engagement detected** - Consider additional support")
    
    # Check for low goal progress
    if mentee_info['Goal_Progress'] < 50:
        alerts.append("**Low goal progress** - Review and adjust goals")
    
    # Check for low satisfaction
    if mentee_info['Mentee_Satisfaction'] < 3.5:
        alerts.append("**Low satisfaction score** - Schedule feedback session")
    
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("✅ No active alerts for this mentee")
