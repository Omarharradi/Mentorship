import streamlit as st
import pandas as pd
import plotly.express as px

def show_mentor_eligibility(data):
    """All Participants Directory - Mentors and Mentees with Details"""
    st.title("👥 All Participants Directory")
    st.markdown("### Complete List of Mentors and Mentees")
    
    # Get participant data
    participants = data['all_participants']
    mentors = participants[participants['Role'] == 'Mentor']
    mentees = participants[participants['Role'] == 'Mentee']
    
    # Analytics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Participants", len(participants))
    
    with col2:
        st.metric("Mentors", len(mentors))
    
    with col3:
        st.metric("Mentees", len(mentees))
    
    with col4:
        st.metric("Eligible Mentors", len(mentors[mentors['Eligible_Mentor'] == 'Yes']))
    
    st.markdown("---")
    
    # Search and Filter
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search participants by name:", placeholder="Enter participant name...")
    
    with col2:
        role_filter = st.selectbox("Filter by role:", ["All Participants", "Mentors Only", "Mentees Only"])
    
    with col3:
        location_filter = st.selectbox("Filter by location:", ["All Locations"] + list(participants['Location'].unique()))
    
    # Filter data
    filtered_data = participants.copy()
    
    if search_term:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(search_term, case=False, na=False)]
    
    if role_filter == "Mentors Only":
        filtered_data = filtered_data[filtered_data['Role'] == 'Mentor']
    elif role_filter == "Mentees Only":
        filtered_data = filtered_data[filtered_data['Role'] == 'Mentee']
    
    if location_filter != "All Locations":
        filtered_data = filtered_data[filtered_data['Location'] == location_filter]
    
    # Display comprehensive participant lists
    st.subheader("📋 All Participants List")
    
    # Display participant details with Name, Email, Grade, Location
    display_columns = ['Name', 'Email', 'Grade', 'Location', 'Role']
    
    # Add eligibility status for mentors
    if 'Eligible_Mentor' in filtered_data.columns:
        display_columns.append('Eligible_Mentor')
    
    display_df = filtered_data[display_columns].copy()
    
    # Style the dataframe for role and eligibility
    def style_role(val):
        if val == 'Mentor':
            return 'background-color: #ff6b35; color: white; font-weight: bold'
        elif val == 'Mentee':
            return 'background-color: #fed7aa; color: #2d3748; font-weight: bold'
        return ''
    
    def style_eligibility(val):
        if val == 'Yes':
            return 'background-color: #10B981; color: white'
        elif val == 'No':
            return 'background-color: #EF4444; color: white'
        return ''
    
    styled_df = display_df.style.applymap(style_role, subset=['Role'])
    if 'Eligible_Mentor' in display_df.columns:
        styled_df = styled_df.applymap(style_eligibility, subset=['Eligible_Mentor'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Separate Mentor and Mentee Lists
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍🏫 Mentors List")
        mentor_list = participants[participants['Role'] == 'Mentor'][['Name', 'Email', 'Grade', 'Location', 'Eligible_Mentor']]
        if len(mentor_list) > 0:
            st.dataframe(mentor_list, use_container_width=True)
        else:
            st.info("No mentors found.")
    
    with col2:
        st.subheader("👨‍🎓 Mentees List")
        mentee_list = participants[participants['Role'] == 'Mentee'][['Name', 'Email', 'Grade', 'Location']]
        if len(mentee_list) > 0:
            st.dataframe(mentee_list, use_container_width=True)
        else:
            st.info("No mentees found.")
    
    # Export functionality
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📥 Export All Participants", type="primary"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download All Participants CSV",
                data=csv,
                file_name="all_participants.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Export Mentors Only"):
            mentors_csv = mentor_list.to_csv(index=False)
            st.download_button(
                label="Download Mentors CSV",
                data=mentors_csv,
                file_name="mentors_list.csv",
                mime="text/csv"
            )
    
    # Location Distribution
    st.markdown("---")
    st.subheader("📍 Participants by Location")
    
    location_counts = participants['Location'].value_counts()
    fig = px.pie(
        values=location_counts.values,
        names=location_counts.index,
        title="Distribution of Participants by Location",
        color_discrete_sequence=['#ff6b35', '#fed7aa', '#fff5f0']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#2d3748'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Role Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Role Distribution")
        role_counts = participants['Role'].value_counts()
        fig_role = px.bar(
            x=role_counts.index,
            y=role_counts.values,
            title="Mentors vs Mentees",
            color=role_counts.values,
            color_continuous_scale=['#fed7aa', '#ff6b35']
        )
        fig_role.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2d3748',
            xaxis_title="Role",
            yaxis_title="Number of Participants"
        )
        st.plotly_chart(fig_role, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Mentor Eligibility")
        eligible_counts = mentors['Eligible_Mentor'].value_counts()
        fig_eligible = px.pie(
            values=eligible_counts.values,
            names=eligible_counts.index,
            title="Mentor Eligibility Status",
            color_discrete_sequence=['#10B981', '#EF4444']
        )
        fig_eligible.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2d3748'
        )
        st.plotly_chart(fig_eligible, use_container_width=True)
