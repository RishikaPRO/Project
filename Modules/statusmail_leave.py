import streamlit as st
import pandas as pd
from datetime import datetime
# ---------------- CONFIG ----------------
EXCEL_FILE = "reporting_manager_dashboard.xlsx"
TOTAL_LEAVE = 24
DEDUCTIBLE = {"P", "UP", "C", "ML", "PL", "Co", "H1", "H2"}

#excel document loading process
class ExcelManager:
   def __init__(self, file_path):
       self.file_path = file_path
   def load_data(self, sheet_name):
       return pd.read_excel(
           self.file_path,
           sheet_name=sheet_name,
           engine="openpyxl"
       )

#status mail summary
class StatusMailProcessor:
   @staticmethod
   def process(df):
       df = df.copy()
       df["MailSent"] = df["MailSent"].fillna("No")
       summary = df.groupby("Employee").agg(
           Total=("MailSent", "count"),
           Sent=("MailSent", lambda x: (x.str.lower() == "yes").sum()),
           Last_Sent_Date=("Date", "max")
       ).reset_index()
       summary["Pending"] = summary["Total"] - summary["Sent"]
       summary["Completion %"] = (summary["Sent"] / summary["Total"]) * 100
       return df, summary

#leave summary
class LeaveProcessor:
   @staticmethod
   def compute(df):
       df = df.copy()
       def calc(x):
           if x in ["H1", "H2"]:
               return 0.5
           if x in DEDUCTIBLE:
               return 1
           return 0
       df["LeaveValue"] = df["LeaveType"].apply(calc)
      
       # Total leave
       total = df.groupby("Employee")["LeaveValue"].sum().reset_index()
       total.rename(columns={"LeaveValue": "Total_Leave_Taken"}, inplace=True)
       total["Leave_Remaining"] = TOTAL_LEAVE - total["Total_Leave_Taken"]
      
       # Monthly leave
       now = datetime.now()
       monthly = df[
           (df["Date"].dt.month == now.month) &
           (df["Date"].dt.year == now.year)
       ].groupby("Employee")["LeaveValue"].sum().reset_index()
       monthly.rename(columns={"LeaveValue": "Monthly_Leave"}, inplace=True)
       # Yearly leave
       yearly = df[df["Date"].dt.year == now.year] \
           .groupby("Employee")["LeaveValue"].sum().reset_index()
       yearly.rename(columns={"LeaveValue": "Yearly_Leave"}, inplace=True)
       
       #overall leave calculations
       final = total.merge(monthly, on="Employee", how="left") \
                    .merge(yearly, on="Employee", how="left") \
                    .fillna(0)
       return df, final

#dashboard upon opening
class ReportingManagerDashboard:
   @classmethod
   def show_statusmail(cls):
       st.title("Status Mail Dashboard")
       excel = ExcelManager(EXCEL_FILE)
       try:
           status_df = excel.load_data("status_mail")
           status_df["Date"] = pd.to_datetime(status_df["Date"])
       except Exception as e:
           st.error(f"Error loading status mail data: {e}")
           st.stop()
       raw, summary = StatusMailProcessor.process(status_df)
       st.subheader("Summary")
       st.dataframe(summary)
       st.bar_chart(summary.set_index("Employee")[["Sent", "Pending"]])

   @classmethod
   def show_leave_records(cls):
       st.title("Leave Records Dashboard (Reporting Manager)")
       excel = ExcelManager(EXCEL_FILE)
       try:
           leave_df = excel.load_data("leave_records")
           leave_df["Date"] = pd.to_datetime(leave_df["Date"])
       except Exception as e:
           st.error(f"Error loading leave data: {e}")
           st.stop()
       raw, summary = LeaveProcessor.compute(leave_df)
       st.subheader("Leave Summary")
       st.dataframe(summary)
       st.bar_chart(
           summary.set_index("Employee")[[
               "Total_Leave_Taken",
               "Monthly_Leave",
               "Yearly_Leave",
               "Leave_Remaining"
           ]]
       )

#function exports
def show_statusmail():
   ReportingManagerDashboard.show_statusmail()

def show_leave_records():
   ReportingManagerDashboard.show_leave_records()