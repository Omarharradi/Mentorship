import streamlit as st
import pandas as pd
import plotly.express as px

def show_mentor_eligibility(data):
    """All Participants Directory - Mentors and Mentees with Details"""
    st.title("All Participants Directory")
    st.markdown("### Complete List of Mentors and Mentees")
    
    # Get participant data from real data files
    mentors_real = data['mentors_real_data'].copy()
    mentees_real = data['mentees_real_data'].copy()
    
    # Clean column names
    mentors_real.columns = mentors_real.columns.str.strip()
    mentees_real.columns = mentees_real.columns.str.strip()
    
    # Create combined participants data from real data
    mentors_df = pd.DataFrame({
        'Name': mentors_real['Mentors from LDP'],
        'Email': mentors_real['Email'],
        'Grade': 'Senior',  # Mock grade
        'Location': mentors_real['Location'],
        'Role': 'Mentor',
        'Eligible_Mentor': 'Yes'
    })
    
    mentees_df = pd.DataFrame({
        'Name': mentees_real['Name'],
        'Email': mentees_real['Email'],
        'Grade': mentees_real['Postion'],
        'Location': mentees_real['Location'],
        'Role': 'Mentee'
    })
    
    # Combine mentors and mentees
    participants = pd.concat([mentors_df, mentees_df], ignore_index=True)
    mentors = mentors_df
    mentees = mentees_df
    
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
        search_term = st.text_input("Search participants by name:", placeholder="Enter participant name...")
    
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
    st.subheader("All Participants List")
    
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
        st.subheader("Mentors List")
        mentor_list = mentors[['Name', 'Email', 'Grade', 'Location', 'Eligible_Mentor']]
        if len(mentor_list) > 0:
            st.dataframe(mentor_list, use_container_width=True)
        else:
            st.info("No mentors found.")
    
    with col2:
        st.subheader("Mentees List")
        mentee_list = mentees[['Name', 'Email', 'Grade', 'Location']]
        if len(mentee_list) > 0:
            st.dataframe(mentee_list, use_container_width=True)
        else:
            st.info("No mentees found.")
    
    # Export functionality
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("Export All Participants", type="primary"):
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download All Participants CSV",
                data=csv,
                file_name="all_participants.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export Mentors Only"):
            mentors_csv = mentor_list.to_csv(index=False)
            st.download_button(
                label="Download Mentors CSV",
                data=mentors_csv,
                file_name="mentors_list.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Export Mentees Only"):
            mentees_csv = mentee_list.to_csv(index=False)
            st.download_button(
                label="Download Mentees CSV",
                data=mentees_csv,
                file_name="mentees_list.csv",
                mime="text/csv"
            )
    
    # Location Distribution
    st.markdown("---")
    st.subheader("Participants by Location")
    
    # Add filters for location graph
    col1, col2 = st.columns(2)
    with col1:
        location_role_filter = st.selectbox("Filter by role for location chart:", ["All Participants", "Mentors Only", "Mentees Only"], key="location_role")
    with col2:
        cohort_filter = st.selectbox("Filter by cohort:", ["All Cohorts"] + [f"Cohort {i}" for i in range(1, 5)], key="location_cohort")
    
    # Filter data for location chart
    location_filtered_data = participants.copy()
    if location_role_filter == "Mentors Only":
        location_filtered_data = location_filtered_data[location_filtered_data['Role'] == 'Mentor']
    elif location_role_filter == "Mentees Only":
        location_filtered_data = location_filtered_data[location_filtered_data['Role'] == 'Mentee']
    
    # Add cohort data if not exists (mock data)
    if 'Cohort' not in location_filtered_data.columns:
        import random
        location_filtered_data['Cohort'] = [random.randint(1, 4) for _ in range(len(location_filtered_data))]
    
    if cohort_filter != "All Cohorts":
        cohort_num = int(cohort_filter.split()[-1])
        location_filtered_data = location_filtered_data[location_filtered_data['Cohort'] == cohort_num]
    
    location_counts = location_filtered_data['Location'].value_counts()
    threshold = 0.03  # 3%

    # Calculate percentage distribution
    total = location_counts.sum()
    location_percent = location_counts / total

    # Filter to keep only values above threshold
    filtered_locations = location_counts[location_percent >= threshold]

    # Optional: group the small ones into "Other"
    if (location_percent < threshold).any():
        other_sum = location_counts[location_percent < threshold].sum()
        filtered_locations['Other'] = other_sum

    # Create pie chart
    fig = px.pie(
        values=filtered_locations.values,
        names=filtered_locations.index,
        title="Distribution of Participants by Location",
        color_discrete_sequence=['#ff6b35', '#fed7aa', '#fff5f0', '#b3b3b3']  # Add more if needed
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#2d3748'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Role Distribution - Centered across all columns as requested
    st.subheader("Role Distribution")
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
    
    # Removed Mentor Eligibility pie chart as requested
