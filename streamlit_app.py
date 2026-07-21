import streamlit as st
import requests
BASE_URL = "http://127.0.0.1:8000"
DAYS_ORDER = ["Mon", "Tue","Wed","Thu", "Fri","Sat","Sun"]

st.title("Study Planner")
#3 session variables for login and user tracking

if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None
menu =["User","Login","Subject","Schedule","Today", "Progress","Dashboard"]   

choice = st.sidebar.selectbox("Menu", menu)
#converting the   file in to json files
def safe_json(res):
    try:
        return res.json()
    except Exception:
        return res.text

if choice== "User":
    st.header("Creating Account")
    email= st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Creating"):
        res = requests.post(f"{BASE_URL}/users",json={"email": email, "password":password})
        if res.status_code==200:
            st.success(f"Account created ! your user id  is {res.json()['id']}")

        else:
            st.error(safe_json(res).get("detail", "Something went wrong"))
# choice login
elif choice == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        res = requests.post(f"{BASE_URL}/login", json={
                    "email": email,
                    "password": password
        })
        data = safe_json(res)
        if res.status_code == 200:
            data= res.json()
            st.session_state.token = data["access_token"]
            st.session_state.user_id = data["user_id"]
            st.success(f"Logged in! User id: {data['user_id']}")
        else:
            st.error(safe_json(res).get("detail", "Login failed")) 

    if st.session_state.token:
            st.divider()
            st.caption("Tested the protected endpoints")
            if st.button("Call /me (requires valid token)"):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                res = requests.get(f"{BASE_URL}/me", headers=headers)
                st.write(safe_json(res))
    # Subjects 
        
elif choice == "Subject":
    if not st.session_state.token:
        st.error("Please login first")
        st.stop()

    st.header("Add a Subject")
    name = st.text_input("Name")
    difficulty =st.selectbox("Difficulty", ["easy", "medium", "hard"])
    hours =st.number_input("Hours", 1, 10)
    default_user_id = st.session_state.user_id if st.session_state.user_id else 1
    user_id = st.number_input("User ID", 1, value=default_user_id)
    if st.button("Add"):
        res = requests.post(f"{BASE_URL}/subjects", json={
            "name": name,
            "difficulty": difficulty,
            "hours": hours,
            "user_id": user_id
        })
        data = safe_json(res)
        if res.status_code == 200:
            st.success(safe_json(res))
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Error"))

    st.divider()
    st.subheader("Your Subjects")
    view_id = st.number_input("View Subjects for user id", 1, key="view_subj")

    if st.button("Load"):
        res = requests.get(f"{BASE_URL}/subjects/{view_id}")
        subjects = safe_json(res)

        if subjects:
            st.table(subjects)
        else:
            st.info("No subjects yet")

# Adding the Sehedule
elif choice == "Schedule":
    """if not st.session_state.token:
        st.error("Please login first")
        st.stop()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
"""
    st.header("Add to Schedule")
    day=st.selectbox("Day", DAYS_ORDER)
    duration =st.number_input("Duration (hours)",1,5)
    subject_id =st.number_input("Subject ID",1)
               
    if st.button("Add"):
        res = requests.post(
            f"{BASE_URL}/schedule",
            json={
                "day": day,"duration": duration,"subject_id": subject_id
            },headers=headers)

        data = safe_json(res)
        if res.status_code == 200:
            st.success("Added successfully ")
        else:
            st.error(data if isinstance(data, str) else data.get("detail", "Error"))

    st.divider()
    st.subheader("Weekly Calendar")
    cal_id = st.number_input("Show calendar for User ID", 1, key="cal_user")

    if st.button("Show Calendar"):
        res = requests.get(f"{BASE_URL}/schedule/{cal_id}", headers=headers)
        schedule = safe_json(res)

    if not isinstance(schedule, list):
            st.error("Invalid response from server")
            st.stop()


    


