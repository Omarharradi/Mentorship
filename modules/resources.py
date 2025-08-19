import streamlit as st
import pandas as pd
import plotly.express as px

def show_resources(data):
    """Resources - Mentor view of resource library"""
    st.title("📚 Resources")
    st.markdown("### Access mentoring materials and guides")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_resources = len(data['resources'])
        st.metric("Available Resources", total_resources)
    
    with col2:
        total_downloads = data['resources']['Downloads'].sum()
        st.metric("Total Downloads", total_downloads)
    
    with col3:
        categories = data['resources']['Category'].nunique()
        st.metric("Categories", categories)
    
    st.markdown("---")
    
    # Search and filter
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("🔍 Search resources:", placeholder="Enter keyword...")
    
    with col2:
        category_filter = st.selectbox("Filter by category:", ["All"] + list(data['resources']['Category'].unique()))
    
    # Apply filters
    filtered_resources = data['resources'].copy()
    
    if search_term:
        filtered_resources = filtered_resources[
            filtered_resources['Document_Name'].str.contains(search_term, case=False, na=False)
        ]
    
    if category_filter != "All":
        filtered_resources = filtered_resources[filtered_resources['Category'] == category_filter]
    
    # Resource categories tabs
    st.subheader("📂 Browse by Category")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Getting Started", "⭐ Best Practices", "📝 Templates"])
    
    with tab1:
        getting_started = filtered_resources[filtered_resources['Category'] == 'Getting Started']
        if not getting_started.empty:
            for _, resource in getting_started.iterrows():
                with st.expander(f"📄 {resource['Document_Name']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Type:** {resource['Type']}")
                        st.write(f"**Size:** {resource['File_Size']}")
                        st.write(f"**Uploaded:** {resource['Upload_Date']}")
                        st.write(f"**Views:** {resource['Views']} | **Downloads:** {resource['Downloads']}")
                        
                        # Mock description
                        descriptions = {
                            'Mentor Guide 2025': 'Comprehensive guide for new mentors covering program overview, expectations, and best practices.',
                            'Mentee Toolkit': 'Essential resources for mentees including goal-setting templates and communication guidelines.',
                            'Mentorship FAQ': 'Frequently asked questions about the mentorship program with detailed answers.'
                        }
                        if resource['Document_Name'] in descriptions:
                            st.write(f"**Description:** {descriptions[resource['Document_Name']]}")
                    
                    with col2:
                        pass
        else:
            st.info("No Getting Started resources match your current filters.")
    
    with tab2:
        best_practices = filtered_resources[filtered_resources['Category'] == 'Best Practices']
        if not best_practices.empty:
            for _, resource in best_practices.iterrows():
                with st.expander(f"📄 {resource['Document_Name']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Type:** {resource['Type']}")
                        st.write(f"**Size:** {resource['File_Size']}")
                        st.write(f"**Uploaded:** {resource['Upload_Date']}")
                        st.write(f"**Views:** {resource['Views']} | **Downloads:** {resource['Downloads']}")
                        
                        # Mock description
                        descriptions = {
                            'Communication Best Practices': 'Effective communication strategies for mentors including active listening and feedback techniques.',
                            'Feedback Framework Guide': 'Structured approach to providing constructive feedback that drives mentee development.',
                            'Leadership Styles Overview': 'Understanding different leadership styles and how to adapt your mentoring approach.'
                        }
                        if resource['Document_Name'] in descriptions:
                            st.write(f"**Description:** {descriptions[resource['Document_Name']]}")
                    
                    with col2:
                        pass
        else:
            st.info("No Best Practices resources match your current filters.")
    
    with tab3:
        templates = filtered_resources[filtered_resources['Category'] == 'Templates']
        if not templates.empty:
            for _, resource in templates.iterrows():
                with st.expander(f"📄 {resource['Document_Name']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Type:** {resource['Type']}")
                        st.write(f"**Size:** {resource['File_Size']}")
                        st.write(f"**Uploaded:** {resource['Upload_Date']}")
                        st.write(f"**Views:** {resource['Views']} | **Downloads:** {resource['Downloads']}")
                        
                        # Mock description
                        descriptions = {
                            'Leadership Assessment Template': 'Template for assessing mentee leadership capabilities and development areas.',
                            'SMART Goals Worksheet': 'Interactive worksheet to help mentees create specific, measurable, achievable goals.',
                            'Career Development Roadmap': 'Template for mapping out mentee career progression and milestones.',
                            'Session Planning Template': 'Structure for planning effective mentoring sessions with clear objectives.'
                        }
                        if resource['Document_Name'] in descriptions:
                            st.write(f"**Description:** {descriptions[resource['Document_Name']]}")
                    
                    with col2:
                        pass
        else:
            st.info("No Templates match your current filters.")
    
    # Recently Added
    st.markdown("---")
    st.subheader("🆕 Recently Added")
    
    # Sort by upload date (mock recent additions)
    recent_resources = data['resources'].nlargest(3, 'Views')  # Using views as proxy for recent
    
    for _, resource in recent_resources.iterrows():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(f"**{resource['Document_Name']}**")
            st.write(f"{resource['Category']} • {resource['Type']}")
        
        with col2:
            st.write(f"**{resource['Views']}** views")
        
        with col3:
            st.write(f"**{resource['Downloads']}** downloads")
        
        with col4:
            pass
    
    # Popular Resources
    st.markdown("---")
    st.subheader("🔥 Most Popular")
    
    popular_resources = data['resources'].nlargest(5, 'Downloads')
    
    fig_popular = px.bar(
        popular_resources,
        x='Downloads',
        y='Document_Name',
        orientation='h',
        title="Top 5 Most Downloaded Resources",
        color='Downloads',
        color_continuous_scale="Blues"
    )
    fig_popular.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    st.plotly_chart(fig_popular, use_container_width=True)
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pass
    
    with col2:
        pass
    
    with col3:
        pass
    
    with col4:
        pass
    
    # Resource Tips
    st.markdown("---")
    st.subheader("💡 Resource Tips")
    
    tips = [
        "📖 Start with the **Mentor Guide 2025** if you're new to the program",
        "🎯 Use **SMART Goals Worksheet** to help your mentee set clear objectives",
        "💬 Review **Communication Best Practices** for effective mentoring conversations",
        "📋 **Session Planning Template** helps structure productive meetings",
        "⭐ **Leadership Assessment Template** is great for identifying development areas"
    ]
    
    for tip in tips:
        st.write(tip)
    
    # My Downloads (mock feature)
    st.markdown("---")
    st.subheader("📥 My Recent Downloads")
    
    # Mock recent downloads
    recent_downloads = [
        {"Resource": "Mentor Guide 2025", "Downloaded": "2 days ago", "Category": "Getting Started"},
        {"Resource": "SMART Goals Worksheet", "Downloaded": "1 week ago", "Category": "Templates"},
        {"Resource": "Communication Best Practices", "Downloaded": "2 weeks ago", "Category": "Best Practices"}
    ]
    
    downloads_df = pd.DataFrame(recent_downloads)
    st.dataframe(downloads_df, use_container_width=True)
