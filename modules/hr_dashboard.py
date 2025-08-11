import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_hr_dashboard(data):
    """HR Dashboard - Overview of all program metrics"""
    st.title("📊 HR Dashboard - Program Overview")
    st.markdown("### Welcome to the Ivy Leadership & Mentorship Program Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_mentors = len(data['mentors'])
        eligible_mentors = len(data['mentors'][data['mentors']['Eligible_Mentor'] == 'Yes'])
        st.markdown(
            f"""<div class="metric-card">
            <h3>👥 Total Mentors</h3>
            <h2>{total_mentors}</h2>
            <p>{eligible_mentors} eligible</p>
            </div>""", unsafe_allow_html=True
        )
    
    with col2:
        active_pairings = len(data['pairings'][data['pairings']['Status'] == 'Active'])
        completed_pairings = len(data['pairings'][data['pairings']['Status'] == 'Completed'])
        st.markdown(
            f"""<div class="metric-card">
            <h3>🤝 Active Pairings</h3>
            <h2>{active_pairings}</h2>
            <p>{completed_pairings} completed</p>
            </div>""", unsafe_allow_html=True
        )
    
    with col3:
        total_goals = len(data['goals'])
        achieved_goals = len(data['goals'][data['goals']['Status'] == 'Completed'])
        achievement_rate = round((achieved_goals / total_goals) * 100, 1) if total_goals > 0 else 0
        st.markdown(
            f"""<div class="metric-card">
            <h3>🎯 Goal Achievement</h3>
            <h2>{achievement_rate}%</h2>
            <p>{achieved_goals}/{total_goals} goals</p>
            </div>""", unsafe_allow_html=True
        )
    
    with col4:
        green_flags = len(data['engagement'][data['engagement']['Flag'] == 'Green'])
        total_participants = len(data['engagement'])
        engagement_rate = round((green_flags / total_participants) * 100, 1) if total_participants > 0 else 0
        st.markdown(
            f"""<div class="metric-card">
            <h3>📈 High Engagement</h3>
            <h2>{engagement_rate}%</h2>
            <p>{green_flags}/{total_participants} participants</p>
            </div>""", unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Engagement Distribution")
        engagement_counts = data['engagement']['Flag'].value_counts()
        colors = {'Green': '#10B981', 'Yellow': '#F59E0B', 'Red': '#EF4444'}
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
            font_color='white'
        )
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Goals Progress by Cohort")
        goals_by_cohort = data['goals'].groupby(['Cohort', 'Status']).size().unstack(fill_value=0)
        fig_goals = px.bar(
            goals_by_cohort,
            title="SMART Goals Status by Cohort",
            color_discrete_map={
                'Completed': '#10B981',
                'Active': '#3B82F6',
                'Not Started': '#6B7280'
            }
        )
        fig_goals.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="Cohort",
            yaxis_title="Number of Goals"
        )
        st.plotly_chart(fig_goals, use_container_width=True)
    
    # Recent Activity
    st.subheader("🔔 Recent Activity")
    
    # Create mock recent activity
    recent_activity = [
        {"Time": "2 hours ago", "Activity": "New mentee Sarah Johnson completed Goal 1", "Type": "Goal"},
        {"Time": "4 hours ago", "Activity": "Mentor Taj Jamal uploaded session notes", "Type": "Session"},
        {"Time": "6 hours ago", "Activity": "Low engagement alert for Anna Martinez", "Type": "Alert"},
        {"Time": "1 day ago", "Activity": "New resource uploaded: Leadership Styles Overview", "Type": "Resource"},
        {"Time": "1 day ago", "Activity": "Cohort 3 mentorship sessions started", "Type": "Program"}
    ]
    
    for activity in recent_activity:
        icon = {"Goal": "🎯", "Session": "📝", "Alert": "⚠️", "Resource": "📚", "Program": "🚀"}.get(activity["Type"], "📌")
        st.markdown(f"{icon} **{activity['Time']}** - {activity['Activity']}")
    

