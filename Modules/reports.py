import reportlab
import streamlit as st
import pandas as pd
import plotly.express as px
import io
import tempfile
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from styles import load_css
import kaleido

class ReportsDashboard:
    def __init__(self, file_path):
        self.FILE = file_path
        self.df = self.load_data()
        self.name_col = self.find_col(["employee_name", "name", "team_members"])
        self.status_col = self.find_col(["job_status", "status"])
        self.date_col = self.find_col(["start_date", "end_date", "date"])
        if self.name_col is None:
            self.name_col = self.df.columns[0]
        self.normalize_employees()
        self.employees = sorted(self.df[self.name_col].unique())
    #load excel data
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
    #Column detection in excel sheet for data retreival
    def find_col(self, options):
        for c in self.df.columns:
            key = c.lower().replace(" ", "_")
            if key in options:
                return c
        return None
   
    #Excel data normalization 
    def normalize_employees(self):
        def clean(x):
            if pd.isna(x):
                return ""
            x = str(x).replace("\xa0", " ")
            return " ".join(x.split())
        self.df[self.name_col] = self.df[self.name_col].apply(clean)
        self.df[self.name_col] = self.df[self.name_col].str.split(",")
        self.df = self.df.explode(self.name_col)
        self.df[self.name_col] = self.df[self.name_col].apply(clean)
        self.df = self.df[self.df[self.name_col] != ""]
    
    #Exoprt report data in excel format
    def to_excel(self, df):
        tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        tmp.close()
        with pd.ExcelWriter(tmp.name, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Report", index=False)
        return tmp.name

    #Export report data in pdf format 
    def to_pdf(self, df, title):
        def plotly_to_image(fig, width=700, height=400):
            img_bytes = io.BytesIO()
            img_bytes.write(fig.to_image(format="png", width=700, height=400))
            img_bytes.seek(0)
            return img_bytes
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.close()
        doc = SimpleDocTemplate(tmp.name, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        styles = getSampleStyleSheet()
        elements = []
    
    #PDF Header
        elements.append(Paragraph(f"<b>{title} - Employee Report</b>", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Total Records: <b>{len(df)}</b>", styles["Normal"]))
        elements.append(Spacer(1,15))

    #Status Chart display 
        if self.status_col and self.status_col in df.columns:
            status_counts = (df[self.status_col].fillna("Unknown"))
           
            if len(status_counts) > 0:
                status_colors=["#a8e6a8", "#1b4d2e", "#c2f0c2", "#2d5016", "#1a6b34"]
                fig = px.pie(df, names=self.status_col, title="Status Breakdown",color=self.status_col, color_discrete_sequence=status_colors)
        
                elements.append(Paragraph("Status Breakdown", styles["Heading2"]))
                elements.append(Spacer(1, 5))
                elements.append(
                RLImage(plotly_to_image(fig), width=450, height=280))                   
                elements.append(Spacer(1, 15))
        #Project timeline chart display
        if self.date_col and self.date_col in df.columns:
            temp = df.copy()
            temp[self.date_col] = pd.to_datetime(temp[self.date_col], errors="coerce")
            temp = temp.dropna(subset=[self.date_col])
            if not temp.empty:
                fig2 = px.histogram(temp, x=self.date_col, title="Timeline", color_discrete_sequence=["#a8e6a8"])
                elements.append(Paragraph("Timeline", styles["Heading2"]))
                elements.append(Spacer(1, 5))
                elements.append(RLImage(plotly_to_image(fig2), width=450, height=280))
                elements.append(Spacer(1, 15))
        
        #Table page
        elements.append(PageBreak())
        elements.append(Paragraph("Detailed Records", styles["Heading1"]))
        elements.append(Spacer(1, 10))
        table_data = [df.columns.tolist()]
        table_data.extend(df.fillna("").astype(str).values.tolist())
        available_width = 520
        col_width = available_width / max(len(df.columns), 1)
        table = Table(table_data, colWidths=[col_width]*len(df.columns), repeatRows=1)
        table.setStyle(TableStyle([("BACKGROUND",(0, 0),(-1, 0),colors.HexColor("#1E293B")),
           ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
           ("FONTSIZE", (0, 0), (-1, -1), 7),
           ("BOTTOMPADDING", (0, 0), (-1, 0),8),
           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),]))
        elements.append(table)
        doc.build(elements)
        return tmp.name
        
        #Dashboard page UI 
    def show_reports(self):
        load_css()
        st.markdown("""
    <div style='
            padding:20px;
            border-radius:12px;
            background:linear-gradient(90deg,#0f172a,#1e293b);
            color:white;
            margin-bottom:20px;
        '>
    <h2 style='margin:0;'>Reports Dashboard</h2>
    <p style='margin:0;opacity:0.8;'>Employee analytics & reporting system</p>
    </div>
    <style>
    body { background: #070b14 !important; }
    .stApp { background: #070b14 !important; }
    [data-testid="stAppViewContainer"] { background: #070b14 !important; }
    .report-card { border: 1px solid #7c5cff; border-radius: 16px; background: rgba(124,92,255,0.08); padding: 18px; margin-bottom: 16px; }
    .report-card h3 { margin: 0 0 8px; color: #f8fbff; font-size: 18px; }
    .report-card p { margin: 0; color: #c5d2ff; font-size: 14px; }
    .employee-card { border: 1px solid #7c5cff; border-radius: 16px; background: rgba(124,92,255,0.08); padding: 18px; margin-bottom: 18px; }
    .employee-card h3 { margin: 0 0 6px; color: #f8fbff; }
    .employee-card p { margin: 0; color: #c5d2ff; }
    [data-testid="stDataFrame"] { border: 1px solid rgba(124,92,255,0.16) !important; border-radius: 12px !important; background: rgba(124,92,255,0.05) !important; }
    [data-testid="stDataFrame"] th { background: rgba(124,92,255,0.12) !important; color: #f8fbff !important; }
    [data-testid="stDataFrame"] td { color: #eaf1ff !important; }
    .stPlotlyChart { border: 1px solid #7c5cff; border-radius: 12px; background: rgba(124,92,255,0.04); padding: 12px; margin-bottom: 18px; }
    </style>
        """, unsafe_allow_html=True)

        # Overall Insights based on Job Status 
        if self.status_col:
            st.markdown("###  Overall Insights")
            fig = px.histogram(
                self.df,
                x=self.status_col,
                color=self.status_col,
                color_discrete_sequence=["#a8e6a8", "#1b4d2e", "#c2f0c2", "#2d5016", "#1a6b34"]
            )
            fig.update_layout(plot_bgcolor="rgba(124,92,255,0.08)", paper_bgcolor="#070b14", font=dict(color="#eaf1ff"))
            st.plotly_chart(fig, use_container_width=True, key="overall_status_histogram")

        #Individual team members data display    
        st.markdown("### Team Members")
        role = st.session_state.get("role", "")
        username = st.session_state.get("Username", "").strip()
        if role == "Team Member":
            employees_to_show = [username]
        else:
            employees_to_show = self.employees
        for emp in employees_to_show:
            if role == "Team Member":
                emp_df = self.df[
                    self.df[self.name_col]
                    .astype(str)
                    .str.contains(emp, case=False, na=False)
                ]
            else:
                emp_df = self.df[self.df[self.name_col] == emp]
            if emp_df.empty:
                continue
            st.markdown(f"""
                        <div class="employee-card">
                        <h3>{emp}</h3>
                        <p>{len(emp_df)} Records</p>
                        </div>""", unsafe_allow_html=True)
            
            #Display of the logged in member s details
            if role == "Team Member":
                st.markdown("#### Employee Details")
                table_height = min(max(400, len(emp_df) * 35), 1200)
                st.dataframe(emp_df, use_container_width=True, height=table_height)
                if self.status_col:
                    st.markdown("#### Status Breakdown")
                    fig = px.pie(emp_df, names=self.status_col, hole=0.45, color_discrete_sequence=["#a8e6a8", "#1b4d2e", "#c2f0c2", "#2d5016", "#1a6b34"])
                    fig.update_layout(plot_bgcolor="rgba(124,92,255,0.08)", paper_bgcolor="#070b14", font=dict(color="#eaf1ff"))
                    st.plotly_chart(fig, use_container_width=True)
                if self.date_col:
                    temp = emp_df.copy()
                    temp[self.date_col] = pd.to_datetime(
                        temp[self.date_col],
                        errors="coerce"
                    )
                    st.markdown("#### Timeline")
                    fig2 = px.histogram(temp, x=self.date_col, nbins=20, color_discrete_sequence=["#a8e6a8"])
                    fig2.update_layout(plot_bgcolor="rgba(124,92,255,0.08)", paper_bgcolor="#070b14", font=dict(color="#eaf1ff"))
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                #cumulative display of employee details for reporting manager
                with st.expander(f"Open Report - {emp}"):
                    st.markdown("#### Employee Details")
                    table_height = min(max(400, len(emp_df) * 35), 1200)
                    st.dataframe(
                        emp_df,
                        use_container_width=True,
                        height=table_height
                    )
                    if self.status_col:
                        st.markdown("#### Status Breakdown")
                        fig = px.pie(
                            emp_df,
                            names=self.status_col,
                            hole=0.45,
                            color_discrete_sequence=["#a8e6a8", "#1b4d2e", "#c2f0c2", "#2d5016", "#1a6b34"]
                        )
                        fig.update_layout(plot_bgcolor="rgba(124,92,255,0.08)", paper_bgcolor="#070b14", font=dict(color="#eaf1ff"))
                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            key=f"status_pie_{emp}"
                        )
                    if self.date_col:
                        temp = emp_df.copy()
                        temp[self.date_col] = pd.to_datetime(
                            temp[self.date_col],
                            errors="coerce"
                        )
                        st.markdown("#### Timeline")
                        fig2 = px.histogram(
                            temp,
                            x=self.date_col,
                            nbins=20,
                            color_discrete_sequence=["#a8e6a8"]
                        )
                        fig2.update_layout(plot_bgcolor="rgba(124,92,255,0.08)", paper_bgcolor="#070b14", font=dict(color="#eaf1ff"))
                        st.plotly_chart(
                            fig2,
                            use_container_width=True,
                            key=f"timeline_histogram_{emp}"
                        )
                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "Excel Report",
                            data=open(self.to_excel(emp_df), "rb"),
                            file_name=f"{emp}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            "PDF Report",
                            data=open(self.to_pdf(emp_df, emp), "rb"),
                            file_name=f"{emp}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
            st.markdown("<br>", unsafe_allow_html=True)

#Function call
def show_reports():
    app = ReportsDashboard("Job_list.xlsx")
    app.show_reports()

if __name__ == "__main__":
   show_reports()