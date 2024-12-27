import streamlit as st
from utils.database import get_comments, delete_comment

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        with st.form("login"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            if st.form_submit_button("Login"):
                if (st.session_state.username == "admin" and 
                    st.session_state.password == "your_secure_password"):
                    st.session_state.authenticated = True
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
        return False
    return True

def show():
    if not check_password():
        return
    
    st.title("评论管理")
    comments = get_comments()
    
    for comment in comments:
        with st.expander(f"评论 by {comment[1]} ({comment[2]})"):
            st.write(f"内容: {comment[3]}")
            st.write(f"时间: {comment[5]}")
            if st.button("删除", key=f"del_{comment[0]}"):
                delete_comment(comment[0])
                st.experimental_rerun()