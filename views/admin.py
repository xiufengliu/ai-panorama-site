import streamlit as st
from utils.database import get_comments, delete_comment, get_messages, delete_message

def show_comments_management():
    st.subheader("评论管理")
    comments = get_comments()
    
    for comment in comments:
        with st.expander(f"评论 by {comment[1]} ({comment[2]})"):
            st.write(f"内容: {comment[3]}")
            st.write(f"时间: {comment[5]}")
            if st.button("删除", key=f"del_comment_{comment[0]}"):
                delete_comment(comment[0])
                st.experimental_rerun()

def show_messages_management():
    st.subheader("留言管理")
    messages = get_messages()
    
    for message in messages:
        with st.expander(f"留言 by {message[1]} ({message[2]})"):
            st.write(f"内容: {message[3]}")
            st.write(f"时间: {message[4]}")
            if st.button("删除", key=f"del_message_{message[0]}"):
                delete_message(message[0])
                st.experimental_rerun()

def show():
    if not check_password():
        return
    
    st.title("网站管理")
    
    tab1, tab2 = st.tabs(["评论管理", "留言管理"])
    
    with tab1:
        show_comments_management()
    
    with tab2:
        show_messages_management()