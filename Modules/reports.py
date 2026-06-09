import streamlit as st
import pandas as pd
import plotly.express as px
import io
import zipfile
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from styles import load_css

class ReportsDashboard:
    def __init__(self, file_path):
        self.FILE = file_path
        self.df = self.load_data()
        self.name_col = self.find_col(["employee_name", "name", "team_members"])
        self.status_col = self.find_col(["job_status", "status"])
        self.date_col = self.find_col(["start_date", "end_date", "date"])
        if self.name_col is None:
            self.name_col = self.df.columns[0]
        
        #break multiple team member's names in the names column
        self.normalize_employees()
        self.employees = sorted(self.df[self.name_col].dropna().unique())
    # ---------------- LOAD ----------------
    @st.cache_data
    def load_data(_self):
        xl = pd.ExcelFile(_self.FILE)
        frames = []
        for sheet in xl.sheet_names:
            df = pd.read_excel(_self.FILE, sheet_name=sheet)
            df["Sheet"] = sheet
            frames.append(df)
        data = pd.concat(frames, ignore_index=True)
        data.columns = [c.strip() for c in data.columns]
        return data
    # ---------------- COLUMN DETECTION ----------------
    def find_col(self, options):
        for c in self.df.columns:
            key = c.lower().replace(" ", "_")
            if key in options:
                return c
        return None
    # ----------------  CORE FIX: NORMALIZATION ----------------
    def normalize_employees(self):
        def clean(x):
            if pd.isna(x):
                return ""
            x = str(x).replace("\xa0", " ")
            return " ".join(x.split())
        self.df[self.name_col] = self.df[self.name_col].apply(clean)
        # split multiple employees in one cell
        self.df[self.name_col] = self.df[self.name_col].str.split(",")
        # explode into multiple rows
        self.df = self.df.explode(self.name_col)
        # final cleanup
        self.df[self.name_col] = self.df[self.name_col].apply(clean)
        # remove empty
        self.df = self.df[self.df[self.name_col] != ""]
    # ---------------- EXCEL EXPORT ----------------
    def to_excel(self, df):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Report")
        buffer.seek(0)
        return buffer
    # ---------------- PDF EXPORT ----------------
    def to_pdf(self, df, title):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
        elements.append(Spacer(1, 10))
        table_data = [df.columns.tolist()] + df.astype(str).values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer
    # ---------------- UI ----------------
    def show_reports(self):
        load_css()
        st.title(" AD-Tools Reports Dashboard")
        # overall chart
        if self.status_col:
            st.subheader(" Overall Status")
            fig = px.histogram(self.df, x=self.status_col, color=self.status_col)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("Team Members")
        cols = st.columns(2)
        if "expanded" not in st.session_state:
            st.session_state.expanded = None
        for i, emp in enumerate(self.employees):
            
            #get records by team members name
            emp_df = self.df[self.df[self.name_col].eq(emp)]
            with cols[i % 2]:
                st.markdown(
                f"""<div style="
                        padding:20px;
                        height:120px;
                        width:500px;
                        border-radius:7px;
                        background:#5d89ba;
                        text-align:center;
                        margin-bottom:10px;
                    ">
<h3>👤 {emp}</h3>
<p>{len(emp_df)} records</p>
</div>

                    """,
                    unsafe_allow_html=True
                )
                if st.button("Open", key=f"btn_{i}"):
                    st.session_state.expanded = emp if st.session_state.expanded != emp else None
                if st.session_state.expanded == emp:
                    st.markdown("### Employee Details")
                    st.dataframe(emp_df, use_container_width=True)
                    # chart of the respective employee
                    if self.status_col:
                        fig1 = px.pie(emp_df, names=self.status_col, title="Status Breakdown")
                        st.plotly_chart(fig1, use_container_width=True)
                    if self.date_col:
                        temp = emp_df.copy()
                        temp[self.date_col] = pd.to_datetime(temp[self.date_col], errors="coerce")
                        fig2 = px.histogram(temp, x=self.date_col, title="Timeline")
                        st.plotly_chart(fig2, use_container_width=True)
                    # downloads
                    st.download_button(
                        "Excel",
                        data=self.to_excel(emp_df),
                        file_name=f"{emp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.download_button(
                        "PDF",
                        data=self.to_pdf(emp_df, emp),
                        file_name=f"{emp}.pdf",
                        mime="application/pdf"
                    )
                st.download_button(
                    "Excel",
                    data=self.to_excel(emp_df),
                    file_name=f"{emp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )    
                st.download_button(
                    "PDF",
                    data=self.to_excel(emp_df),
                    file_name=f"{emp}.xlsx",
                    mime="application./df"
                )
# ---------------- MAIN ----------------
def show_reports():
    app = ReportsDashboard("AD_Weekly_Load_Tracking_2026-27.xlsx")
    app.show_reports()

if __name__ == "__main__":
    show_reports()
 