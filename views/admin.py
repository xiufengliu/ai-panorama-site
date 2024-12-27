import streamlit as st
from utils.database import get_comments, delete_comment, get_messages, delete_message
import uuid
import time

def show_comments_management():
    st.subheader("评论管理")
    comments = get_comments()
    
    root_comments = [c for c in comments if c[4] is None]
    for comment in root_comments:
        with st.expander(f"评论 by {comment[1]} ({comment[2]})"):
            st.write(f"内容: {comment[3]}")
            st.write(f"时间: {comment[5]}")
            
            unique_key = str(uuid.uuid4())[:8]
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("删除主评论", key=f"del_root_{comment[0]}_{unique_key}"):
                    try:
                        delete_comment(comment[0])
                        st.success("评论已删除")
                        time.sleep(1)  # Give user time to see confirmation
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(str(e))
            
            replies = [c for c in comments if c[4] == comment[0]]
            if replies:
                st.markdown("**回复:**")
                for reply in replies:
                    st.write(f"↳ {reply[1]}: {reply[3]}")
                    st.caption(f"时间: {reply[5]}")
                    
                    reply_key = str(uuid.uuid4())[:8]
                    if st.button("删除回复", key=f"del_reply_{reply[0]}_{reply_key}"):
                        try:
                            delete_comment(reply[0])
                            st.success("回复已删除")
                            time.sleep(1)
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(str(e))

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

def check_password():
    """Returns `True` if the user had the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    # Show input for password
    st.subheader("请输入管理员密码")
    password = st.text_input("密码", type="password", key="admin_password")
    
    if st.button("登录"):
        if password == "admin1234":  # Replace with your secure password
            st.session_state.password_correct = True
            st.experimental_rerun()
        else:
            st.error("密码错误")
            return False

    return st.session_state.password_correct

def show():
    if not check_password():
        return
    
    st.title("网站管理")
    
    tab1, tab2 = st.tabs(["评论管理", "留言管理"])
    
    with tab1:
        show_comments_management()
    
    with tab2:
        show_messages_management()
    
