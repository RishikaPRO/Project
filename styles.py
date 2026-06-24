import streamlit as st
from pathlib import Path

def load_css():
    """Call this at the top of every page to apply the global dark theme."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
    else:
        st.warning("styles.css not found. Make sure it's in the same folder as styles.py")
