import streamlit as st
st.set_page_config(
    page_title="AI全景探索",
    layout="wide",
    initial_sidebar_state="collapsed"
)
from views import admin, book

def apply_custom_css():
    st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 300px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 0px;
            margin-left: -300px;
        }
        [data-testid="stVerticalBlock"] {
            padding-left: 0rem;
            padding-right: 0rem;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Sidebar navigation
    st.sidebar.title("导航")
    selection = st.sidebar.radio("前往", ["书籍", "管理"])
    
    # Display selected view
    if selection == "书籍":
        book.show()
    elif selection == "管理":
        admin.show()

if __name__ == "__main__":
    main()