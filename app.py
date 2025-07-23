import json
import streamlit as st
from datetime import date

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
                "Company": company,
                "Position": position,
                "Status": status,
                "Date Applied": str(date_applied),
                "Notes": notes
            }
            jobs.append(new_job)
            save_jobs(jobs)
            st.success("job application added successfully")
        else:
            st.error("Please fill in all required fields.")

st.subheader("Job Application list")
jobs = load_jobs()
st.write(jobs)