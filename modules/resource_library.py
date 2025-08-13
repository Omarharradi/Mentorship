import streamlit as st
import pandas as pd
import plotly.express as px

def show_resource_library(data):
    """Module 5: Live Access to Library"""
    st.title("📚 Resource Library")
    st.markdown("### One-stop hub for guides, journey maps, and FAQs")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_resources = len(data['resources'])
    total_views = data['resources']['Views'].sum()
    total_downloads = data['resources']['Downloads'].sum()
    avg_usage = round(data['resources']['Downloads'].mean(), 1)
    
    with col1:
        st.metric("Total Resources", total_resources)
    
    with col2:
        st.metric("Total Views", total_views)
    
    with col3:
        st.metric("Total Downloads", total_downloads)
    
    with col4:
        st.metric("Avg Downloads/Resource", avg_usage)
    
    st.markdown("---")
    
    # Upload section (HR only) - Simplified
    if st.session_state.user_role == "HR":
        st.subheader("📤 Upload New Resource")
        
        with st.expander("Upload Resource", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'pptx'])
                category = st.selectbox("Category:", ["Getting Started", "Best Practices", "Templates"])
            
            with col2:
                resource_name = st.text_input("Resource Name", placeholder="Enter resource name...")
                description = st.text_area("Description", height=80, placeholder="Brief description...")
            
            if st.button("📤 Upload Resource", type="primary"):
                if uploaded_file and resource_name:
                    # Simulate successful upload
                    st.success(f"✅ Resource '{resource_name}' uploaded successfully!")
                    st.info(f"📁 File: {uploaded_file.name} | 📂 Category: {category}")
                else:
                    st.error("Please select a file and enter a resource name.")
        
        st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("Filter by Category:", ["All"] + list(data['resources']['Category'].unique()))
    
    with col2:
        type_filter = st.selectbox("Filter by Type:", ["All"] + list(data['resources']['Type'].unique()))
    
    with col3:
        search_term = st.text_input("Search Resources:", placeholder="Enter resource name...")
    
    # Apply filters
    filtered_resources = data['resources'].copy()
    
    if category_filter != "All":
        filtered_resources = filtered_resources[filtered_resources['Category'] == category_filter]
    
    if type_filter != "All":
        filtered_resources = filtered_resources[filtered_resources['Type'] == type_filter]
    
    if search_term:
        filtered_resources = filtered_resources[filtered_resources['Document_Name'].str.contains(search_term, case=False, na=False)]
    

    
    # Resources table
    st.subheader("📋 Available Resources")
    
    # Add download buttons
    display_df = filtered_resources.copy()
    
    # Create download column
    download_buttons = []
    for idx, row in display_df.iterrows():
        download_buttons.append(f"📥 Download")
    
    display_df['Action'] = download_buttons
    
    # Select columns for display
    display_columns = ['Document_Name', 'Type', 'Category', 'Upload_Date', 'Views', 'Downloads', 'File_Size']
    
    st.dataframe(display_df[display_columns], use_container_width=True)
    
    # Resource categories
    st.markdown("---")
    st.subheader("📂 Browse by Category")
    
    tab1, tab2, tab3 = st.tabs(["Getting Started", "Best Practices", "Templates"])
    
    with tab1:
        getting_started = data['resources'][data['resources']['Category'] == 'Getting Started']
        for _, resource in getting_started.iterrows():
            with st.expander(f"📄 {resource['Document_Name']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Type:** {resource['Type']}")
                    st.write(f"**Size:** {resource['File_Size']}")
                    st.write(f"**Views:** {resource['Views']} | **Downloads:** {resource['Downloads']}")
                with col2:
                    if st.button(f"Download", key=f"download_gs_{resource['Document_Name']}"):
                        st.success("Download started!")
    
    with tab2:
        best_practices = data['resources'][data['resources']['Category'] == 'Best Practices']
        for _, resource in best_practices.iterrows():
            with st.expander(f"📄 {resource['Document_Name']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Type:** {resource['Type']}")
                    st.write(f"**Size:** {resource['File_Size']}")
                    st.write(f"**Views:** {resource['Views']} | **Downloads:** {resource['Downloads']}")
                with col2:
                    if st.button(f"Download", key=f"download_bp_{resource['Document_Name']}"):
                        st.success("Download started!")
    
    with tab3:
        templates = data['resources'][data['resources']['Category'] == 'Templates']
        for _, resource in templates.iterrows():
            with st.expander(f"📄 {resource['Document_Name']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Type:** {resource['Type']}")
                    st.write(f"**Size:** {resource['File_Size']}")
                    st.write(f"**Views:** {resource['Views']} | **Downloads:** {resource['Downloads']}")
                with col2:
                    if st.button(f"Download", key=f"download_t_{resource['Document_Name']}"):
                        st.success("Download started!")
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Usage Report", use_container_width=True):
            st.success("Usage analytics report generated!")
    
    with col2:
        if st.button("🔍 Search Analytics", use_container_width=True):
            st.info("Search terms with no results: 'advanced leadership', 'conflict resolution'")
    
    with col3:
        if st.button("📧 Request New Resource", use_container_width=True):
            st.info("Resource request form sent to HR team.")
