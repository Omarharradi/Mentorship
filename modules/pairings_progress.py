import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.my_mentee import show_my_mentee

def show_pairings_progress(data):
    """Module 2: Mentor-Mentee Pairings & Progress Tracker"""
    st.title("👥 Mentor-Mentee Pairings & Progress")
    st.markdown("### Track active pairings and session progress")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_pairings = len(data['pairings'])
    active_pairings = len(data['pairings'][data['pairings']['Status'] == 'Active'])
    completed_pairings = len(data['pairings'][data['pairings']['Status'] == 'Completed'])
    
    # Calculate completion rate and progress score
    data['pairings']['completion_rate'] = data['pairings']['Sessions_Completed'] / data['pairings']['Total_Sessions'] * 100
    avg_completion = round(data['pairings']['completion_rate'].mean(), 1)
    avg_progress = round(data['pairings']['Progress_Score'].mean(), 1)
    
    with col1:
        st.metric("Total Pairings", total_pairings)
    
    with col2:
        st.metric("Active Pairings", active_pairings)
    
    with col3:
        st.metric("Completed Programs", completed_pairings)
    
    with col4:
        st.metric("Avg Progress Score", f"{avg_progress}%")
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cohort_filter = st.selectbox("Filter by Cohort:", ["All"] + list(data['pairings']['Cohort'].unique()))
    
    with col2:
        status_filter = st.selectbox("Filter by Status:", ["All", "Active", "Completed"])
    
    with col3:
        search_mentor = st.text_input("Search Mentor:", placeholder="Enter mentor name...")
    
    # Apply filters
    filtered_pairings = data['pairings'].copy()
    
    if cohort_filter != "All":
        filtered_pairings = filtered_pairings[filtered_pairings['Cohort'] == cohort_filter]
    
    if status_filter != "All":
        filtered_pairings = filtered_pairings[filtered_pairings['Status'] == status_filter]
    
    if search_mentor:
        filtered_pairings = filtered_pairings[filtered_pairings['Mentor'].str.contains(search_mentor, case=False, na=False)]
    
    # Progress Tracker Dashboard
    st.subheader("🎯 Progress Tracker Dashboard")
    
    # Progress overview by mentor
    mentor_progress = filtered_pairings.groupby('Mentor').agg({
        'Progress_Score': 'mean',
        'Sessions_Completed': 'sum',
        'Total_Sessions': 'sum',
        'Mentee': 'count'
    }).reset_index()
    mentor_progress.columns = ['Mentor', 'Avg_Progress_Score', 'Total_Sessions_Completed', 'Total_Sessions_Planned', 'Mentee_Count']
    mentor_progress['Overall_Completion'] = (mentor_progress['Total_Sessions_Completed'] / mentor_progress['Total_Sessions_Planned'] * 100).round(1)
    
    # Simple progress visualization
    fig_progress = px.bar(
        mentor_progress,
        x='Mentor',
        y='Avg_Progress_Score',
        title="Average Progress Score by Mentor",
        color='Avg_Progress_Score',
        color_continuous_scale="RdYlGn",
        text='Mentee_Count'
    )
    fig_progress.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_tickangle=-45,
        showlegend=False
    )
    fig_progress.update_traces(texttemplate='%{text} mentees', textposition='outside')
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Progress Tracker Table
    st.subheader("📋 Progress Tracker")
    
    # Create enhanced display dataframe
    display_df = filtered_pairings.copy()
    display_df['Session_Progress'] = display_df.apply(
        lambda row: f"{row['Sessions_Completed']}/{row['Total_Sessions']}", 
        axis=1
    )
    display_df['Progress_Status'] = display_df['Progress_Score'].apply(
        lambda x: '🔴 Needs Attention' if x < 50 else '🟡 In Progress' if x < 80 else '🟢 Excellent'
    )
    
    # Display enhanced table with progress tracking
    progress_columns = ['Mentor', 'Mentee', 'Session_Progress', 'Progress_Score', 'Progress_Status', 'Status', 'Cohort']
    st.dataframe(display_df[progress_columns], use_container_width=True)

    st.markdown("---")
    st.subheader("View Mentor's Detailed Progress")
    
    mentor_list = ["None"] + sorted(data['pairings']['Mentor'].unique().tolist())
    selected_mentor_for_detail = st.selectbox("Select a mentor to see their mentee details:", mentor_list)

    if selected_mentor_for_detail != "None":
        show_my_mentee(data, selected_mentor_for_detail)
    
    # Progress Tracker Dashboard
    st.markdown("---")
    st.subheader("🎯 Progress Tracker Dashboard")
    
    # Calculate key metrics for progress bars
    excellent = len(filtered_pairings[filtered_pairings['Progress_Score'] >= 80])
    good = len(filtered_pairings[(filtered_pairings['Progress_Score'] >= 50) & (filtered_pairings['Progress_Score'] < 80)])
    needs_attention = len(filtered_pairings[filtered_pairings['Progress_Score'] < 50])
    total_pairings_filtered = len(filtered_pairings)
    
    mentor_counts = filtered_pairings['Mentor'].value_counts()
    total_planned = filtered_pairings['Total_Sessions'].sum()
    total_completed = filtered_pairings['Sessions_Completed'].sum()
    overall_completion = (total_completed/total_planned*100) if total_planned > 0 else 0
    avg_progress_score = filtered_pairings['Progress_Score'].mean()
    
    # Progress Tracking Cards with Visual Indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏆 Progress Distribution Tracker**")
        
        # Excellent Progress Bar
        excellent_pct = (excellent / total_pairings_filtered * 100) if total_pairings_filtered > 0 else 0
        st.markdown(f"🟢 **Excellent Progress** ({excellent}/{total_pairings_filtered})")
        st.progress(excellent_pct / 100)
        st.caption(f"{excellent_pct:.1f}% of mentorships")
        
        # Good Progress Bar
        good_pct = (good / total_pairings_filtered * 100) if total_pairings_filtered > 0 else 0
        st.markdown(f"🟡 **Good Progress** ({good}/{total_pairings_filtered})")
        st.progress(good_pct / 100)
        st.caption(f"{good_pct:.1f}% of mentorships")
        
        # Needs Attention Progress Bar
        attention_pct = (needs_attention / total_pairings_filtered * 100) if total_pairings_filtered > 0 else 0
        st.markdown(f"🔴 **Needs Attention** ({needs_attention}/{total_pairings_filtered})")
        st.progress(attention_pct / 100)
        st.caption(f"{attention_pct:.1f}% of mentorships")
    
    with col2:
        st.markdown("**👥 Mentor Load Tracker**")
        
        # Average Progress Score
        st.markdown(f"🎯 **Average Progress Score**")
        st.progress(avg_progress_score / 100)
        st.caption(f"{avg_progress_score:.1f}% overall progress")
        
        # Mentor Distribution
        max_mentees = mentor_counts.max() if len(mentor_counts) > 0 else 0
        avg_mentees = mentor_counts.mean() if len(mentor_counts) > 0 else 0
        
        st.markdown(f"📈 **Mentor Capacity**")
        capacity_usage = (avg_mentees / 5 * 100) if avg_mentees > 0 else 0  # Assuming max 5 mentees per mentor
        st.progress(min(capacity_usage / 100, 1.0))
        st.caption(f"Avg: {avg_mentees:.1f} mentees/mentor (Max: {max_mentees})")
        
        st.markdown(f"👤 **Active Mentors**")
        mentor_utilization = (len(mentor_counts) / 10 * 100)  # Assuming target of 10 active mentors
        st.progress(min(mentor_utilization / 100, 1.0))
        st.caption(f"{len(mentor_counts)} mentors active")
    
    with col3:
        st.markdown("**📅 Session Progress Tracker**")
        
        # Overall Session Completion
        st.markdown(f"🏁 **Overall Session Completion**")
        st.progress(overall_completion / 100)
        st.caption(f"{overall_completion:.1f}% sessions completed")
        
        # Sessions Completed vs Planned
        st.markdown(f"📋 **Sessions Completed**")
        st.progress(total_completed / total_planned if total_planned > 0 else 0)
        st.caption(f"{total_completed}/{total_planned} sessions")
        
        # Active vs Completed Programs
        active_programs = len(filtered_pairings[filtered_pairings['Status'] == 'Active'])
        completed_programs = len(filtered_pairings[filtered_pairings['Status'] == 'Completed'])
        total_programs = active_programs + completed_programs
        
        st.markdown(f"✅ **Program Completion Rate**")
        program_completion = (completed_programs / total_programs * 100) if total_programs > 0 else 0
        st.progress(program_completion / 100)
        st.caption(f"{completed_programs}/{total_programs} programs completed")
    
    # Real-time Mentor Performance Tracker
    st.markdown("---")
    st.subheader("🔍 Real-time Mentor Performance Tracker")
    
    # Show mentors with multiple mentees with progress bars
    multi_mentee_mentors = mentor_progress[mentor_progress['Mentee_Count'] > 1].sort_values('Mentee_Count', ascending=False)
    if not multi_mentee_mentors.empty:
        st.markdown("**🎆 High-Capacity Mentors Performance:**")
        
        for _, mentor in multi_mentee_mentors.iterrows():
            col_mentor, col_progress = st.columns([2, 1])
            
            with col_mentor:
                st.markdown(f"**{mentor['Mentor']}**")
                st.caption(f"{mentor['Mentee_Count']} mentees • {mentor['Total_Sessions_Completed']}/{mentor['Total_Sessions_Planned']} sessions")
                
                # Progress bar for this mentor
                st.progress(mentor['Avg_Progress_Score'] / 100)
            
            with col_progress:
                st.metric(
                    label="Avg Progress",
                    value=f"{mentor['Avg_Progress_Score']:.1f}%",
                    delta=f"+{mentor['Avg_Progress_Score'] - avg_progress_score:.1f}%" if mentor['Avg_Progress_Score'] > avg_progress_score else f"{mentor['Avg_Progress_Score'] - avg_progress_score:.1f}%"
                )
    


