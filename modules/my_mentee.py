import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_my_mentee(data, mentor_name):
    """My Mentee - Detailed view of mentor's assigned mentee(s)"""
    st.title("👥 My Mentee")
    st.markdown("### Detailed mentee progress and interaction tracking")
    
    # Get mentor's pairings
    mentor_pairings = data['pairings'][data['pairings']['Mentor'] == mentor_name]
    
    if mentor_pairings.empty:
        st.info("You don't have any assigned mentees at this time.")
        return
    
    # Active mentees
    active_pairings = mentor_pairings[mentor_pairings['Status'] == 'Active']
    
    if active_pairings.empty:
        st.info("You don't have any active mentees at this time.")
        # Show completed mentees
        completed_pairings = mentor_pairings[mentor_pairings['Status'] == 'Completed']
        if not completed_pairings.empty:
            st.subheader("📋 Previously Mentored")
            st.dataframe(completed_pairings[['Mentee', 'Cohort', 'Sessions_Completed', 'Feedback_Summary']], use_container_width=True)
        return
    
    # Select mentee if multiple
    if len(active_pairings) > 1:
        selected_mentee = st.selectbox("Select Mentee:", active_pairings['Mentee'].tolist())
        current_pairing = active_pairings[active_pairings['Mentee'] == selected_mentee].iloc[0]
    else:
        current_pairing = active_pairings.iloc[0]
        selected_mentee = current_pairing['Mentee']
    
    st.subheader(f"📊 {selected_mentee} - Progress Overview")
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sessions Completed", f"{current_pairing['Sessions_Completed']}/{current_pairing['Total_Sessions']}")
    
    with col2:
        completion_rate = (current_pairing['Sessions_Completed'] / current_pairing['Total_Sessions']) * 100
        st.metric("Progress", f"{completion_rate:.0f}%")
    
    with col3:
        st.metric("Cohort", current_pairing['Cohort'])
    
    with col4:
        start_date = pd.to_datetime(current_pairing['Start_Date'])
        days_active = (pd.Timestamp.now() - start_date).days
        st.metric("Days Active", days_active)
    
    # Progress visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Session Progress")
        
        # Create progress bar chart
        sessions_data = {
            'Session': [f"Session {i+1}" for i in range(current_pairing['Total_Sessions'])],
            'Status': ['Completed' if i < current_pairing['Sessions_Completed'] else 'Pending' 
                      for i in range(current_pairing['Total_Sessions'])]
        }
        
        sessions_df = pd.DataFrame(sessions_data)
        fig_progress = px.bar(
            sessions_df,
            x='Session',
            color='Status',
            title="Session Completion Status",
            color_discrete_map={'Completed': '#10B981', 'Pending': '#6B7280'}
        )
        fig_progress.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Mentee Engagement")
        
        # Get mentee engagement data
        mentee_engagement = data['engagement'][data['engagement']['Name'] == selected_mentee]
        
        if not mentee_engagement.empty:
            engagement_data = mentee_engagement.iloc[0]
            
            # Create engagement gauge
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = engagement_data['Engagement_Score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Engagement Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#3B82F6"},
                    'steps': [
                        {'range': [0, 50], 'color': "#FEE2E2"},
                        {'range': [50, 75], 'color': "#FEF3C7"},
                        {'range': [75, 100], 'color': "#D1FAE5"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80}}))
            
            fig_gauge.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.info("Engagement data not available for this mentee.")
    
    # Mentee Goals
    st.subheader("🎯 Mentee Goals")
    
    mentee_goals = data['goals'][data['goals']['Mentee'] == selected_mentee]
    
    if not mentee_goals.empty:
        for _, goal in mentee_goals.iterrows():
            status_color = {
                'Completed': '🟢',
                'Active': '🟡', 
                'Not Started': '🔴'
            }.get(goal['Status'], '⚪')
            
            with st.expander(f"{status_color} {goal['SMART_Goal'][:50]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Full Goal:** {goal['SMART_Goal']}")
                    st.write(f"**Progress:** {goal['Progress']}")
                    st.write(f"**Date Set:** {goal['Date']}")
                
                with col2:
                    st.write(f"**Status:** {goal['Status']}")
                    if goal['Status'] == 'Active':
                        pass
    
    # Session Notes and Feedback
    st.subheader("📝 Session Notes & Feedback")
    
    # Mock session data
    session_notes = [
        {
            'Session': 1,
            'Date': '2025-01-15',
            'Duration': '60 min',
            'Topics': 'Introduction, Goal Setting, Career Aspirations',
            'Notes': 'Great first session. Mentee is eager to learn and has clear career goals.',
            'Action_Items': 'Send career development resources'
        },
        {
            'Session': 2,
            'Date': '2025-01-22',
            'Duration': '45 min',
            'Topics': 'Communication Skills, Feedback Techniques',
            'Notes': 'Discussed active listening techniques. Role-played difficult conversations.',
            'Action_Items': 'Practice techniques before next meeting'
        },
        {
            'Session': 3,
            'Date': '2025-01-29',
            'Duration': '50 min',
            'Topics': 'Leadership Styles, Team Management',
            'Notes': 'Explored different leadership approaches. Discussed current team challenges.',
            'Action_Items': 'Implement new team meeting structure'
        }
    ]
    
    for i, session in enumerate(session_notes[:current_pairing['Sessions_Completed']]):
        with st.expander(f"📅 Session {session['Session']} - {session['Date']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Topics Covered:** {session['Topics']}")
                st.write(f"**Notes:** {session['Notes']}")
                st.write(f"**Action Items:** {session['Action_Items']}")
            
            with col2:
                st.write(f"**Duration:** {session['Duration']}")
                pass
    
    # Feedback Summary
    st.markdown("---")
    st.subheader("💬 Overall Feedback Summary")
    
    st.markdown(f"""
    **Current Status:** {current_pairing['Feedback_Summary']}
    
    **Progress Score:** {current_pairing['Progress_Score']}%
    
    **Mentor Notes:** This mentee shows strong potential and is actively engaged in the development process. 
    Regular check-ins and goal tracking are helping maintain momentum.
    """)
