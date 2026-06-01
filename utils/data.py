import pandas as pd
def get_employees()->pd.DataFrame:
    raw_df=pd.read_excel(r"C:\Users\jaspherfaithlins\Downloads\employeefinal.xlsx")
    raw_df.columns=raw_df.columns.str.strip()
    df=pd.DataFrame()
    df["Employee ID"]=raw_df.iloc[:,0].astype(str).str.strip()
    df["Employee Name"]=raw_df.iloc[:,1].astype(str).str.strip()
    df["Department"]=raw_df.iloc[:,2].astype(str).str.strip()
    df["Designation"]=raw_df.iloc[:,3].astype(str).str.strip()
    df["Status"]=raw_df.iloc[:,4].astype(str).str.strip()
    df["Role"]=raw_df.iloc[:,5].astype(str).str.strip()
    df["Username"]=raw_df.iloc[:,6].astype(str).str.strip()

    return df



