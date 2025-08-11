import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_my_engagement(data, mentor_name):
    """My Engagement - Personal engagement insights for mentor"""
    st.title("📈 My Engagement Insights")
    st.markdown("### Your participation and engagement analytics")
    
    # Get mentor's engagement data
    mentor_engagement = data['engagement'][data['engagement']['Name'] == mentor_name]
    
    if mentor_engagement.empty:
        st.error("Engagement data not found for your profile.")
        return
    
    engagement_data = mentor_engagement.iloc[0]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = engagement_data['Engagement_Score']
        st.metric("Engagement Score", f"{score:.1f}")
    
    with col2:
        flag = engagement_data['Flag']
        flag_emoji = {'Green': '🟢', 'Yellow': '🟡', 'Red': '🔴'}.get(flag, '⚪')
        st.metric("Status Flag", f"{flag_emoji} {flag}")
    
    with col3:
        response_rate = engagement_data['Response_Rate']
        st.metric("Response Rate", f"{response_rate}%")
    
    with col4:
        sessions = engagement_data['Sessions_Attended']
        st.metric("Sessions Attended", sessions)
    
    # Engagement Score Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Your Engagement Score")
        
        # Create gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Engagement Score"},
            delta = {'reference': 70, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
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
                    'value': 85}}))
        
        fig_gauge.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.subheader("📈 Engagement Breakdown")
        
        # Engagement components
        components = {
            'Session Attendance': (engagement_data['Sessions_Attended'] / 5) * 100,  # Assuming max 5 sessions
            'Response Rate': engagement_data['Response_Rate'],
            'Proactive Communication': 100 if engagement_data['Proactive_Communication'] == 'Yes' else 30,
            'EQ Application': (engagement_data['EQ_Score'] / 100) * 100
        }
        
        fig_components = px.bar(
            x=list(components.keys()),
            y=list(components.values()),
            title="Engagement Components",
            color=list(components.values()),
            color_continuous_scale="Blues"
        )
        fig_components.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_components, use_container_width=True)
    
    # Engagement Trends
    st.subheader("📊 Engagement Trends")
    
    # Mock historical data
    dates = pd.date_range(start='2025-01-01', end='2025-01-22', freq='D')
    trend_data = []
    
    base_score = score
    for i, date in enumerate(dates):
        # Create realistic variation around the current score
        variation = (hash(str(date) + mentor_name) % 20 - 10)  # -10 to +10 variation
        daily_score = max(30, min(100, base_score + variation))
        trend_data.append({
            'Date': date,
            'Engagement_Score': daily_score,
            'Sessions': 1 if i % 7 < 2 else 0,  # Mock sessions twice a week
            'Messages': hash(str(date) + mentor_name) % 5  # Mock message activity
        })
    
    trend_df = pd.DataFrame(trend_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trend = px.line(
            trend_df,
            x='Date',
            y='Engagement_Score',
            title="Daily Engagement Score Trend",
            markers=True
        )
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        fig_trend.update_traces(line_color='#10B981', marker_color='#10B981')
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        fig_activity = px.bar(
            trend_df.tail(14),  # Last 2 weeks
            x='Date',
            y='Messages',
            title="Recent Communication Activity",
            color='Messages',
            color_continuous_scale="Greens"
        )
        fig_activity.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_activity, use_container_width=True)
    
    # Performance Insights
    st.subheader("💡 Performance Insights")
    
    # Generate personalized insights based on engagement data
    insights = []
    
    if score >= 80:
        insights.append({
            'type': 'success',
            'title': 'Excellent Engagement!',
            'message': 'You are highly engaged and setting a great example for your mentee.'
        })
    elif score >= 60:
        insights.append({
            'type': 'info',
            'title': 'Good Engagement',
            'message': 'You are doing well. Consider increasing proactive communication for even better results.'
        })
    else:
        insights.append({
            'type': 'warning',
            'title': 'Engagement Needs Attention',
            'message': 'Your engagement score is below optimal. Consider scheduling more regular check-ins.'
        })
    
    if engagement_data['Proactive_Communication'] == 'No':
        insights.append({
            'type': 'info',
            'title': 'Communication Opportunity',
            'message': 'Increase proactive communication with your mentee to boost engagement scores.'
        })
    
    if response_rate < 80:
        insights.append({
            'type': 'warning',
            'title': 'Response Rate',
            'message': f'Your response rate is {response_rate}%. Aim for 90%+ for optimal mentorship.'
        })
    
    for insight in insights:
        if insight['type'] == 'success':
            st.success(f"✅ **{insight['title']}:** {insight['message']}")
        elif insight['type'] == 'warning':
            st.warning(f"⚠️ **{insight['title']}:** {insight['message']}")
        else:
            st.info(f"💡 **{insight['title']}:** {insight['message']}")
    
    # Comparison with Peers
    st.subheader("📊 Peer Comparison")
    
    # Get other mentors' engagement data
    other_mentors = data['engagement'][
        (data['engagement']['Role'] == 'Mentor') & 
        (data['engagement']['Name'] != mentor_name)
    ]
    
    if not other_mentors.empty:
        avg_peer_score = other_mentors['Engagement_Score'].mean()
        avg_peer_response = other_mentors['Response_Rate'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score_diff = score - avg_peer_score
            st.metric(
                "vs Peer Average (Score)", 
                f"{score:.1f}",
                f"{score_diff:+.1f}"
            )
        
        with col2:
            response_diff = response_rate - avg_peer_response
            st.metric(
                "vs Peer Average (Response)", 
                f"{response_rate}%",
                f"{response_diff:+.1f}%"
            )
        
        with col3:
            percentile = (other_mentors['Engagement_Score'] < score).mean() * 100
            st.metric("Your Percentile", f"{percentile:.0f}th")
    
    # Action Plan
    st.subheader("🎯 Personalized Action Plan")
    
    action_items = []
    
    if score < 70:
        action_items.append("📞 Schedule weekly check-ins with your mentee")
        action_items.append("📝 Set up regular session note reviews")
    
    if engagement_data['Proactive_Communication'] == 'No':
        action_items.append("💬 Initiate at least 2 proactive conversations per week")
    
    if response_rate < 85:
        action_items.append("⚡ Aim to respond to mentee messages within 24 hours")
    
    if engagement_data['Sessions_Attended'] < 3:
        action_items.append("📅 Prioritize attending all scheduled mentoring sessions")
    
    action_items.append("📚 Review mentoring best practices resources")
    action_items.append("🤝 Connect with other high-performing mentors")
    
    for i, item in enumerate(action_items, 1):
        st.write(f"{i}. {item}")
    

