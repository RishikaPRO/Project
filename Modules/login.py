import streamlit as st
from utils.auth import authenticate
 
 
class LoginPage:
 
    def show_login(self):
        
 
        col1, col2, col3 = st.columns([1, 1.6, 1])
        #css scriot for style
 
        with col2:
            st.markdown(
                """
                <div style="text-align:center; padding: 2rem 0 1rem 0;">
                <div style="font-family:'Syne',sans-serif; font-size:2.4rem;
                font-weight:800; color:#0d1117; letter-spacing:-1px;">
                AD<span style="color:#f97316">-Tools</span>
                </div>
                <div style="color:#6e7681; font-size:0.85rem; margin-top:0.25rem;">
                Project Management & Audit System
                </div>
<<<<<<< HEAD
                </div>
                """,
                unsafe_allow_html=True,
            )
 
            role_choice = st.radio(
                "Login as",
                ["Reporting Manager", "Team Member"],
                horizontal=True,
            )
 
            st.markdown("<br>", unsafe_allow_html=True)
            #username and password input
=======
            </div>
            """,
            unsafe_allow_html=True,
        ) 
        role_choice = st.radio(
            "Login as",
            ["Reporting Manager", "Team Member"],
            horizontal=True,
        )
>>>>>>> b7f309dcc13965b6e372e5fec1ce780da0c6cdc8
 
            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )
 
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            #Login buttons
 
            col_a, col_b = st.columns(2)
 
            with col_a:
                login_clicked = st.button(
                    "Login",
                    use_container_width=True
                )
 
            with col_b:
                if st.button(
                    "Reset",
                    use_container_width=True
                ):
                    st.rerun()
            #Authentication using role and excel data
 
            if login_clicked:
                if not username or not password:
                    st.error(
                        "Please enter both username and password."
                    )
                else:
                    user = authenticate(username, password)
 
                    if user:
                        if (
                            user["role"] == role_choice
                            or (
                                role_choice == "Reporting Manager"
                                and user["role"] == "Reporting Manager"
                            )
                            or (
                                role_choice == "Team Member"
                                and user["role"] == "Team Member"
                            )
                        ):
                            st.session_state.logged_in = True
                            st.session_state.Username = username
                            st.session_state.role = user["role"]
                            st.session_state.team = user["team"]
                            st.session_state.current_page = "Dashboard"
 
                            st.success(
                                "Login successful! Redirecting…"
                            )
                            st.rerun()
                        else:
                            st.error(
                                "Role mismatch. Please select the correct login type."
                            )
                    else:
                        st.error(
                            "Invalid username or password."
                        )
 
            st.markdown("</div>", unsafe_allow_html=True)
 
            st.markdown(
                '<div style="text-align:center; color:#6e7681; font-size:0.75rem;'
                'margin-top:1.5rem;">AD-Tools Team · AD_Tools</div>',
                unsafe_allow_html=True,
            )
 
 
def show_login():
    LoginPage().show_login()