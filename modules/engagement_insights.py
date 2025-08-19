import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_engagement_insights(data):
    """Module 4: AI-Powered Engagement Insights"""
    st.title("📈 AI-Powered Engagement Insights")
    st.markdown("### Real-time engagement scores and participation flags")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_participants = len(data['engagement'])
    green_flags = len(data['engagement'][data['engagement']['Flag'] == 'Green'])
    yellow_flags = len(data['engagement'][data['engagement']['Flag'] == 'Yellow'])
    red_flags = len(data['engagement'][data['engagement']['Flag'] == 'Red'])
    
    avg_engagement = round(data['engagement']['Engagement_Score'].mean(), 1)
    
    with col1:
        st.metric("Total Participants", total_participants)
    
    with col2:
        st.metric("High Engagement (Green)", green_flags, f"{round(green_flags/total_participants*100, 1)}%")
    
    with col3:
        st.metric("At Risk (Yellow)", yellow_flags, f"{round(yellow_flags/total_participants*100, 1)}%")
    
    with col4:
        st.metric("Critical (Red)", red_flags, f"{round(red_flags/total_participants*100, 1)}%")
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        role_filter = st.selectbox("Filter by Role:", ["All", "Mentor", "Mentee"])
    
    with col2:
        flag_filter = st.selectbox("Filter by Flag:", ["All", "Green", "Yellow", "Red"])
    
    with col3:
        search_name = st.text_input("Search by Name:", placeholder="Enter name...")
    
    # Apply filters
    filtered_engagement = data['engagement'].copy()
    
    if role_filter != "All":
        filtered_engagement = filtered_engagement[filtered_engagement['Role'] == role_filter]
    
    if flag_filter != "All":
        filtered_engagement = filtered_engagement[filtered_engagement['Flag'] == flag_filter]
    
    if search_name:
        filtered_engagement = filtered_engagement[filtered_engagement['Name'].str.contains(search_name, case=False, na=False)]
    
    # Simple Engagement Overview
    st.subheader("📊 Engagement Overview")
    
    # Simple bar chart showing engagement by flag
    flag_counts = filtered_engagement['Flag'].value_counts()
    fig_simple = px.bar(
        x=flag_counts.index,
        y=flag_counts.values,
        title="Engagement Status Distribution",
        color=flag_counts.index,
        color_discrete_map={'Green': '#10B981', 'Yellow': '#F59E0B', 'Red': '#EF4444'}
    )
    fig_simple.update_layout(
        showlegend=False,
        xaxis_title="Status",
        yaxis_title="Count",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_simple, use_container_width=True)
    
    # Individual Scorecards
    st.subheader("📋 Individual Engagement Scorecards")
    
    # Create styled dataframe
    def style_flags(val):
        if val == 'Green':
            return 'background-color: #10B981; color: white'
        elif val == 'Yellow':
            return 'background-color: #F59E0B; color: white'
        else:
            return 'background-color: #EF4444; color: white'
    
    def style_communication(val):
        if val == 'Yes':
            return 'background-color: #10B981; color: white'
        else:
            return 'background-color: #6B7280; color: white'
    
    display_df = filtered_engagement[['Name', 'Role', 'Engagement_Score', 'Flag', 'Proactive_Communication', 'EQ_Score', 'Sessions_Attended', 'Response_Rate']].copy()
    
    styled_df = display_df.style.applymap(style_flags, subset=['Flag']).applymap(style_communication, subset=['Proactive_Communication'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Alert Logic Section
    st.markdown("---")
    st.subheader("🚨 Alert Logic & Recommendations")
    
    # Calculate alerts based on criteria
    alerts = []
    for _, row in filtered_engagement.iterrows():
        if row['Flag'] == 'Red':
            alerts.append({
                'Name': row['Name'],
                'Alert': 'Critical - Immediate intervention required',
                'Reason': f"Engagement score: {row['Engagement_Score']}, No proactive communication",
                'Action': 'Schedule 1-on-1 meeting within 24 hours'
            })
        elif row['Flag'] == 'Yellow':
            alerts.append({
                'Name': row['Name'],
                'Alert': 'Warning - Monitor closely',
                'Reason': f"Engagement score: {row['Engagement_Score']}, Low activity",
                'Action': 'Send check-in message and resources'
            })
    
    if alerts:
        alert_df = pd.DataFrame(alerts)
        
        def style_alert_level(val):
            if 'Critical' in val:
                return 'background-color: #FEE2E2; color: #DC2626'
            else:
                return 'background-color: #FEF3C7; color: #D97706'
        
        styled_alerts = alert_df.style.applymap(style_alert_level, subset=['Alert'])
        st.dataframe(styled_alerts, use_container_width=True)
        
        # Alert information display only (no action buttons)
        st.info(f"📋 Total alerts: {len(alerts)} | Critical: {len([a for a in alerts if 'Critical' in a['Alert']])} | Warnings: {len([a for a in alerts if 'Warning' in a['Alert']])}")
    else:
        st.success("🎉 No active alerts! All participants are showing good engagement.")
    
    # Simple Summary Statistics
    st.markdown("---")
    st.subheader("📈 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Average Scores:**")
        st.write(f"• Engagement: {avg_engagement}")
        st.write(f"• EQ Score: {filtered_engagement['EQ_Score'].mean():.1f}")
        st.write(f"• Response Rate: {filtered_engagement['Response_Rate'].mean():.1f}%")
    
    with col2:
        st.write("**Participation:**")
        st.write(f"• Total Sessions: {filtered_engagement['Sessions_Attended'].sum()}")
        st.write(f"• Avg Sessions per Person: {filtered_engagement['Sessions_Attended'].mean():.1f}")
        st.write(f"• Active Communicators: {len(filtered_engagement[filtered_engagement['Proactive_Communication'] == 'Yes'])}")

