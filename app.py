import streamlit as st
import sqlite3

# --- Database Functions ---
def create_db():
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            comment TEXT,
            parent_id INTEGER DEFAULT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

def add_comment(name, email, comment, parent_id=None):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (name, email, comment, parent_id) VALUES (?, ?, ?, ?)",
        (name, email, comment, parent_id),
    )
    conn.commit()
    conn.close()

def get_comments(parent_id=None):
    conn = sqlite3.connect("comments.db")
    cursor = conn.cursor()
    if parent_id is None:
        cursor.execute("SELECT * FROM comments WHERE parent_id IS NULL ORDER BY timestamp DESC")
    else:
        cursor.execute(
            "SELECT * FROM comments WHERE parent_id = ? ORDER BY timestamp ASC", (parent_id,)
        )
    comments = cursor.fetchall()
    conn.close()
    return comments

# --- Initialize Database ---
create_db()

# --- Main App ---
def main():
    st.set_page_config(page_title="AI全景探索", page_icon="🤖", layout="wide")

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
        with open("path/to/your/book.pdf", "rb") as f:
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
    st.markdown("## 读者评论")

    comments = get_comments()

    def display_comment(comment):
        # Display the comment
        with st.chat_message("user"):
            st.markdown(f"**{comment[1]}**: {comment[3]}")

            # Reply button
            reply_key = f"reply_button_{comment[0]}"
            if st.button("回复", key=reply_key):
                st.session_state.reply_to = comment[0]
                st.experimental_rerun()

            # Display replies
            replies = get_comments(parent_id=comment[0])
            if replies:
                for reply in replies:
                    with st.chat_message("assistant"):
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;↳ **{reply[1]}**: {reply[3]}")

    # Display each comment and its replies
    for comment in comments:
        display_comment(comment)

    # Form to add a new comment or reply
    with st.form(key='comment_form'):
        name = st.text_input("您的姓名:")
        email = st.text_input("您的邮箱:")
        if 'reply_to' in st.session_state:
            replying_to = next((c for c in comments if c[0] == st.session_state.reply_to), None)
            if replying_to:
                new_comment = st.text_area(f"回复 {replying_to[1]}:", key="new_comment")
            else:
                new_comment = st.text_area("添加您的评论:", key="new_comment")
        else:
            new_comment = st.text_area("添加您的评论:", key="new_comment")

        submit_button = st.form_submit_button(label="提交")

        if submit_button:
            if name and email and new_comment:
                parent_id = st.session_state.pop('reply_to', None)  # Get and clear reply_to
                add_comment(name, email, new_comment, parent_id)
                st.success("评论/回复已提交！")
                st.experimental_rerun()
            else:
                st.warning("请填写所有字段。")

    # --- Contact Form ---
    st.markdown("---")
    st.markdown("## 联系作者")
    with st.form(key="contact_form"):
        name = st.text_input("您的姓名:", key="contact_name")
        email = st.text_input("您的邮箱:", key="contact_email")
        message = st.text_area("您的留言:", key="contact_message")
        submit_button = st.form_submit_button(label="发送留言")

        if submit_button:
            if name and email and message:
                # Add logic here to send the message (e.g., via email)
                st.success(
                    f"感谢您的留言，{name}！我们会尽快回复您。"
                )
            else:
                st.warning("请填写所有字段。")

if __name__ == "__main__":
    main()