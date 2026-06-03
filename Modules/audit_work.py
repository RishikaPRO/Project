import streamlit as st
import pandas as pd
import os
class AuditWorkPage:
    AUDIT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditwork.xlsx")
    STAGES   = ["Start-Up Audit", "In Progress", "Post Release", "Open NC"]
    STATUSES = ["Pending", "Active", "Completed", "On Hold"]
    STYLE = """
        <style>
        .block-container { padding-top: 3rem; padding-bottom: 5rem; }
        [data-testid="metric-container"] { background-color: #F5F7FA; border: 1px solid #DDE2E7; padding: 15px; border-radius: 10px; }
        h3 { color: #1F3A5F; }
        div[data-testid="stDataFrame"] { border: 1px solid #DDE2E7; border-radius: 10px; }
        .stButton button { background-color: #1F3A5F; color: white; border-radius: 8px; border: none; }
        .stButton button:hover { background-color: #2B4E7A; }
        </style>
    """
    def show(self):
        st.title("Audit Work")
        st.markdown(self.STYLE, unsafe_allow_html=True)
        st.caption("View and manage audit records")
        # Load data
        try:
            raw_df = pd.read_excel(self.AUDIT_FILE)
            raw_df.columns = raw_df.columns.str.strip().str.lower()
        except FileNotFoundError:
            st.error("Audit data file not found. Please make sure 'auditwork.xlsx' exists.")
            return
        except Exception as e:
            st.error(f"Failed to load audit data: {e}")
            return
        df = pd.DataFrame()
        df["Audit ID"]   = raw_df.iloc[:, 0].astype(str).str.strip()
        df["Project"]    = raw_df.iloc[:, 1].astype(str).str.strip()
        df["Auditor"]    = raw_df.iloc[:, 2].astype(str).str.strip()
        df["Stage"]      = raw_df.iloc[:, 3].astype(str).str.strip()
        df["Status"]     = raw_df.iloc[:, 4].astype(str).str.strip()
        df["Completion"] = pd.to_numeric(raw_df.iloc[:, 5], errors="coerce").fillna(0).astype(int)
        df["Remarks"]    = raw_df.iloc[:, 6].astype(str).str.strip()
        role = st.session_state.get("role", "")
        # Metrics
        st.markdown("### Audit Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Audits", len(df))
        c2.metric("Completed",    (df["Status"].str.lower() == "completed").sum())
        c3.metric("Active",       (df["Status"].str.lower() == "active").sum())
        c4.metric("Pending",      (df["Status"].str.lower() == "pending").sum())
        st.markdown("---")
        st.subheader("Audit Directory")
        # Filters
        with st.expander("Filters", expanded=True):
            f1, f2, f3 = st.columns(3)
            with f1:
                search = st.text_input("Search by Audit ID or Project", placeholder="Type to search")
            with f2:
                stage_filter = st.selectbox("Filter by Stage", ["All"] + sorted(df["Stage"].unique().tolist()))
            with f3:
                status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique().tolist()))
        filtered_df = df.copy()
        if search:
            filtered_df = filtered_df[
                filtered_df["Audit ID"].str.contains(search, case=False) |
                filtered_df["Project"].str.contains(search, case=False)
            ]
        if stage_filter != "All":
            filtered_df = filtered_df[filtered_df["Stage"] == stage_filter]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        st.markdown("<br>", unsafe_allow_html=True)
        if filtered_df.empty:
            st.info("No audit records found matching the criteria.")
            return
        st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True, hide_index=True)
        # Edit panel — Reporting Manager only
        if role == "Reporting Manager":
            st.markdown("---")
            st.markdown("**Action**")
            selected_id = st.selectbox("Select Audit ID to edit", [""] + filtered_df["Audit ID"].tolist())
            if selected_id != "":
                selected = filtered_df[filtered_df["Audit ID"] == selected_id].iloc[0]
                with st.expander(f"Edit - {selected_id}", expanded=True):
                    c1, c2 = st.columns(2)
                    new_project  = c1.text_input("Project",      value=selected["Project"])
                    new_auditor  = c2.text_input("Auditor",      value=selected["Auditor"])
                    new_stage    = c1.selectbox("Stage",         self.STAGES,   index=self.STAGES.index(selected["Stage"])     if selected["Stage"]   in self.STAGES   else 0)
                    new_status   = c2.selectbox("Status",        self.STATUSES, index=self.STATUSES.index(selected["Status"])  if selected["Status"]  in self.STATUSES else 0)
                    new_pct      = c1.slider("Completion %",     0, 100, int(selected["Completion"]))
                    new_remarks  = c2.text_input("Remarks",      value=selected["Remarks"])
                    col1, col2, _ = st.columns([1, 1, 4])
                    if col1.button("Save", use_container_width=True):
                        try:
                            full_df = pd.read_excel(self.AUDIT_FILE)
                            full_df.columns = full_df.columns.str.strip().str.lower()
                            mask = full_df.iloc[:, 0].astype(str).str.strip() == selected_id
                            full_df.loc[mask, full_df.columns[1]] = new_project
                            full_df.loc[mask, full_df.columns[2]] = new_auditor
                            full_df.loc[mask, full_df.columns[3]] = new_stage
                            full_df.loc[mask, full_df.columns[4]] = new_status
                            full_df.loc[mask, full_df.columns[5]] = new_pct
                            full_df.loc[mask, full_df.columns[6]] = new_remarks
                            full_df.to_excel(self.AUDIT_FILE, index=False)
                            st.success(f"Audit '{selected_id}' updated successfully!")
                            st.rerun()
                        except FileNotFoundError:
                            st.error("Could not save — file not found.")
                        except PermissionError:
                            st.error("Could not save — close the file in Excel and try again.")
                        except Exception as e:
                            st.error(f"Unexpected error while saving: {e}")
                    if col2.button("Back", use_container_width=True):
                        st.session_state.current_page = "Dashboard"
                        st.rerun()
def show_audit():
    AuditWorkPage().show()