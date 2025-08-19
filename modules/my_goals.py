import streamlit as st
import pandas as pd
import plotly.express as px

def show_my_goals(data, mentor_name):
    """My Goals - Mentor's view of their mentee's goals"""
    st.title("🎯 Goals Tracking")
    st.markdown("### Track your mentee's SMART goals and progress")
    
    # Get mentor's mentees and their goals
    mentor_pairings = data['pairings'][data['pairings']['Mentor'] == mentor_name]
    
    if mentor_pairings.empty:
        st.info("You don't have any assigned mentees at this time.")
        return
    
    # Get all mentees for this mentor
    mentee_names = mentor_pairings['Mentee'].tolist()
    mentee_goals = data['goals'][data['goals']['Mentee'].isin(mentee_names)]
    
    if mentee_goals.empty:
        st.info("No goals have been set by your mentees yet.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_goals = len(mentee_goals)
    completed_goals = len(mentee_goals[mentee_goals['Status'] == 'Completed'])
    active_goals = len(mentee_goals[mentee_goals['Status'] == 'Active'])
    not_started = len(mentee_goals[mentee_goals['Status'] == 'Not Started'])
    
    with col1:
        st.metric("Total Goals", total_goals)
    
    with col2:
        st.metric("Completed", completed_goals)
    
    with col3:
        st.metric("In Progress", active_goals)
    
    with col4:
        st.metric("Not Started", not_started)
    
    # Progress visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Goal Status Overview")
        status_counts = mentee_goals['Status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Distribution of Goal Status",
            color_discrete_map={
                'Completed': '#10B981',
                'Active': '#3B82F6',
                'Not Started': '#6B7280'
            }
        )
        fig_status.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        st.subheader("📈 Progress by Mentee")
        if len(mentee_names) > 1:
            mentee_progress = mentee_goals.groupby(['Mentee', 'Status']).size().unstack(fill_value=0)
            fig_mentee = px.bar(
                mentee_progress,
                title="Goal Progress by Mentee",
                color_discrete_map={
                    'Completed': '#10B981',
                    'Active': '#3B82F6',
                    'Not Started': '#6B7280'
                }
            )
            fig_mentee.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_mentee, use_container_width=True)
        else:
            # Single mentee - show timeline
            mentee_name = mentee_names[0]
            st.write(f"**Goals for {mentee_name}:**")
            for status in ['Completed', 'Active', 'Not Started']:
                count = len(mentee_goals[mentee_goals['Status'] == status])
                st.write(f"• {status}: {count}")
    
    # Filter options
    st.subheader("🔍 Filter Goals")
    col1, col2 = st.columns(2)
    
    with col1:
        if len(mentee_names) > 1:
            selected_mentee = st.selectbox("Select Mentee:", ["All"] + mentee_names)
        else:
            selected_mentee = mentee_names[0]
            st.write(f"**Mentee:** {selected_mentee}")
    
    with col2:
        status_filter = st.selectbox("Filter by Status:", ["All", "Completed", "Active", "Not Started"])
    
    # Apply filters
    filtered_goals = mentee_goals.copy()
    
    if len(mentee_names) > 1 and selected_mentee != "All":
        filtered_goals = filtered_goals[filtered_goals['Mentee'] == selected_mentee]
    
    if status_filter != "All":
        filtered_goals = filtered_goals[filtered_goals['Status'] == status_filter]
    
    # Goals detail view
    st.subheader("📋 Goal Details")
    
    if not filtered_goals.empty:
        for _, goal in filtered_goals.iterrows():
            # Status indicator
            status_color = {
                'Completed': '🟢',
                'Active': '🟡',
                'Not Started': '🔴'
            }.get(goal['Status'], '⚪')
            
            with st.expander(f"{status_color} {goal['Mentee']} - {goal['SMART_Goal'][:60]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Mentee:** {goal['Mentee']}")
                    st.write(f"**Goal:** {goal['SMART_Goal']}")
                    st.write(f"**Progress:** {goal['Progress']}")
                    st.write(f"**Date Set:** {goal['Date']}")
                
                with col2:
                    st.write(f"**Status:** {goal['Status']}")
                    st.write(f"**Cohort:** {goal['Cohort']}")
                    
                # Mentor notes section
                st.write("**Mentor Notes:**")
                mentor_note = st.text_area(
                    "Add your observations or guidance:",
                    placeholder="Enter notes about this goal...",
                    key=f"note_{goal['Mentee']}_{goal['Date']}",
                    height=80,
                    disabled=True
                )
                
                st.success("Note saved successfully!")
    else:
        st.info("No goals match the current filters.")
    
    # Goal Setting Assistance
    st.markdown("---")
    st.subheader("💡 Goal Setting Assistance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**SMART Goal Framework:**")
        st.markdown("""
        - **S**pecific: Clear and well-defined
        - **M**easurable: Quantifiable outcomes
        - **A**chievable: Realistic and attainable
        - **R**elevant: Aligned with career goals
        - **T**ime-bound: Has a deadline
        """)
    
    with col2:
        st.write("**Common Goal Categories:**")
        goal_categories = [
            "Communication Skills",
            "Leadership Development", 
            "Technical Competencies",
            "Network Building",
            "Project Management",
            "Public Speaking"
        ]
        
        for category in goal_categories:
            st.write(f"• {category}")
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**Help Set New Goal**")
    
    with col2:
        st.write("**Generate Progress Report**")
    
    with col3:
        st.write("**Send Goal Reminder**")
    
    with col4:
        st.write("**Goal Resources**")
    
    # Progress Insights
    if total_goals > 0:
        st.markdown("---")
        st.subheader("📈 Progress Insights")
        
        completion_rate = (completed_goals / total_goals) * 100
        
        if completion_rate >= 75:
            st.success(f"🎉 Excellent progress! {completion_rate:.1f}% of goals completed.")
        elif completion_rate >= 50:
            st.warning(f"📈 Good progress! {completion_rate:.1f}% of goals completed. Keep encouraging your mentee!")
        else:
            st.error(f"⚠️ Goals need attention! Only {completion_rate:.1f}% completed. Consider additional support.")
        
        # Recommendations
        if not_started > 0:
            st.info(f"💡 **Recommendation:** {not_started} goals haven't been started. Schedule a goal-setting session with your mentee.")
        
        if active_goals > completed_goals:
            st.info(f"💡 **Recommendation:** Focus on completing active goals before setting new ones.")
