from pathlib import Path
import pandas as pd
import streamlit as st
 
def authenticate(username, password):
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = BASE_DIR / "Login.xlsx"
 
        st.write("Reading:", file_path)
 
        df = pd.read_excel(file_path)
        st.write(df)
 
        df.columns = df.columns.str.strip().str.lower()
 
        user = df[
            (df["username"].astype(str).str.strip() == str(username).strip()) &
            (df["password"].astype(str).str.strip() == str(password).strip())
        ]
 
        if not user.empty:
            row = user.iloc[0]
            return {
                "role": row["role"],
                "team": row["team"]
            }
 
        return None
 
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return None
 