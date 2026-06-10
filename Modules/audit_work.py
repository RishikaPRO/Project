import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from styles import load_css,page_banner
 
class AuditWorkPage:
    #read excel file
 
    AUDIT_FILE = "Audit.xlsx"
 
    def load_data(self):
        excel_file = pd.ExcelFile(self.AUDIT_FILE)
        records = []
 
        for sheet in excel_file.sheet_names:
            ws_df = pd.read_excel(self.AUDIT_FILE, sheet_name=sheet, header=None)
 
            for row in range(9, len(ws_df)):
                project_id = ws_df.iloc[row, 2]
 
                if pd.isna(project_id):
                    continue
 
                project_id = str(project_id).strip()
                #To select the required fields
 
                if not project_id:
                    continue
                if project_id.lower().startswith("note"):
                    continue
                if "release" in project_id.lower():
                    continue
                if not project_id.startswith("CS"):
                    continue
 
                records.append({
                    "Sheet": sheet,
                    "Excel_Row": row + 1,
                    "Project ID": project_id,
                    "Project Name": str(ws_df.iloc[row, 4]).strip(),
                    "Category": str(ws_df.iloc[row, 6]).strip(),
                    "Project Status": str(ws_df.iloc[row, 7]).strip(),
                    "Audit Type": str(ws_df.iloc[row, 8]).strip(),
                    "Audit Plan Date": str(ws_df.iloc[row, 9]).strip(),
                    "Auditee": str(ws_df.iloc[row, 10]).strip()
                })
 
        return pd.DataFrame(records)
    #save the particular fields
 
    def save_record(self, sheet_name, excel_row, project_status, audit_type, audit_date, auditee):
        wb = load_workbook(self.AUDIT_FILE)
        ws = wb[sheet_name]
   
        wb.save(self.AUDIT_FILE)
 
    def show(self):
        #loading styles.py for styling the page.
        load_css()
        st.markdown("""
        <div style='
        padding:20px;
            border-radius:12px;
            background:linear-gradient(90deg,#0f172a,#1e293b);
            color:white;
            margin-bottom:20px;
        '>
    <h2 style='margin:0;'>Audit Work </h2>
        </div>
                    """, unsafe_allow_html=True)

 
        try:
            df = self.load_data()
        except Exception as e:
            st.error(f"Error loading audit file: {e}")
            return
        #displaying metrics from the audit data
 
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Audits", len(df))
        c2.metric("Projects", df["Project ID"].nunique())
        c3.metric("Weeks", df["Sheet"].nunique())
 
        st.divider()
 
        search = st.text_input("Search Project ID / Project Name")
 
        if search:
            df = df[
                df["Project ID"].str.contains(search, case=False, na=False)
                |
                df["Project Name"].str.contains(search, case=False, na=False)
            ]
 
        sheet_names = sorted(df["Sheet"].unique().tolist())
        #Different tabs for displaying various sheets
 
        tabs = st.tabs(sheet_names)
 
        role = st.session_state.get("role", "")
 
        for idx, sheet in enumerate(sheet_names):
 
            with tabs[idx]:
 
                sheet_df = df[df["Sheet"] == sheet]
 
                st.dataframe(
                    sheet_df.drop(columns=["Sheet", "Excel_Row"], errors="ignore"),
                    use_container_width=True,
                    hide_index=True
                )
                #Reporting Manager dashboard only has Edit and Save options
                #Creating edit and save buttons and to display the editted details
 
                if role == "Reporting Manager" and not sheet_df.empty:
 
                    st.subheader("Edit Audit")
 
                    selected_id = st.selectbox(
                        "Select Project",
                        sheet_df["Project ID"].tolist(),
                        key=f"project_{sheet}"
                    )
 
                    selected = sheet_df[sheet_df["Project ID"] == selected_id].iloc[0]
 
                    new_status = st.text_input(
                        "Project Status",
                        selected["Project Status"],
                        key=f"status_{sheet}"
                    )
 
                    new_audit_type = st.text_input(
                        "Audit Type",
                        selected["Audit Type"],
                        key=f"type_{sheet}"
                    )
 
                    new_date = st.text_input(
                        "Audit Plan Date",
                        selected["Audit Plan Date"],
                        key=f"date_{sheet}"
                    )
 
                    new_auditee = st.text_input(
                        "Auditee",
                        selected["Auditee"],
                        key=f"auditee_{sheet}"
                    )
 
                    if st.button("Save Changes", key=f"save_{sheet}"):
 
                        self.save_record(
                            selected["Sheet"],
                            int(selected["Excel_Row"]),
                            new_status,
                            new_audit_type,
                            new_date,
                            new_auditee
                        )
 
                        st.success("Audit updated successfully.")
                        st.rerun()
 
def show_audit():
    AuditWorkPage().show()
 