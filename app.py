import streamlit as st
import pandas as pd
from database import create_database, save_job, get_all_jobs, delete_job, filter_jobs, update_job_status, get_job_stats, search_jobs
create_database()
st.title("Smart Job Tracker")
total, applied, interview, offer, rejected = get_job_stats()
col1,col2,col3,col4,col5=st.columns(5)
with col1:
    st.metric("Total",total)
with col2:
    st.metric("Applied",applied)
with col3:
    st.metric("Interview",interview)
with col4:
    st.metric("Offer",offer)
with col5:
    st.metric("Rejected",rejected)
search_term=st.text_input("Search by Company Name")
if search_term:
    jobs=search_jobs(search_term)
else:
    jobs=get_all_jobs()
st.subheader("Add New Job Application")
company=st.text_input("Company Name")
role=st.text_input("Job Role")
date_applied=st.date_input("Date Applied")
status=st.selectbox("Application Status",["Applied","Assessment","Interview","Rejected","Offer"])
notes=st.text_area("Notes")
if st.button("Save Job"):
    st.write("Button clicked")
    if company.strip() == "" or role.strip() == "":
        st.error("Company name and Job role are required!")
    else:
        save_job(company,role,date_applied,status,notes)
        st.success("Job saved to database successfully!") 
st.subheader("Saved Applications")
selected_status=st.selectbox("Filter by Status",["All", "Applied", "Assessment", "Interview", "Rejected", "Offer"])

if selected_status!="All":
    jobs=[job for job in jobs if job[4]==selected_status]

if jobs:
    df=pd.DataFrame(jobs, columns=["ID","Company","Role","Date","Status","Notes"])
    csv=df.to_csv(index=False)
    st.download_button(label="Export to CSV",data=csv,file_name="job_applications.csv",mime="text/csv")

for job in jobs:
    st.write(f"Company:{job[1]}")
    st.write(f"Roles:{job[2]}")
    st.write(f"Date:{job[3]}")
    new_status=st.selectbox(f"Update status for {job[1]}", ["Applied","Assessment","Interview","Rejected","Offer"], index=["Applied","Assessment","Interview","Rejected","Offer"].index(job[4]),key=f"status_{job[0]}")
    st.write(f"Notes:{job[5]}")
    if st.button("Update", key=f"update_{job[0]}"):
        update_job_status(job[0],new_status)
        st.rerun()

    if st.button("Delete",key=f"delete_{job[0]}"):
        delete_job(job[0])
        st.rerun()
    st.divider()
