import streamlit as st
from utils.authenticate import authenticate
# --- Page Configuration ---
st.set_page_config(
  page_title="Gunma WorkVista",
  layout="wide",
  menu_items={
      'Get Help': None,
      'Report a bug': None,
      'About': None
  }
)
# --- Hide Streamlit Menu, Footer, and Floating Decorators ---
st.markdown("""
<style>
/* Hide the entire top app bar / header area */
header[data-testid="stHeader"] {
   visibility: hidden;
   display: none !important;
}
/* Specific selectors to target Streamlit cloud injected elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
/* Hide the Deploy button specifically */
.stAppDeployButton {
   display: none !important;
   visibility: hidden;
}
/* Hide the GitHub icon specifically */
#GithubIcon {
   visibility: hidden;
   display: none !important;
}
/* Wipe out the remaining top action toolbar wrapper entirely */
[data-testid="stAppToolbar"] {
   display: none !important;
}
/* Hide Streamlit floating background decorator line */
[data-testid="stDecoration"] {
   display: none !important;
}
</style>
""", unsafe_allow_html=True)

class LoginPage:
   def show_login(self):
       col1, col2, col3 = st.columns([1, 1.6, 1])
       with col2:
           st.markdown(
               """
<div style="text-align:center; padding: 2rem 0 1rem 0;">
<div style="font-family:'Syne',sans-serif; font-size:2.4rem;
               font-weight:800; color:#0d1117; letter-spacing:-1px;">
               Gunma <span style="color:#f97316">WorkVista</span>
</div>
<div style="color:#6e7681; font-size:0.85rem; margin-top:0.25rem;">
</div>
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
           # Username and password inputs
           username = st.text_input(
               "Username",
               placeholder="Enter your username"
           )
           password = st.text_input(
               "Password",
               type="password",
               placeholder="Enter your password"
           )
           # Action buttons layout
           col_a, col_b = st.columns(2)
           with col_a:
               login_clicked = st.button("Login", use_container_width=True)
           with col_b:
               if st.button("Reset", use_container_width=True):
                   st.rerun()
           # Authentication processing logic
           if login_clicked:
               if not username or not password:
                   st.error("Please enter both username and password.")
               else:
                   user = authenticate(username, password)
                   if user:
                       # Streamlined condition evaluation
                       if user["role"] == role_choice:
                           st.session_state.logged_in = True
                           st.session_state.Username = username
                           st.session_state.role = user["role"]
                           st.session_state.team = user["team"]
                           st.session_state.current_page = "Dashboard"
                           st.success("Login successful! Redirecting…")
                           st.rerun()
                       else:
                           st.error("Role mismatch. Please select the correct login type.")
                   else:
                       st.error("Invalid username or password.")
           st.markdown("</div>", unsafe_allow_html=True)

def show_login():
   LoginPage().show_login()