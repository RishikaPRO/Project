import pandas as pd
import streamlit as st
def authenticate(username,password):
    try:
        df=pd.read_excel("Login.xlsx")
        st.write(df)

        print(df.shape)
        df.columns=df.columns.str.strip().str.lower()
        user=df[(df["username"].astype(str).str.strip()==str(username)) & (df["password"].astype(str).str.strip()==str(password))]
        if not user.empty:
            row=user.iloc[0]
            return {
                "role":row["role"],
                "team":row["team"]}
        else:
            return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
    