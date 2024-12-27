import streamlit as st
import logging
from pathlib import Path
from utils.database import init_db, get_comments, add_comment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent / 'app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Comment display functions
def display_reply(reply):
    st.write(f"↳ **{reply[1]}**: {reply[3]}")
    st.caption(f"回复于 {reply[5]}")

def display_comment(comment):
    st.write(f"**{comment[1]}**: {comment[3]}")
    st.caption(f"发表于 {comment[5]}")
    
    reply_key = f"reply_button_{comment[0]}"
    if st.button("回复", key=reply_key):
        st.session_state.reply_to = comment[0]
        st.experimental_rerun()
    
    replies = get_comments(parent_id=comment[0])
    if replies:
        with st.container():
            for reply in replies:
                col1, col2 = st.columns([1, 20])
                with col2:
                    display_reply(reply)


def display_comments_section():
    st.markdown("## 读者评论")
    comments = get_comments()
    
    for comment in comments:
        with st.container():
            display_comment(comment)
            st.markdown("---")
    
    with st.form(key='comment_form'):
        name = st.text_input("您的姓名:")
        email = st.text_input("您的邮箱:")
        if 'reply_to' in st.session_state:
            parent_comment = next((c for c in comments if c[0] == st.session_state.reply_to), None)
            comment_text = st.text_area(
                f"回复 {parent_comment[1]}:" if parent_comment else "添加您的评论:", 
                key="new_comment"
            )
        else:
            comment_text = st.text_area("添加您的评论:", key="new_comment")
        
        if st.form_submit_button("提交"):
            if name and email and comment_text:
                parent_id = st.session_state.get('reply_to', None)
                add_comment(name, email, comment_text, parent_id)
                if 'reply_to' in st.session_state:
                    del st.session_state.reply_to
                st.experimental_rerun()
            else:
                st.error("请填写所有必填字段")





def main():
    try:
        st.set_page_config(page_title="AI全景探索", page_icon="🤖", layout="wide")
        init_db()

        # --- Header Section ---
        st.title("AI全景探索：人工智能的未来之旅")
        st.markdown("### 一本开源书籍，探索人工智能的未来")

        # --- Book Cover and Download ---
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image("image/book_cover.png", caption="Book Cover", use_column_width=True)

        with col2:
            st.markdown(
                """
                ## 欢迎来到《AI全景探索》的世界！

                本书从技术、哲学和文化等多个视角，深入探讨人工智能的未来发展。
                我们希望与您一起，在这个充满变革的时代，重新思考人类与技术的关系。

                **本书特色:**
                *   **多重视角:** 融合技术、哲学和文化，提供全面的 AI 洞察。
                *   **开源协作:** 采用开放的协作模式, 任何人都可以参与贡献。
                *   **深度思考:** 引发读者对 AI 伦理、社会影响等问题的深入思考。
                *   **面向未来:** 不仅回顾过去，更着眼于 AI 的未来发展趋势。
                """
            )
            with open("data/AI_book_v1.pdf", "rb") as f:
                st.download_button(
                    label="📥 下载本书 PDF",
                    data=f,
                    file_name="AI全景探索.pdf",
                    mime="application/pdf",
                )

        # --- Book Introduction ---
        st.markdown("---")
        st.markdown("## 内容简介")
        st.markdown(
            """
            随着人工智能技术的飞速发展，我们正站在一个时代的转折点。
            《AI全景探索》旨在引导读者踏上一段探索人工智能未来的旅程。
            本书不仅仅局限于技术层面的探讨，更深入到哲学与文化的层面，
            思考 AI 对人类社会、工作、生活乃至存在意义的影响。

            **章节概览:**

            *   **第一章：AI 的现状与发展趋势:**  回顾 AI 的发展历程，介绍当前的关键技术和应用领域。
            *   **第二章：重新定义工作 - 人工智能如何改变职场:** 探讨 AI 对就业市场、职业技能和人机协作模式的影响。
            *   **第三章：伦理与监管的挑战:** 分析 AI 带来的伦理问题，如算法偏见、隐私保护等，并探讨监管框架的构建。
            *   **第四章：AI 的哲学思考:** 从哲学角度探讨 AI 与人类的关系，思考 AI 时代的劳动意义、人类价值等问题。
            *   **第五章：未来展望:** 展望 AI 技术的未来发展方向，以及人类如何与 AI 共同塑造未来。
            """
        )

        # --- Author Introduction ---
        st.markdown("---")
        st.markdown("## 关于作者")
        st.markdown(
            """
            这里写上作者信息, 例如作者的背景、研究方向、联系方式等。

            也可以是一个多人协作的作者列表。
            """
        )

    # --- Comments Section ---
        st.markdown("---")
        display_comments_section()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        logging.error(f"Application error: {str(e)}")    

if __name__ == "__main__":
    main()