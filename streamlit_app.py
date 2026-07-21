import streamlit as st
import requests
BASE_URL = "http://127.0.0.1:8000"
DAYS_ORDER = ["Mon", "Tue","Wed","Thu", "Fri","Sat","Sun"]

st.title("Study Planner")
if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None
    

     