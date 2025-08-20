import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_progress_tracker(data):
    """Detailed Progress Tracker - Mentor and Mentee Overview with Session Details"""
    st.title("📊 Detailed Progress Tracker")
    st.markdown("### Comprehensive Mentor-Mentee Progress Monitoring")
    
    # Top selector: Mentor or Mentee
    st.subheader("🔍 Select View Type")
    view_type = st.selectbox("Choose view:", ["Mentor View", "Mentee View"])
    
    st.markdown("---")
    
    if view_type == "Mentor View":
        show_mentor_view(data)
    else:
        show_mentee_view(data)

def show_mentor_view(data):
    """Mentor Selection & Overview with Mentee Details"""
    
    # 1. Mentor Selection & Overview
    st.subheader("👨‍🏫 Mentor Selection & Overview")
    
    # Get mentor data from all_participants
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
    mentors_data = engagement_data[engagement_data['Role'] == 'Mentor']
    mentor_names = mentors_data['Name'].tolist()  # Use 'Name' column from all_participants
    
    if not mentor_names:
        st.warning("No mentors found in the system.")
        return
    
    selected_mentor = st.selectbox("Select a mentor:", mentor_names)
    
    # Get selected mentor data
    mentor_info = mentors_data[mentors_data['Name'] == selected_mentor].iloc[0]
    
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
        satisfaction = mentor_info['Mentor_Satisfaction']
        st.metric("Mentor Satisfaction", f"{satisfaction}/5.0")
    
    st.markdown("---")
    
    # 2. Mentor's Mentee Overview
    st.subheader("👨‍🎓 Mentor's Mentee Overview")
    
    # Get mentees for this mentor (mock data based on session notes)
    session_data = data['session_notes']
    mentor_sessions = session_data[session_data['Mentor_Name'] == selected_mentor]
    
    if len(mentor_sessions) == 0:
        st.info("No mentees assigned to this mentor yet.")
        return
    
    # Create mentee overview table
    mentee_overview = []
    for _, session in mentor_sessions.iterrows():
        mentee_name = session['Mentee_Name']
        
        # Get mentee data
        mentee_data = engagement_data[
            engagement_data['Name'] == mentee_name
        ]
        
        if len(mentee_data) > 0:
            mentee_info = mentee_data.iloc[0]
            mentee_overview.append({
                'Mentee Name': mentee_name,
                'Sessions Completed': mentee_info['Total_Sessions'],
                'Avg Sessions/Month': mentee_info['Sessions_This_Month'],
                'Goal Progress (%)': mentee_info['Goal_Progress'],
                'Last Session Date': mentee_info['Last_Session_Date'],
                'Engagement Status': mentee_info['Engagement_Status']
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
        st.subheader("🔍 Mentee Detail View")
        
        selected_mentee = st.selectbox("Select mentee for detailed view:", 
                                     [m['Mentee Name'] for m in mentee_overview])
        
        show_mentee_detail(data, selected_mentee, selected_mentor)

def show_mentee_view(data):
    """Mentee Selection & Overview"""
    
    st.subheader("👨‍🎓 Mentee Selection & Overview")
    
    # Get mentee data from all_participants
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
    mentees_data = engagement_data[engagement_data['Role'] == 'Mentee']
    mentee_names = mentees_data['Name'].tolist()  # Use 'Name' column from all_participants
    
    if not mentee_names:
        st.warning("No mentees found in the system.")
        return
    
    selected_mentee = st.selectbox("Select a mentee:", mentee_names)
    
    # Find mentor for this mentee
    session_data = data['session_notes']
    mentee_sessions = session_data[session_data['Mentee_Name'] == selected_mentee]
    
    if len(mentee_sessions) > 0:
        mentor_name = mentee_sessions.iloc[0]['Mentor_Name']
        show_mentee_detail(data, selected_mentee, mentor_name)
    else:
        st.info("No mentor assigned to this mentee yet.")

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
    
    mentee_data = participants_data[
        participants_data['Name'] == mentee_name
    ]
    
    if len(mentee_data) == 0:
        st.error("Mentee data not found.")
        return
    
    mentee_info = mentee_data.iloc[0]
    
    # A. Snapshot
    st.subheader(f"📋 {mentee_name} - Snapshot")
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
            st.metric("Mentor Rating", f"{mentor_satisfaction}/5.0")
        else:
            st.info("No mentor feedback available.")
    
    with col2:
        st.write("**Mentee Feedback:**")
        if pd.notna(mentee_info['Mentee_Satisfaction']):
            st.metric("Mentee Satisfaction", f"{mentee_info['Mentee_Satisfaction']}/5.0")
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
