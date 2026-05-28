import streamlit as st
import time

# Page configuration
st.set_page_config(page_title="AD-TOOLS", layout="centered")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# Login page
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .main { background-color: #f0f2f6; }
        .login-box {
            border: 1px solid #ccc;
            padding: 30px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            width: 400px;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title(" User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "srm" and password == "12345":
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
            time.sleep(1)
            #st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

# Dashboard page
else:
    # Sidebar menu
    menu = st.sidebar.radio(
        "Navigation",
        ["Employee Details", "Reports", "Job List", "Status Mail/Leave", "Logout"]
    )

    st.title("AD-Tools Dashboard")

    if menu == "Employee Details":
        st.header("Employee Details")
        st.write("Here you can view and manage employee information.")

    elif menu == "Reports":
        st.header("Reports")
        st.write("Generate and view reports here.")

    elif menu == "Job List":
        st.header("Job Load")
        st.metric("Santhosh", 3471)
        st.metric("Sivasree", 2355)

    elif menu == "Status Mail/Leave":
        st.header("Status Mail")
        st.write("Automated status mails sent to all stakeholders.")
        st.header("Leave Management")
        st.write("Track and approve leave requests.")

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.success("You have been logged out.")
        time.sleep(1)
        st.experimental_rerun()

    # Add some design elements
    st.progress(70)
    st.toast("Dashboard loaded!", duration="short")
