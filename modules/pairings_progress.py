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
    
    # Calculate average completion rate
    data['pairings']['completion_rate'] = data['pairings']['Sessions_Completed'] / data['pairings']['Total_Sessions'] * 100
    avg_completion = round(data['pairings']['completion_rate'].mean(), 1)
    
    with col1:
        st.metric("Total Pairings", total_pairings)
    
    with col2:
        st.metric("Active Pairings", active_pairings)
    
    with col3:
        st.metric("Completed Programs", completed_pairings)
    
    with col4:
        st.metric("Avg Session Completion", f"{avg_completion}%")
    
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
    
    # Progress visualization
    st.subheader("📊 Session Progress Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Progress bar chart
        fig_progress = px.bar(
            filtered_pairings,
            x='Mentor',
            y='Sessions_Completed',
            color='Status',
            title="Sessions Completed by Mentor",
            color_discrete_map={'Active': '#3B82F6', 'Completed': '#10B981'}
        )
        fig_progress.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with col2:
        # Completion rate by cohort
        cohort_completion = filtered_pairings.groupby('Cohort')['completion_rate'].mean().reset_index()
        fig_cohort = px.bar(
            cohort_completion,
            x='Cohort',
            y='completion_rate',
            title="Average Completion Rate by Cohort",
            color='completion_rate',
            color_continuous_scale="Greens"
        )
        fig_cohort.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_cohort, use_container_width=True)
    
    # Detailed pairings table
    st.subheader("📋 Detailed Pairings")
    
    # Create display dataframe with progress indicators
    display_df = filtered_pairings.copy()
    display_df['Progress'] = display_df.apply(
        lambda row: f"{row['Sessions_Completed']}/{row['Total_Sessions']} ({row['completion_rate']:.0f}%)", 
        axis=1
    )
    
    # Select columns for display
    display_columns = ['Mentor', 'Mentee', 'Progress', 'Status', 'Cohort', 'Feedback_Summary', 'Action_Items']
    st.dataframe(filtered_pairings[['Mentor', 'Mentee', 'Cohort', 'Status', 'Sessions_Completed', 'Total_Sessions', 'completion_rate']], use_container_width=True)

    st.markdown("---")
    st.subheader("View Mentor's Detailed Progress")
    
    mentor_list = ["None"] + sorted(data['pairings']['Mentor'].unique().tolist())
    selected_mentor_for_detail = st.selectbox("Select a mentor to see their mentee details:", mentor_list)

    if selected_mentor_for_detail != "None":
        show_my_mentee(data, selected_mentor_for_detail)
    
    # Action items summary
    st.markdown("---")
    st.subheader("📝 Open Action Items")
    
    action_items = []
    for _, row in filtered_pairings.iterrows():
        if row['Action_Items'] and row['Status'] == 'Active':
            action_items.append({
                'Mentor': row['Mentor'],
                'Mentee': row['Mentee'],
                'Action': row['Action_Items'],
                'Priority': 'High' if row['Sessions_Completed'] < 2 else 'Medium'
            })
    
    if action_items:
        action_df = pd.DataFrame(action_items)
        
        # Color code by priority
        def highlight_priority(val):
            if val == 'High':
                return 'background-color: #FEE2E2; color: #DC2626'
            else:
                return 'background-color: #FEF3C7; color: #D97706'
        
        styled_actions = action_df.style.applymap(highlight_priority, subset=['Priority'])
        st.dataframe(styled_actions, use_container_width=True)
    else:
        st.info("No open action items at this time.")
    
    # Export functionality
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("📥 Export Progress Report", type="primary"):
            csv = filtered_pairings.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="pairings_progress_report.csv",
                mime="text/csv"
            )
