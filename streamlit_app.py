import streamlit as st
import requests
from collections import defaultdict
BASE_URL = "http://127.0.0.1:8000"
DAYS_ORDER = ["Mon", "Tue","Wed","Thu", "Fri","Sat","Sun"]

st.title("Study Planner")
#3 session variables for login and user tracking

if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "schedule" not in st.session_state:
    st.session_state.schedule = []
def require_login():
    if not st.session_state.token:
        st.error("Please login first")
        st.stop()    


menu =["User","Login","Subject","Schedule","Today", "Progress","Dashboard"]   

choice = st.sidebar.selectbox("Menu", menu)
#converting the   file in to json files
def safe_json(res):
    try:
        return res.json()
    except Exception:
        return res.text
# user 
if choice== "User":
    st.header("Creating Account")
    email= st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Creating"):
        res = requests.post(f"{BASE_URL}/user",json={"email": email, "password":password})
        data = safe_json(res)
        if res.status_code==200:
            st.success(f"Account created! Your user id is {data.get('id')}")
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Something went wrong")) 
# choice login
elif choice == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        res = requests.get(
            f"{BASE_URL}/login",
            params={
                "email": email,
                "password": password
            }
        )
        data = safe_json(res)
        
        if res.status_code == 200:
            st.session_state.token = data["access_token"]
            st.session_state.user_id = data["user_id"]
            st.success(f"Logged in! User id: {data['user_id']}")
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Login failed"))
            
    if st.session_state.token:
        st.divider()
        st.caption("Tested the protected endpoints")

        if st.button("Call /me (requires valid token)"):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            res = requests.get(f"{BASE_URL}/me", headers=headers)
            st.write(safe_json(res))
    # Subjects 
        
elif choice == "Subject":
    require_login() 

    st.header("Add a Subject")
    name = st.text_input("Name")
    difficulty =st.selectbox("Difficulty", ["easy", "medium", "hard"])
    hours =st.number_input("Hours", 1, 10)
    user_id = st.session_state.user_id
    if st.button("Add"):
        res = requests.post(f"{BASE_URL}/subjects", json={
            "name": name,
            "difficulty": difficulty,
            "hours": hours,
            "user_id": user_id
        })
        data = safe_json(res)
        if res.status_code == 200:
            st.success("Subject added successfully")
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Error"))

    st.divider()
    st.subheader("Your Subjects")
    view_id = st.number_input("View Subjects for user id", 1, key="view_subj")

    if st.button("Load"):
        res = requests.get(f"{BASE_URL}/subjects/{view_id}")
        subjects = safe_json(res)

        if isinstance(subjects, list) and subjects:
            st.table(subjects)
        else:
            st.info("No subjects yet")

# Adding the Sehedule
elif choice == "Schedule":
    require_login() 
    
    headers = {"Authorization":f"Bearer {st.session_state.token}"}

    st.header("Add to Schedule")
    day=st.selectbox("Day", DAYS_ORDER)
    duration =st.number_input("Duration (hours)",1,5)
    res = requests.get(f"{BASE_URL}/subjects/{st.session_state.user_id}")
    subjects = safe_json(res)

    if isinstance(subjects, list) and subjects:
        subject_options = {s["name"]: s["id"] for s in subjects}

        selected_subject = st.selectbox("Select Subject", list(subject_options.keys()))

        subject_id = subject_options[selected_subject]  
    else:
        st.warning("No subjects found. Please add subject first.")
        st.stop()

               
    if st.button("Add"):
        res = requests.post(
            f"{BASE_URL}/schedule",
            json={
                "day": day,"duration": duration,"subject_id":subject_id
            },headers=headers)

        data = safe_json(res)
        if res.status_code == 200:
            st.success("Added successfully ")
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Error"))

    st.divider()
    st.subheader("Weekly Calendar")
    
    if st.button("Show Calendar"):
        res = requests.get(
            f"{BASE_URL}/schedule/{st.session_state.user_id}",
            headers=headers)
        st.session_state.schedule = safe_json(res)

    schedule = st.session_state.schedule  

    if schedule:
        if not isinstance(schedule, list):
            st.error("Invalid response from server")
        else:
            clean_data = [
    {
        "ID": s["id"], 
        "Day": s["day"],
        "Subject": s.get("subject_name"),
        "Hours": s["duration"],
        "Status": s.get("status", "pending") 
    }
    for s in schedule
    ]


        st.table(clean_data)

    if schedule and isinstance(schedule, list):
        grouped = defaultdict(list)

        for s in schedule:
            grouped[s["day"]].append(s)

        st.divider()
        st.subheader("Day-wise View")

        for d in DAYS_ORDER:
            st.write(f"### {d}")
            for item in grouped.get(d, []):
                status = item.get("status", "pending")
                status_text = "Completed" if status == "completed" else "Pending"
                st.write(f"{status_text} | {item.get('subject_name')} ({item['duration']}h)")       

#Adding  Today events
elif choice == "Today":
    require_login() 
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.header("Today's Tasks")
    user_id = st.session_state.user_id
    if st.button("Show Today"):
        res = requests.get(f"{BASE_URL}/schedule/today/{user_id}", headers=headers)
        today_data =safe_json(res)

        if not isinstance(today_data, list):
            st.error("Invalid response from server")
            st.stop()

        if not today_data:
            st.info("No subjects scheduled for today.")
        else:
            completed =sum(1 for row in today_data if row.get("status") == "completed")
            total =len(today_data)
            percent =int((completed/total)*100) if total else 0

            st.progress(percent / 100)
            st.caption(f"{completed}/{total} completed today ({percent}%)")

            for row in today_data:
                status_text = "Completed" if row.get("status") == "completed" else "Pending"
                st.write(f"{status_text} | {row.get('subject','Unknown')} — {row.get('duration',0)}h")

#Addiing progress 
elif choice == "Progress":

    if not st.session_state.token:
        st.error("Please login first")
        st.stop()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.header("Update Task Progress")
    res = requests.get(
        f"{BASE_URL}/schedule/{st.session_state.user_id}",
        headers=headers
    )

    schedule = safe_json(res)
    if isinstance(schedule, list) and schedule:
        schedule_options = {
            f"{row['subject_name']} ({row['day']}) - {row['duration']}h - ID {row['id']}": row['id']
            for row in schedule
        }
        selected_task = st.selectbox("Select Task", list(schedule_options.keys()))
        schedule_id = schedule_options[selected_task]

    else:
        st.warning("No schedule found")
        st.stop()
    status = st.selectbox("Status", ["pending", "completed"])
    if st.button("Update"):
        res = requests.put(
            f"{BASE_URL}/progress/{schedule_id}",
            params={"status": status},
            headers=headers
        )

        data = safe_json(res)

        if res.status_code == 200:
            st.success("Updated successfully")
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Error"))           
#Adding Dashborad            
elif choice == "Dashboard":
    require_login()  
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.header("Weekly Progress Report")
    user_id = st.number_input("User ID", 1)

    if st.button("Generate Report"):
        res = requests.get(f"{BASE_URL}/report/{user_id}", headers=headers)
        data = safe_json(res)
        if not isinstance(data, dict):
            st.error("Invalid response from server")
            st.stop()

        total = data.get("total", 0)
        completed = data.get("completed", 0)
        pending = data.get("pending", 0)
        percent = data.get("percent", 0)
        by_day = data.get("by_day", {})

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total)
        col2.metric("Completed", completed)
        col3.metric("Pending", pending)

        st.progress(percent/100 if percent else 0)
        st.caption(f"{percent}% complete")

        if isinstance(by_day, dict) and by_day:
            chart_data = {d:by_day.get(d, 0) for d in DAYS_ORDER}
            st.subheader("Completed tasks per day")
            st.bar_chart(chart_data)
        else:
            st.info("No completed tasks yet.")

    


