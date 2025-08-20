import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_hr_dashboard(data):
    """HR Dashboard - Comprehensive Program Overview with Filters and Metrics"""
    st.title("HR Dashboard - Program Overview")
    
    # Recent Activity Section (Top)
    st.subheader("Recent Activity")
    recent_activity = [
        {"Time": "2 hours ago", "Activity": "New mentee Sarah Johnson completed Goal 1", "Type": "Goal"},
        {"Time": "4 hours ago", "Activity": "Mentor Taj Jamal uploaded session notes", "Type": "Session"},
        {"Time": "6 hours ago", "Activity": "Low engagement alert for Anna Martinez", "Type": "Alert"},
        {"Time": "1 day ago", "Activity": "New resource uploaded: Leadership Styles Overview", "Type": "Resource"},
        {"Time": "1 day ago", "Activity": "Cohort 3 mentorship sessions started", "Type": "Program"}
    ]
    
    for activity in recent_activity:
        icon = {"Goal": "🎯", "Session": "📝", "Alert": "⚠️", "Resource": "📚", "Program": "🚀"}.get(activity["Type"], "📌")
        st.markdown(f" **{activity['Time']}** - {activity['Activity']}")
    
    st.markdown("---")
    
    # Filter Options (Top Bar)
    st.subheader("🔍 Filter Options")
    col1, col2 = st.columns(2)
    
    with col1:
        timeframe = st.selectbox("📅 Timeframe Selector:", ["All Time", "This Month", "Last 3 Months"])
    
    with col2:
        cohort_filter = st.selectbox("👥 By Cohort:", ["All Cohorts", "Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"])
    
    st.markdown("---")
    
    # Get filtered data based on selections - use all_participants data
    participants_data = data['all_participants'].copy()
    
    # Add mock engagement data for dashboard metrics
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
    participants_data['Cohort'] = [1, 2, 1, 3, 1, 4, 2, 4, 1, 3, 1, 2, 1, 3, 2, 4, 1, 3, 2, 4]
    participants_data['Risk_Flag'] = ['', '', 'No session in 30 days', '', '', 'Low coverage', '', 'No session in 30 days', '', '',
                                     '', 'No session in 30 days', '', '', 'Personal reasons', '', '', 'Goals not updated', '', 'Low engagement']
    participants_data['Dropout_Reason'] = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Personal reasons', '', '', '', '', '']
    
    # Convert numeric columns to proper types
    participants_data['Goal_Progress'] = pd.to_numeric(participants_data['Goal_Progress'], errors='coerce').fillna(0)
    participants_data['Total_Sessions'] = pd.to_numeric(participants_data['Total_Sessions'], errors='coerce').fillna(0)
    participants_data['Sessions_This_Month'] = pd.to_numeric(participants_data['Sessions_This_Month'], errors='coerce').fillna(0)
    participants_data['Mentor_Satisfaction'] = pd.to_numeric(participants_data['Mentor_Satisfaction'], errors='coerce').fillna(0)
    participants_data['Mentee_Satisfaction'] = pd.to_numeric(participants_data['Mentee_Satisfaction'], errors='coerce').fillna(0)
    
    engagement_data = participants_data
    
    if cohort_filter != "All Cohorts":
        cohort_num = int(cohort_filter.split()[-1])
        engagement_data = engagement_data[engagement_data['Cohort'] == cohort_num]
    
    # Program Overview (Top Section)
    st.subheader("Program Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    mentors_count = len(engagement_data[engagement_data['Role'] == 'Mentor'])
    mentees_count = len(engagement_data[engagement_data['Role'] == 'Mentee'])
    total_participants = len(engagement_data)
    # Ensure Goal_Progress is numeric before comparison
    engagement_data['Goal_Progress'] = pd.to_numeric(engagement_data['Goal_Progress'], errors='coerce').fillna(0)
    completed_programs = len(engagement_data[engagement_data['Goal_Progress'] >= 90])
    completion_rate = round((completed_programs / total_participants) * 100, 1) if total_participants > 0 else 0
    
    with col1:
        st.metric("# of Mentors", mentors_count)
    
    with col2:
        st.metric("# of Mentees", mentees_count)
    
    with col3:
        st.metric("Total Participants", total_participants)
    
    with col4:
        st.metric("Program Completion Rate", f"{completion_rate}%")
    
    # Engagement Metrics (Middle Section)
    st.subheader("Engagement Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Calculate engagement metrics
    active_participants = len(engagement_data[engagement_data['Engagement_Status'] == 'Active'])
    overall_engagement_rate = round((active_participants / total_participants) * 100, 1) if total_participants > 0 else 0
    
    mentors_data = engagement_data[engagement_data['Role'] == 'Mentor']
    avg_mentor_sessions = round(mentors_data['Total_Sessions'].mean(), 1) if len(mentors_data) > 0 else 0
    
    mentees_data = engagement_data[engagement_data['Role'] == 'Mentee']
    avg_mentee_sessions = round(mentees_data['Total_Sessions'].mean(), 1) if len(mentees_data) > 0 else 0
    
    total_sessions = engagement_data['Total_Sessions'].sum()
    avg_sessions_per_mentor = round(mentors_data['Total_Sessions'].mean(), 1) if len(mentors_data) > 0 else 0
    
    with col1:
        st.metric("Overall Engagement Rate", f"{overall_engagement_rate}%")
    
    with col2:
        st.metric("Avg Mentor Sessions", f"{avg_mentor_sessions}")
    
    with col3:
        st.metric("Avg Mentee Sessions", f"{avg_mentee_sessions}")
    
    with col4:
        st.metric("Total Sessions Completed", total_sessions)
    
    with col5:
        st.metric("Avg Sessions per Mentor", f"{avg_sessions_per_mentor}")
    
    st.markdown("---")
    
    # Satisfaction & Progress (Middle-Lower Section)
    st.subheader("Satisfaction & Progress")
    col1, col2, col3 = st.columns(3)
    
    # Calculate satisfaction metrics
    mentor_satisfaction = round(mentors_data['Mentor_Satisfaction'].mean(), 1) if len(mentors_data) > 0 else 0
    mentee_satisfaction = round(engagement_data['Mentee_Satisfaction'].mean(), 1) if len(engagement_data) > 0 else 0
    
    # Goal progress (Goal_Progress already converted to numeric above)
    goal_progress_participants = len(engagement_data[engagement_data['Goal_Progress'] > 0])
    goal_progress_rate = round((goal_progress_participants / total_participants) * 100, 1) if total_participants > 0 else 0
    
    with col1:
        st.metric("Mentor Satisfaction Rate", f"{mentor_satisfaction}/5.0")
    
    with col2:
        st.metric("Mentee Satisfaction Rate", f"{mentee_satisfaction}/5.0")
    
    with col3:
        st.metric("Overall Goal Progress", f"{goal_progress_rate}%")
    
    st.markdown("---")
    
    # Risks & Dropouts (Bottom Section)
    st.subheader("Risks & Dropouts")
    
    # Calculate risk metrics
    dropped_mentors = len(engagement_data[(engagement_data['Role'] == 'Mentor') & (engagement_data['Engagement_Status'] == 'Dropped')])
    dropped_mentees = len(engagement_data[(engagement_data['Role'] == 'Mentee') & (engagement_data['Engagement_Status'] == 'Dropped')])
    
    # Handle Risk_Flag safely in case column doesn't exist
    if 'Risk_Flag' in engagement_data.columns:
        no_session_30_days = len(engagement_data[engagement_data['Risk_Flag'] == 'No session in 30 days'])
        low_coverage_mentors = len(engagement_data[engagement_data['Risk_Flag'] == 'Low coverage'])
    else:
        no_session_30_days = 0
        low_coverage_mentors = 0
    
    dropped_mentor_rate = round((dropped_mentors / mentors_count) * 100, 1) if mentors_count > 0 else 0
    dropped_mentee_rate = round((dropped_mentees / mentees_count) * 100, 1) if mentees_count > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Dropped Mentors Rate", f"{dropped_mentor_rate}%", f"{dropped_mentors} mentors")
    
    with col2:
        st.metric("Dropped Mentees Rate", f"{dropped_mentee_rate}%", f"{dropped_mentees} mentees")
    
    with col3:
        st.metric("No Session in 30 Days", no_session_30_days)
    
    with col4:
        st.metric("Low Coverage Mentors", low_coverage_mentors)
    
    # Risk Details
    st.subheader("Risk Details")
    
    # At-risk participants
    at_risk_data = engagement_data[engagement_data['Engagement_Status'] == 'At Risk']
    if len(at_risk_data) > 0:
        st.warning(f"**{len(at_risk_data)} participants at risk:**")
        for _, participant in at_risk_data.iterrows():
            reason = participant.get('Risk_Flag', 'General risk') if participant.get('Risk_Flag') else 'General risk'
            st.markdown(f"• **{participant['Name']}** ({participant['Role']}) - {reason}")
    
    # Dropout reasons
    dropped_data = engagement_data[engagement_data['Engagement_Status'] == 'Dropped']
    if len(dropped_data) > 0:
        st.error(f"**{len(dropped_data)} participants dropped:**")
        for _, participant in dropped_data.iterrows():
            reason = participant['Dropout_Reason'] if pd.notna(participant['Dropout_Reason']) else 'Reason not specified'
            st.markdown(f"• **{participant['Name']}** ({participant['Role']}) - {reason}")
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement Status Distribution")
        engagement_counts = engagement_data['Engagement_Status'].value_counts()
        colors = {'Active': '#10B981', 'At Risk': '#F59E0B', 'Dropped': '#EF4444'}
        fig_engagement = px.pie(
            values=engagement_counts.values,
            names=engagement_counts.index,
            color=engagement_counts.index,
            color_discrete_map=colors,
            title="Participant Engagement Status"
        )
        fig_engagement.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2d3748'
        )
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with col2:
        st.subheader("Goal Progress Distribution")
        # Create goal progress bins
        engagement_data_copy = engagement_data.copy()
        engagement_data_copy['Progress_Bin'] = pd.cut(engagement_data_copy['Goal_Progress'], 
                                                     bins=[0, 25, 50, 75, 100], 
                                                     labels=['0-25%', '26-50%', '51-75%', '76-100%'])
        progress_counts = engagement_data_copy['Progress_Bin'].value_counts()
        
        fig_progress = px.bar(
            x=progress_counts.index,
            y=progress_counts.values,
            title="Goal Progress Distribution",
            color=progress_counts.values,
            color_continuous_scale=['#fed7aa', '#ff6b35']
        )
        fig_progress.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2d3748',
            xaxis_title="Progress Range",
            yaxis_title="Number of Participants"
        )
        st.plotly_chart(fig_progress, use_container_width=True)

