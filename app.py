import json
import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px
import io

Data_file = "data/jobs.json"

def load_jobs():
    try:
        with open(Data_file, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []
    

def save_jobs(jobs):
    with open(Data_file,"w") as f:
        json.dump(jobs,f,indent=2)

st.title("AI job application tracer")

with st.form("Job Application"):
    st.subheader("Add a new Job Application")
    company = st.text_input("Company Name")
    position = st.text_input("position")
    status = st.selectbox("Status", ["Applied","Interview", "Offer", "Rejected"])
    date_applied = st.date_input("Date Applied",value= date.today())
    notes = st.text_area("notes")
    submitted = st.form_submit_button("Add Job Application")

    if submitted:
        if company and position:
            jobs = load_jobs()
            new_job ={
                "company": company,
                "position": position,
                "status": status,
                "applied_on": str(date_applied),
                "notes": notes
            }
            jobs.append(new_job)
            save_jobs(jobs)
            st.success("job application added successfully")
        else:
            st.error("Please fill in all required fields.")

st.subheader("Job Application list")
jobs = load_jobs()

st.subheader("job Applications")
search_term = st.text_input("Search by company or position")
status_filter = st.selectbox("Filter by status",["All","Applied","Interview","Offer","Rejected"])
df = pd.DataFrame(jobs)

if not df.empty:
    if search_term:
        df= df[df.apply(lambda row: search_term.lower() in row["company"].lower() or search_term.lower()in row["position"].lower(),axis=1)]
    if status_filter != "All":
        df = df[df["status"] == status_filter]
    st.dataframe(df.reset_index(drop=True))
else:
    st.info("no jobs added yet")
    
if not df.empty:
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    fig = px.pie(
        status_counts,
        names="status",
        values="count",
        title="job application status distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
if not df.empty:
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download CSV",
        data = csv_buffer.getvalue(),
        file_name = "job applications.csv",
        mime = "txt/csv"
    )
    
    st.success("CSV file has been created successfully")