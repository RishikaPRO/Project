import streamlit as st
import pandas as pd
# Page configuration
st.set_page_config(page_title="AD-TOOLS", page_icon="🔐", layout="centered")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# Login page
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .main { background-color: #f0f2f6; }
        
        
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "srm" and password == "12345":
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
        else:
            st.error("Invalid username or password. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

# Dashboard page
else:
    st.title("AD-Tools Dashboard")
    st.sidebar.title("AD-Tools")
    menu=st.sidebar.radio(
        "Navigation",
        [
            "Dashboad",
            "Employee Details",
            "Job List",
            "Audit Work",
            "Reports",
            "Statusmail/Leave",
            "Log out"
        ]
    )

    if menu=="Dashboard":
        st.title("AD-Tools Dashboard")
        col1,col2,col3=st.columns(3)
        col1.metric("Total Jobs",25)
        col2.metric("Completed",18)
        col3.metric("Pending",7)
    elif menu=="Employee Details":
        df=pd.read_excel("employees.xlsx")
        st.title("Employee Details")
        search=st.text_input("Search Employee Name")
        department=st.selectbox(
            "Filter Department",
            ["All"]+
        list(df["Department"].unique())
        )
        filtered_df=df
        if search:
            filtered_df=filtered_df[
                filtered_df["Name"].str.contains(search,case=False)
            ]
        if department !="All":
            filtered_df=filtered_df[filtered_df["Department"]==department]
        st.dataframe(filtered_df)
        
    elif menu=="Job list":
        st.title("Job list")
        st.write("Job 1")
        st.progress(70)
        st.write("Job 2")
        st.progress(90)
    elif menu=="Audit Work":
        st.title("Audit Work")
        tab1,tab2,tab3,tab4=st.tabs([
            "Start-up Audit",
            "In Progress",
            "Post Release",
            "Open NC"
        ])

