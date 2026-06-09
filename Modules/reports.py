import streamlit as st
import pandas as pd
import io
from datetime import datetime
import plotly.express as px
import numpy as np
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

# Read excel data
class ExcelManager:
    def __init__(self, file_path):
        self.file_path = file_path
    def load_data(self):
        return pd.read_excel(self.file_path)
    def save_data(self, df):
        df.to_excel(self.file_path, index=False)

#Filter reports table
class ReportFilter:
    @staticmethod
    def apply_filters(df, filters: dict):
        filtered = df.copy()
        column_mapping = {
            "Employee Name": "Employee_Name",
            "Project Type": "Project_Type",
            "Project Team": "Project_Team",
            "Job Status": "Job_Status",
        }
        for label, value in filters.items():
            col = column_mapping.get(label)
            if col and value and value != "All" and col in filtered.columns:
                filtered = filtered[filtered[col] == value]
        return filtered

#Export page data
class ExportManager:
    @staticmethod
    def to_excel_bytes(df: pd.DataFrame) -> bytes:
        from openpyxl import Workbook
        from openpyxl.utils.dataframe import dataframe_to_rows
        from openpyxl.chart import BarChart, Reference
        buffer = io.BytesIO()
        wb = Workbook()
       
        #Reports export
        ws = wb.active
        ws.title = "Employee Report"
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
       
        #Charts Export
        chart_ws = wb.create_sheet("Charts")
        # Job Status
        if "Job_Status" in df.columns:
            status_counts = df["Job_Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            chart_ws.append(["Status", "Count"])
            for _, row in status_counts.iterrows():
                chart_ws.append([row["Status"], int(row["Count"])])
            chart1 = BarChart()
            chart1.title = "Job Status Distribution"
            data = Reference(chart_ws, min_col=2, min_row=2, max_row=1 + len(status_counts))
            cats = Reference(chart_ws, min_col=1, min_row=2, max_row=1 + len(status_counts))
            chart1.add_data(data, titles_from_data=False)
            chart1.set_categories(cats)
            chart_ws.add_chart(chart1, "D2")
        # Project Type
        if "Project_Type" in df.columns:
            start_row = 3 + len(df["Job_Status"].unique()) if "Job_Status" in df.columns else 2
            type_counts = df["Project_Type"].value_counts().reset_index()
            type_counts.columns = ["Project_Type", "Count"]
            chart_ws.append([])
            chart_ws.append(["Project_Type", "Count"])
            for _, row in type_counts.iterrows():
                chart_ws.append([row["Project_Type"], int(row["Count"])])
            chart2 = BarChart()
            chart2.title = "Project Type Breakdown"
            t_start = start_row + 1
            t_end = t_start + len(type_counts) - 1
            data2 = Reference(chart_ws, min_col=2, min_row=t_start, max_row=t_end)
            cats2 = Reference(chart_ws, min_col=1, min_row=t_start, max_row=t_end)
            chart2.add_data(data2, titles_from_data=False)
            chart2.set_categories(cats2)
            chart_ws.add_chart(chart2, "D15")
        wb.save(buffer)
        return buffer.getvalue()
 
    @staticmethod
    def to_pdf_bytes(df: pd.DataFrame) -> bytes:
        if plt is None:
            return None
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph("Employee Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        # Table
        data = [df.columns.tolist()] + df.astype(str).values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))
        # Job status chart
        if "Job_Status" in df.columns:
            fig, ax = plt.subplots()
            df["Job_Status"].value_counts().plot(kind="bar", ax=ax)
            img = io.BytesIO()
            fig.savefig(img, format="png")
            plt.close(fig)
            img.seek(0)
            elements.append(Image(img, width=400, height=200))
        # Project type chart
        if "Project_Type" in df.columns:
            fig, ax = plt.subplots()
            df["Project_Type"].value_counts().plot(kind="bar", ax=ax)
            img = io.BytesIO()
            fig.savefig(img, format="png")
            plt.close(fig)
            img.seek(0)
            elements.append(Image(img, width=400, height=200))
        doc.build(elements)
        return buffer.getvalue()

#UI
class ReportsPage:
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
    @classmethod
    def show_reports(cls):
        st.title("Employee Reports")
        excel_file = "job_tracker.xlsx"
        try:
            df = ExcelManager(excel_file).load_data()
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()
       
        #Filters
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        with col1:
            emp = st.selectbox("Employee Name", ["All"] + df["Employee_Name"].dropna().unique().tolist())
        with col2:
            ptype = st.selectbox("Project Type", ["All"] + df["Project_Type"].dropna().unique().tolist())
        with col3:
            status = st.selectbox("Job Status", ["All"] + df["Job_Status"].dropna().unique().tolist())
        filters = {
            "Employee Name": emp,
            "Project Type": ptype,
            "Job Status": status
        }
        filtered_df = ReportFilter.apply_filters(df, filters)
        st.write(f"Records: {len(filtered_df)}")
        st.dataframe(filtered_df, use_container_width=True)
        
        #charts
        st.subheader("Analytics")
        if not filtered_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    filtered_df,
                    names="Job_Status",
                    title="Job Status"
                )
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                type_counts = filtered_df["Project_Type"].value_counts().reset_index()
                type_counts.columns=["Project_Type", "Count"]
                fig=px.bar( type_counts,
                           x="Project_Type",
                           y="Count",
                           title= "Project Type Breakdown")

                st.plotly_chart(fig, use_container_width=True)
       
        #Data export
        st.subheader("Export")
        if st.button("Export Report"):
            excel_bytes = ExportManager.to_excel_bytes(filtered_df)
            st.download_button(
                "Download Excel",
                data=excel_bytes,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="Excel_report/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            pdf_bytes = ExportManager.to_pdf_bytes(filtered_df)
            if pdf_bytes:
                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="reports/pdf"
                )

show_reports = ReportsPage.show_reports