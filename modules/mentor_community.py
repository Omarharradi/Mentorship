import streamlit as st
import pandas as pd
import plotly.express as px

def show_mentor_community(data):
    """Module 6: Mentor Participation & Community"""
    st.title("🏆 Mentor Participation & Community")
    st.markdown("### Track mentor involvement and celebrate returning mentors")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_mentors = len(data['participation'])
    returning_mentors = len(data['participation'][data['participation']['Returning_Mentor'] == 'Yes'])
    featured_mentors = len(data['participation'][data['participation']['Featured_in_Newsletter'] == 'Yes'])
    avg_success_rate = round(data['participation']['Success_Rate'].mean(), 1)
    
    with col1:
        st.metric("Total Mentors", total_mentors)
    
    with col2:
        st.metric("Returning Mentors", returning_mentors, f"{round(returning_mentors/total_mentors*100, 1)}%")
    
    with col3:
        st.metric("Featured in Newsletter", featured_mentors)
    
    with col4:
        st.metric("Avg Success Rate", f"{avg_success_rate}%")
    
    st.markdown("---")
    
    # Participation Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Mentor Retention by Year")
        # Create retention data
        retention_data = data['participation'].copy()
        retention_data['Years_Count'] = retention_data['Years'].str.count(',') + 1
        
        fig_retention = px.histogram(
            retention_data,
            x='Years_Count',
            title="Distribution of Mentor Participation Years",
            color_discrete_sequence=['#3B82F6']
        )
        fig_retention.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="Number of Years Participated",
            yaxis_title="Number of Mentors"
        )
        st.plotly_chart(fig_retention, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Success Rate Distribution")
        fig_success = px.box(
            data['participation'],
            y='Success_Rate',
            title="Mentor Success Rate Distribution",
            color_discrete_sequence=['#10B981']
        )
        fig_success.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_success, use_container_width=True)
    
    # Mentor Spotlight Section
    st.subheader("⭐ Mentor Spotlight")
    
    # Featured mentors
    featured = data['participation'][data['participation']['Featured_in_Newsletter'] == 'Yes'].copy()
    
    if not featured.empty:
        for _, mentor in featured.iterrows():
            with st.expander(f"🌟 {mentor['Name']} - Featured {mentor['Newsletter_Date']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Years Participated", mentor['Cohorts_Participated'].count(',') + 1)
                
                with col2:
                    st.metric("Total Mentees", int(mentor['Total_Mentees']))
                
                with col3:
                    st.metric("Success Rate", f"{mentor['Success_Rate']}%")
                
                st.write(f"**Cohorts:** {mentor['Cohorts_Participated']}")
                st.write("**Bio:** Experienced leader with a passion for developing emerging talent. Known for innovative mentoring approaches and exceptional mentee outcomes.")
    else:
        st.info("No mentors currently featured in newsletter.")
    
    # Participation Table
    st.subheader("📋 Mentor Participation Overview")
    
    # Style the dataframe
    def style_returning(val):
        if val == 'Yes':
            return 'background-color: #10B981; color: white'
        else:
            return 'background-color: #6B7280; color: white'
    
    def style_featured(val):
        if val == 'Yes':
            return 'background-color: #F59E0B; color: white'
        else:
            return 'background-color: #6B7280; color: white'
    
    display_df = data['participation'][['Name', 'Cohorts_Participated', 'Returning_Mentor', 'Featured_in_Newsletter', 'Total_Mentees', 'Success_Rate']].copy()
    
    styled_df = display_df.style.applymap(style_returning, subset=['Returning_Mentor']).applymap(style_featured, subset=['Featured_in_Newsletter'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Newsletter Management
    st.markdown("---")
    st.subheader("📰 Newsletter Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Upcoming Newsletter Features:**")
        
        # Suggest mentors for featuring
        potential_features = data['participation'][
            (data['participation']['Featured_in_Newsletter'] == 'No') & 
            (data['participation']['Success_Rate'] >= 75)
        ].nlargest(3, 'Success_Rate')
        
        for _, mentor in potential_features.iterrows():
            st.write(f"• **{mentor['Name']}** - {mentor['Success_Rate']}% success rate")
    
    with col2:
        st.write("**Newsletter Actions:**")
        
    # Recognition Program
    st.markdown("---")
    st.subheader("🏅 Recognition Program")
    
    # Awards and recognition
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🥇 Excellence Awards**
        - Top Success Rate: Taj Jamal (100%)
        - Most Mentees: Ghazi Ibrahim (8)
        - Longest Tenure: Ghazi Ibrahim (3 years)
        """)
    
    with col2:
        st.markdown("""
        **🌟 Special Recognition**
        - Innovation in Mentoring
        - Outstanding Feedback Scores
        - Community Leadership
        """)
    
    with col3:
        pass
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pass
    
    with col2:
        st.write("**Export Report:**")
        csv = data['participation'].to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="mentor_participation_report.csv",
            mime="text/csv"
        )
    
    with col3:
        pass

    with col4:
        pass
