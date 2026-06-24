import streamlit as st

import pandas as pd
from styles import load_css
class LeaveStatusPage:
    LEAVE_FILE = "leave.xlsx"
    STATUS_FILE = "Status_Mail_Report.xlsx"
    ANNUAL_LEAVE = 24
    @st.cache_data(ttl=600)
    def load_leave_data(_self):
        df = pd.read_excel(_self.LEAVE_FILE, sheet_name="Leave Tracker")
        data = []
        for _, row in df.iterrows():
            name = str(row.iloc[0]).strip()
            if not name or name.lower() == "nan" or "total" in name.lower():
                continue
            month = pd.to_numeric(row.iloc[1], errors="coerce")
            year = pd.to_numeric(row.iloc[2], errors="coerce")
            month = 0 if pd.isna(month) else float(month)
            year = 0 if pd.isna(year) else float(year)
            data.append({
                "Employee Name": name,
                "Leave This Month": month,
                "Leave This Year": year,
                "Leave Remaining": _self.ANNUAL_LEAVE - year
            })
        return pd.DataFrame(data)
    @st.cache_data(ttl=600)
    def load_status_data(_self):
        raw = pd.read_excel(_self.STATUS_FILE, header=None)
        records = []
        for r in range(6, len(raw)):
            name = raw.iloc[r,2]
            if pd.isna(name):
                continue
            received = pd.to_numeric(raw.iloc[r,35], errors="coerce")
            missing = pd.to_numeric(raw.iloc[r,36], errors="coerce")
            received = 0 if pd.isna(received) else int(received)
            missing = 0 if pd.isna(missing) else int(missing)
            total = received + missing
            records.append({
                "Employee ID": str(raw.iloc[r,1]).strip(),
                "Employee Name": str(name).strip(),
                "Mail ID": str(raw.iloc[r,3]).strip(),
                "Received": received,
                "Not Sent": missing,
                "Completion %": round(received/total*100,1) if total else 0
            })
        return pd.DataFrame(records)
    def filter_employee(self, df, username_or_name):
        search_target = str(username_or_name).strip().lower()
        exact = df[df["Employee Name"].str.lower().str.strip() == search_target]
        if not exact.empty:
            return exact
        return df[df["Employee Name"].str.contains(search_target, case=False, na=False)]
    def leave_card(self, row):

        st.markdown(f"""
<div style="background:#1e293b;padding:22px;border-radius:14px;border-left:6px solid #facc15;box-shadow:0 4px 10px rgba(0,0,0,.3);margin-bottom:18px;font-family:inherit;">
<h2 style="color:white;font-family:inherit;"> Leave Status</h2>
<p style="color:#fff;font-family:inherit;"> <b>{row['Employee Name']}</b></p>
<hr>
<h3 style="color:#38bdf8;font-family:inherit;">This Month : {row['Leave This Month']}</h3>
<h3 style="color:#f97316;font-family:inherit;">This Year : {row['Leave This Year']}</h3>
<h3 style="color:#22c55e;font-family:inherit;">Remaining : {row['Leave Remaining']}</h3>
</div>""", unsafe_allow_html=True)
    def status_card(self, row):
        st.markdown(f"""
<div style="background:#1e293b;padding:22px;border-radius:14px;border-left:6px solid #3b82f6;box-shadow:0 4px 10px rgba(0,0,0,.3);margin-bottom:18px;font-family:inherit;">
<h2 style="color:white;font-family:inherit;"> Status Mail</h2>
<p style="color:#fff;font-family:inherit;"> <b>{row['Employee Name']}</b></p>
<p style="color:#fff;font-family:inherit;">{row['Employee ID']}</p>
<hr>
<h3 style="color:#22c55e;font-family:inherit;">Sent : {row['Received']}</h3>
<h3 style="color:#ef4444;font-family:inherit;">Not Sent : {row['Not Sent']}</h3>
<h3 style="color:#60a5fa;font-family:inherit;"> Completion : {row['Completion %']}%</h3>
</div>""", unsafe_allow_html=True)
    def show(self):
        load_css()
        # Reference styling injection
        st.markdown("""
<style>
.block-container { padding-top: 3rem; padding-bottom: 5rem; }
h3 { color: #1F3A5F; }
.directory-card { border: 1px solid #7c5cff; border-radius: 16px; background: rgba(124,92,255,0.08); padding: 18px; margin-bottom: 24px; font-family: inherit; }
.directory-table { width: 100%; border-collapse: collapse; margin-top: 16px; font-family: inherit; }
.directory-table th, .directory-table td { border: 1px solid rgba(124,92,255,0.16); padding: 12px 14px; text-align: left; }
.directory-table th { background: rgba(124,92,255,0.12); color: #f8fbff; font-weight: 700; }
.directory-table td { color: #eaf1ff; }
.directry-table tr:hover { background: rgba(124,92,255,0.08); }
</style>
""", unsafe_allow_html=True)
        role = st.session_state.get("role", "").strip().lower()
        username = st.session_state.get("Username", "").strip() 
        leave_df = self.load_leave_data()
        status_df = self.load_status_data()
        tab1, tab2 = st.tabs(["Leave Status"," Status Mail"])
        with tab1:
            if role == "team member":
                user = self.filter_employee(leave_df, username)
                if user.empty:
                    st.warning(f"Leave record not found for user: {username}")
                else:
                    self.leave_card(user.iloc[0])
            else:
                st.subheader("Leave Status Overview")
                search = st.text_input("search by employee name",placeholder="Type employee name...")
                df = leave_df
                if search:
                    df = df[df["Employee Name"].str.contains(search, case=False, na=False)]

                if df.empty:
                    st.info("No records match your criteria.")
                else:
                    # Formatted Reference Table Generation
                    table_html = '<div class="directory-card"><table class="directory-table">'
                    table_html += '<thead><tr>'
                    for col in df.columns:
                        table_html += f'<th>{col}</th>'
                    table_html += '</tr></thead><tbody>'
                    for _, row in df.iterrows():
                        table_html += '<tr>'
                        for val in row:
                            table_html += f'<td>{val}</td>'
                        table_html += '</tr>'
                    table_html += '</tbody></table></div>'
                    st.markdown(table_html, unsafe_allow_html=True)
        with tab2:
            if role == "team member":
                user = self.filter_employee(status_df, username)
                if user.empty:
                    st.warning(f"Status record not found for user: {username}")
                else:
                    self.status_card(user.iloc[0])
            else:
                st.subheader(" Status Mail Report Overview")
                search = st.text_input("search by name",placeholder="Type employee name...")
                df = status_df
                if search:
                    df = df[df["Employee Name"].str.contains(search, case=False, na=False)]
                if df.empty:
                     st.info("No records match your criteria.")
                else:
                    # Formatted Reference Table Generation
                    display_cols = ["Employee ID", "Employee Name", "Mail ID", "Received", "Not Sent", "Completion %"]
                    df_display = df[display_cols]
                    table_html = '<div class="directory-card"><table class="directory-table">'
                    table_html += '<thead><tr>'
                    for col in df_display.columns:
                        table_html += f'<th>{col}</th>'
                    table_html += '</tr></thead><tbody>'
                    for _, row in df_display.iterrows():
                        table_html += '<tr>'
                        for val in row:
                            table_html += f'<td>{val}</td>'
                        table_html += '</tr>'
                    table_html += '</tbody></table></div>'
                    st.markdown(table_html, unsafe_allow_html=True)
def show_statusmail():
    LeaveStatusPage().show()
 