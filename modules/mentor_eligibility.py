import streamlit as st
import pandas as pd
import plotly.express as px

def show_mentor_eligibility(data):
    """Module 1: Tool Integration (Mentor Eligibility Detection) - HR Only"""
    st.title("🔍 Mentor Eligibility Detection")
    st.markdown("### LDP Methodology Results")
    
    # Analytics Cards
    col1, col2, col3 = st.columns(3)
    
    total_mentors = len(data['mentors'])
    eligible_mentors = len(data['mentors'][data['mentors']['Eligible_Mentor'] == 'Yes'])
    eligibility_rate = round((eligible_mentors / total_mentors) * 100, 1)
    
    with col1:
        st.metric("Total LDP Participants", total_mentors)
    
    with col2:
        st.metric("Eligible Mentors", eligible_mentors, f"{eligibility_rate}%")
    
    with col3:
        st.metric("Data Sync Success", "100%", "✅ Live")
    
    st.markdown("---")
    
    # Search and Filter
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search mentors by name:", placeholder="Enter mentor name...")
    
    with col2:
        filter_eligible = st.selectbox("Filter by eligibility:", ["All", "Eligible Only", "Not Eligible"])
    
    # Filter data
    filtered_data = data['mentors'].copy()
    
    if search_term:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(search_term, case=False, na=False)]
    
    if filter_eligible == "Eligible Only":
        filtered_data = filtered_data[filtered_data['Eligible_Mentor'] == 'Yes']
    elif filter_eligible == "Not Eligible":
        filtered_data = filtered_data[filtered_data['Eligible_Mentor'] == 'No']
    
    # Display table
    st.subheader("📋 Mentor Eligibility Results")
    
    # Style the dataframe
    def style_eligibility(val):
        if val == 'Yes':
            return 'background-color: #10B981; color: white'
        else:
            return 'background-color: #EF4444; color: white'
    
    display_df = filtered_data[['Name', 'LDP_Complete', 'Leadership_Style', 'Eligible_Mentor']].copy()
    styled_df = display_df.style.applymap(style_eligibility, subset=['Eligible_Mentor'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Export functionality
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("📥 Export to CSV", type="primary"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="mentor_eligibility.csv",
                mime="text/csv"
            )
    
    # Leadership Style Distribution
    st.markdown("---")
    st.subheader("📊 Leadership Style Distribution")
    
    style_counts = data['mentors']['Leadership_Style'].value_counts()
    fig = px.bar(
        x=style_counts.index,
        y=style_counts.values,
        title="Distribution of Leadership Styles",
        color=style_counts.values,
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Leadership Style",
        yaxis_title="Number of Mentors"
    )
    st.plotly_chart(fig, use_container_width=True)
