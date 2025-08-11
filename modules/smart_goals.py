import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_smart_goals(data):
    """Module 3: SMART Goal Tracking"""
    st.title("🎯 SMART Goal Tracking")
    st.markdown("### Monitor mentee goal submissions and progress over time")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_goals = len(data['goals'])
    achieved_goals = len(data['goals'][data['goals']['Status'] == 'Completed'])
    in_progress = len(data['goals'][data['goals']['Status'] == 'Active'])
    achievement_rate = round((achieved_goals / total_goals) * 100, 1) if total_goals > 0 else 0
    
    with col1:
        st.metric("Total Goals", total_goals)
    
    with col2:
        st.metric("Achieved Goals", achieved_goals, f"{achievement_rate}%")
    
    with col3:
        st.metric("In Progress", in_progress)
    
    with col4:
        not_started = len(data['goals'][data['goals']['Status'] == 'Not Started'])
        st.metric("Not Started", not_started)
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cohort_filter = st.selectbox("Filter by Cohort:", ["All"] + list(data['goals']['Cohort'].unique()))
    
    with col2:
        status_filter = st.selectbox("Filter by Status:", ["All", "Completed", "Active", "Not Started"])
    
    with col3:
        mentee_search = st.text_input("Search Mentee:", placeholder="Enter mentee name...")
    
    # Apply filters
    filtered_goals = data['goals'].copy()
    
    if cohort_filter != "All":
        filtered_goals = filtered_goals[filtered_goals['Cohort'] == cohort_filter]
    
    if status_filter != "All":
        filtered_goals = filtered_goals[filtered_goals['Status'] == status_filter]
    
    if mentee_search:
        filtered_goals = filtered_goals[filtered_goals['Mentee'].str.contains(mentee_search, case=False, na=False)]
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Goal Progress by Cohort")
        cohort_status = filtered_goals.groupby(['Cohort', 'Status']).size().unstack(fill_value=0)
        fig_cohort = px.bar(
            cohort_status,
            title="Goal Status Distribution by Cohort",
            color_discrete_map={
                'Completed': '#10B981',
                'Active': '#3B82F6',
                'Not Started': '#6B7280'
            }
        )
        fig_cohort.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_cohort, use_container_width=True)
    
    with col2:
        st.subheader("📈 Achievement Rate Trends")
        # Create mock time series data for achievement rates
        dates = pd.date_range(start='2025-01-01', end='2025-02-23', freq='W') # 8 weeks
        achievement_trend = [15, 25, 35, 45, 55, 65, 75, achievement_rate] # 8 values
        
        fig_trend = px.line(
            x=dates,
            y=achievement_trend,
            title="Goal Achievement Rate Over Time",
            markers=True
        )
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="Date",
            yaxis_title="Achievement Rate (%)"
        )
        fig_trend.update_traces(line_color='#10B981', marker_color='#10B981')
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Goals table
    st.subheader("📋 SMART Goals Overview")
    
    # Style the status column
    def style_status(val):
        if val == 'Completed':
            return 'background-color: #10B981; color: white'
        elif val == 'Active':
            return 'background-color: #3B82F6; color: white'
        else:
            return 'background-color: #6B7280; color: white'
    
    display_df = filtered_goals[['Mentee', 'Cohort', 'Date', 'SMART_Goal', 'Progress', 'Status', 'Mentor']].copy()
    styled_df = display_df.style.applymap(style_status, subset=['Status'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Goal themes analysis
    st.markdown("---")
    st.subheader("🔍 Recurring Goal Themes")
    
    # Extract themes from goals (simplified keyword analysis)
    goal_text = ' '.join(filtered_goals['SMART_Goal'].astype(str))
    common_themes = {
        'Communication': goal_text.lower().count('communication'),
        'Leadership': goal_text.lower().count('leadership') + goal_text.lower().count('lead'),
        'Technical Skills': goal_text.lower().count('technical') + goal_text.lower().count('certification'),
        'Networking': goal_text.lower().count('network') + goal_text.lower().count('contact'),
        'Presentation': goal_text.lower().count('presentation') + goal_text.lower().count('speaking'),
        'Project Management': goal_text.lower().count('project')
    }
    
    themes_df = pd.DataFrame(list(common_themes.items()), columns=['Theme', 'Frequency'])
    themes_df = themes_df[themes_df['Frequency'] > 0].sort_values('Frequency', ascending=False)
    
    if not themes_df.empty:
        fig_themes = px.bar(
            themes_df,
            x='Theme',
            y='Frequency',
            title="Most Common Goal Themes",
            color='Frequency',
            color_continuous_scale="Blues"
        )
        fig_themes.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_themes, use_container_width=True)
    else:
        st.info("No common themes identified in current goal set.")
    
    # Export functionality
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("📥 Export Goals Report", type="primary"):
            csv = filtered_goals.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="smart_goals_report.csv",
                mime="text/csv"
            )
    

