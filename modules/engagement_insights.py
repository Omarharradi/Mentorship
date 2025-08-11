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
    
    # Engagement Score Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Engagement Score Distribution")
        fig_hist = px.histogram(
            filtered_engagement,
            x='Engagement_Score',
            color='Flag',
            title="Distribution of Engagement Scores",
            color_discrete_map={'Green': '#10B981', 'Yellow': '#F59E0B', 'Red': '#EF4444'}
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.subheader("🎯 EQ vs Engagement Correlation")
        fig_scatter = px.scatter(
            filtered_engagement,
            x='EQ_Score',
            y='Engagement_Score',
            color='Flag',
            size='Response_Rate',
            hover_data=['Name', 'Role'],
            title="EQ Score vs Engagement Score",
            color_discrete_map={'Green': '#10B981', 'Yellow': '#F59E0B', 'Red': '#EF4444'}
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
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
        
        # Quick action buttons for alerts
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Send Alert Notifications", type="primary"):
                st.success(f"Alert notifications sent to {len(alerts)} participants!")
        
        with col2:
            if st.button("📞 Schedule Interventions", use_container_width=True):
                critical_alerts = len([a for a in alerts if 'Critical' in a['Alert']])
                st.success(f"Intervention meetings scheduled for {critical_alerts} critical cases!")
        
        with col3:
            if st.button("📊 Generate Alert Report", use_container_width=True):
                st.info("Detailed alert report generated and sent to HR team.")
    else:
        st.success("🎉 No active alerts! All participants are showing good engagement.")
    
    # Engagement Trends
    st.markdown("---")
    st.subheader("📈 Engagement Trends Over Time")
    
    # Mock trend data
    dates = pd.date_range(start='2025-01-01', end='2025-01-22', freq='D')
    trend_data = []
    
    for date in dates:
        avg_score = avg_engagement + (hash(str(date)) % 20 - 10)  # Mock variation
        trend_data.append({
            'Date': date,
            'Average_Engagement': max(30, min(100, avg_score)),
            'Green_Count': green_flags + (hash(str(date)) % 4 - 2),
            'Yellow_Count': yellow_flags + (hash(str(date)) % 3 - 1),
            'Red_Count': red_flags + (hash(str(date)) % 2)
        })
    
    trend_df = pd.DataFrame(trend_data)
    
    fig_trend = px.line(
        trend_df,
        x='Date',
        y='Average_Engagement',
        title="Average Engagement Score Trend",
        markers=True
    )
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    fig_trend.update_traces(line_color='#3B82F6', marker_color='#3B82F6')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Export functionality
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("📥 Export Engagement Report", type="primary"):
            csv = filtered_engagement.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="engagement_insights_report.csv",
                mime="text/csv"
            )
