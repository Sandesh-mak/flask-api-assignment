import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/students"

st.set_page_config(page_title="Student Management System", layout="wide")
st.title("🎓 Student Management Dashboard")

# Function to fetch all students
def fetch_students():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to load students from API.")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend server: {e}")
        return []

students = fetch_students()

# --- Sidebar: Add Student ---
st.sidebar.header("➕ Add New Student")
with st.sidebar.form("add_student_form", clear_on_submit=True):
    new_name = st.text_input("Name")
    new_dept = st.text_input("Department")
    new_email = st.text_input("Email")
    add_submitted = st.form_submit_button("Add Student")
    
    if add_submitted:
        if new_name and new_dept and new_email:
            payload = {"name": new_name, "department": new_dept, "email": new_email}
            res = requests.post(API_URL, json=payload)
            if res.status_code == 201:
                st.sidebar.success("Student added successfully!")
                st.rerun()
            else:
                st.sidebar.error("Failed to add student.")
        else:
            st.sidebar.warning("Please fill out all fields.")

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Student Directory")
    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No student records found.")

with col2:
    st.subheader("✏️ Update Student")
    if students:
        student_options = {f"ID {s['id']} - {s['name']}": s for s in students}
        selected_label = st.selectbox("Select Student to Update", list(student_options.keys()))
        selected_student = student_options[selected_label]
        
        with st.form("update_student_form"):
            up_name = st.text_input("Name", value=selected_student['name'])
            up_dept = st.text_input("Department", value=selected_student['department'])
            up_email = st.text_input("Email", value=selected_student['email'])
            update_submitted = st.form_submit_button("Update Student")
            
            if update_submitted:
                payload = {"name": up_name, "department": up_dept, "email": up_email}
                res = requests.put(f"{API_URL}/{selected_student['id']}", json=payload)
                if res.status_code == 200:
                    st.success("Student updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update student.")
    else:
        st.write("No students available to update.")

    st.divider()

    st.subheader("🗑️ Delete Student")
    if students:
        del_options = {f"ID {s['id']} - {s['name']}": s['id'] for s in students}
        del_label = st.selectbox("Select Student to Delete", list(del_options.keys()))
        del_id = del_options[del_label]
        
        if st.button("Delete Student", type="primary"):
            res = requests.delete(f"{API_URL}/{del_id}")
            if res.status_code == 200:
                st.success("Student deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete student.")
    else:
        st.write("No students available to delete.")