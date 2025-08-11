import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def show_mentor_dashboard(data, mentor_name):
    """Redesigned Mentor Dashboard - matching the provided image"""
    
    # Get mentor-specific data
    mentor_data = data['mentors'][data['mentors']['Name'] == mentor_name].iloc[0]
    profile_data = data['leadership_profiles'][data['leadership_profiles']['Name'] == mentor_name].iloc[0]

    # --- HEADER --- 
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<p style='font-size: 20px; font-weight: bold;'>NAME: {mentor_name}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'>Company: NESMA & PARTNERS</p>", unsafe_allow_html=True)
    with col2:
        st.image('assets/nesma2.png', width=150)
        st.image('assets/Ivy Logo copy.png', width=100)

    st.title("MENTOR DASHBOARD")
    st.markdown("<hr style='border: 1px solid #00b0f0;'>", unsafe_allow_html=True)

    # --- MAIN CONTENT --- 
    col1, col2 = st.columns(2)

    # --- LEFT COLUMN ---
    with col1:
        st.markdown("### Managerial Profile: Mentoring Leader")
        st.markdown("#### Top 5 Managerial Strengths for Mentorship")

        strengths = {
            'Accountability': profile_data['Accountability'],
            'Patience': profile_data['Patience'],
            'Communication': profile_data['Communication'],
            'Supportiveness': profile_data['Supportiveness'],
            'Coaching & Mentoring': profile_data['Coaching_Mentoring']
        }
        strengths_df = pd.DataFrame(list(strengths.items()), columns=['Strength', 'Score'])

        fig_strengths = go.Figure(go.Bar(
            y=strengths_df['Strength'],
            x=strengths_df['Score'],
            orientation='h',
            marker_color='#ff7f0e',
            text=strengths_df['Score'],
            textposition='outside'
        ))
        fig_strengths.update_layout(
            xaxis_title="", yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='black', yaxis_autorange='reversed',
            xaxis=dict(range=[0, 80], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        st.plotly_chart(fig_strengths, use_container_width=True)

        st.markdown("#### Score on 3 crucial Behavioral Tendencies")
        behav_col1, behav_col2, behav_col3 = st.columns(3)
        with behav_col1:
            st.markdown("**Fairness**")
            st.progress(profile_data['Fairness'] / 100)
            st.markdown(f"<h3 style='text-align: center;'>{profile_data['Fairness']}%</h3>", unsafe_allow_html=True)
        with behav_col2:
            st.markdown("**Proactive Approach**")
            st.progress(profile_data['Proactive_Approach'] / 100)
            st.markdown(f"<h3 style='text-align: center;'>{profile_data['Proactive_Approach']}%</h3>", unsafe_allow_html=True)
        with behav_col3:
            st.markdown("**Conflict Management**")
            st.progress(profile_data['Conflict_Management'] / 100)
            st.markdown(f"<h3 style='text-align: center;'>{profile_data['Conflict_Management']}%</h3>", unsafe_allow_html=True)

    # --- RIGHT COLUMN ---
    with col2:
        st.markdown("### EIQ Result:")
        eq_score = mentor_data['EQ_Score']
        percentile = 45 # Mock percentile
        st.markdown(f"**Overall Score:** EQ Score: {eq_score}, Percentile Score: {percentile}")

        # Bell curve for EIQ
        x = np.linspace(eq_score - 30, eq_score + 30, 100)
        y = (1 / (10 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - eq_score) / 10) ** 2)
        fig_bell = go.Figure()
        fig_bell.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', mode='lines', line_color='rgba(255,127,14,0.5)'))
        fig_bell.add_vline(x=eq_score, line_width=3, line_dash="dash", line_color="black")
        fig_bell.update_layout(
            title="", xaxis_title="", yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False)
        )
        st.plotly_chart(fig_bell, use_container_width=True)

        st.markdown("#### Essential Components for Mentorship")
        components = {
            'Adaptable Social Skills': profile_data['Adaptable_Social_Skills'],
            'Social Insight': profile_data['Social_Insight'],
            'Self-control': profile_data['Self_Control'],
            'Conflict-Resolution Knowledge': profile_data['Conflict_Resolution_Knowledge'],
            'Empathy': profile_data['Empathy'],
            'Emotional Reflection': profile_data['Emotional_Reflection'],
            'Positive Mindset': profile_data['Positive_Mindset'],
            'Comfort with Emotions': profile_data['Comfort_with_Emotions'],
            'Recognition of other\'s emotions': profile_data['Recognition_of_others_emotions']
        }
        components_df = pd.DataFrame(list(components.items()), columns=['Component', 'Score'])

        fig_components = go.Figure(go.Bar(
            x=components_df['Component'],
            y=components_df['Score'],
            marker_color='#90ee90',
            text=components_df['Score'],
            textposition='outside'
        ))
        fig_components.update_layout(
            xaxis_title="", yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='black', yaxis=dict(range=[0, 100], showgrid=False, zeroline=False),
            xaxis=dict(showgrid=False, zeroline=False, tickangle=-45)
        )
        st.plotly_chart(fig_components, use_container_width=True)

    # --- CALL TO ACTION --- 
    st.markdown("### Call to Action:")
    st.markdown("""
    - You handle conflict adequately but have room for improvement in finding resolutions.
    - Stay aware of your emotional triggers and responses, and be truthful about your feelings to enhance your life.
    - Practice patience and empathy, considering the impact of your actions on others to improve relationships and avoid misunderstandings.
    
    *Components chosen are based on traits best for mentorship and from the personality assessments taken*
    """)
