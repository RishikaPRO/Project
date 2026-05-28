import streamlit as st
def showsidebar():
    with st.sidebar:
        st.markdown(
            f'<div class="sidebar-logo"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="Logo"></div>',
            unsafe_allow_html=True
        )
        st.markdown(f"**{st.session_state.get('team','AD_Tools Team')}**", unsafe_allow_html=True)
    st.markdown("---")
    nav_items = ["Dashboard", "Employee Details", "Job List", "Audit Work", "Reports", "Statusmail/Leave", "Logout"]
    selected=st.session_state.get("current_page","Dashboard")
    for label in nav_items:
        if st.button(f"{label}",key=f"nav_{label}",use_container_width=True):
            selected=label
            st.session_state["current_page"]=label
    st.markdown("---")
    st.markdown(
        f'<div class="sidebar-user">Loffed in as<br>'
        f'<strong>{st.session_state.get("username","").title()}</strong>'
        f' . {st.session_state.get("role","")}</div>',
        unsafe_allow_html=True
    )
    if st.button("Logout",use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    return selected