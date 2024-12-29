import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import base64
import logging, os
from pathlib import Path
from utils.database import init_db, get_comments, add_comment, add_message, get_next_anon_number

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



def display_reply(reply):
    st.write(f"↳ **{reply[1]}**: {reply[3]}")
    st.caption(f"回复于 {reply[5]}")

def display_comment(comment):
    st.write(f"**{comment[1]}**: {comment[3]}")
    st.caption(f"发表于 {comment[5]}")
    
    # Use button styled as link for reply
    reply_key = f"reply_button_{comment[0]}"
    if st.button("回复 ↩", key=reply_key, type="secondary", help="点击回复此评论"):
        st.session_state.reply_to = comment[0]
        st.experimental_rerun()
    
    # Display replies
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
        comment_text = st.text_area("添加您的评论:", key="new_comment")
        
        if st.form_submit_button("提交"):
            if comment_text:
                try:
                    next_num = get_next_anon_number()
                    name = f"anon_{next_num}"
                    email = f"anon_{next_num}@anonymous.com"
                    parent_id = st.session_state.get('reply_to', None)
                    add_comment(name, email, comment_text, parent_id)
                    if 'reply_to' in st.session_state:
                        del st.session_state.reply_to
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"评论失败: {str(e)}")
            else:
                st.error("请输入评论内容")

def show_authors():
    st.markdown("## 关于作者")
    
    # First Author
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("image/Xiufeng_liu.png", width=200)
    with col2:
        st.markdown("### 刘秀峰 (Xiufeng Liu)")
        st.markdown("""
        刘秀峰现为丹麦科技大学（Technical University of Denmark）技术、管理与经济学部高级研究员(副教授)。
        2012年，他获得丹麦奥尔堡大学计算机科学博士学位。2013年至2014年，他在加拿大滑铁卢大学从事博士后研究，
        并在IBM多伦多研发中心担任研究科学家。他的研究方向包括智能电表数据分析、数据仓库、能源信息学以及大数据领域，
        致力于推动信息技术与能源系统的深度融合。
        """)
    
    st.markdown("---")
    
    # Second Author
    col3, col4 = st.columns([1, 3])
    with col3:
        st.image("image/zhijinwang.jpg", width=200)
    with col4:
        st.markdown("### 王智谨 (Zhijin Wang)")
        st.markdown("""
        王智谨现为中国厦门集美大学计算机工程学院副教授。2016年，他获得华东师范大学计算机科学与技术系博士学位。
        他的研究兴趣包括推荐系统、时间序列预测以及健康与医疗领域的人工智能应用。他致力于推动人工智能技术在实际应用中的创新发展，
        特别是在医疗健康相关问题上的深度探索。
        """)

def show_copyright():
    st.markdown("""
        ## 版权信息
        
        **版权所有 © 2024 刘秀峰 & 王智谨**
        
        本作品采用 [**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**](https://creativecommons.org/licenses/by-nc-nd/4.0/) 许可证进行许可。
        
        ![CC License](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png)
        
        ### 您可以：
        * **分享**：在任何媒介以任何形式复制和传播本作品
        * **引用**：在学术或非商业环境下引用本作品，只要提供适当的署名
        
        ### 您不得：
        * **商业化使用**：将本作品用于任何商业目的，包括销售、广告或营利活动
        * **演绎**：修改、改编或以任何方式创作本作品的衍生作品
        
        ### 署名要求：
        * 任何使用本作品的人必须明确标注作者姓名（刘秀峰 & 王智谨），书名《AI 全景探索：人工智能的未来之旅》，并提供到本书的原始来源或链接。
        
        ### 免责声明：
        * 本书所表达的观点仅代表作者个人，与任何相关机构无关。本书内容仅供参考，作者对任何因使用本书内容而产生的后果不承担任何责任。
        
        ### 联系方式：
        * 电子邮件：[xiufengliu@gmail.com](mailto:xiufengliu@gmail.com), [zhijinecnu@gmail.com](mailto:zhijinecnu@gmail.com)
        * 网址：[https://xiufengliu.github.io](https://xiufengliu.github.io)
        
        有关本许可证的完整条款，请访问：[https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)
    """)


def show_contact_form():
    st.markdown("## 联系作者")
    with st.form(key='contact_form'):
        name = st.text_input("您的姓名:")
        email = st.text_input("您的邮箱:")
        message = st.text_area("您的留言:")
        
        if st.form_submit_button("发送"):
            if name and email and message:
                add_message(name, email, message)
                st.success("消息已发送！作者会尽快回复。")
            else:
                st.error("请填写所有字段")


def show_donation():
    st.markdown("## 支持我们")
    st.markdown("""
    创作不易，如果您觉得这本书对您有价值，欢迎您通过以下方式支持我们继续创作。
    您的每一份支持都是我们持续创作的动力！
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 微信支付")
        st.image("image/wechat_qr.png", width=180)
        
    with col2:
        st.markdown("### 支付宝")
        st.image("image/alipay_qr.png", width=180)
    
    st.markdown("""
    **感谢您的支持！**
    
    您的支持将帮助我们:
    - 持续更新和完善内容
    - 开发更多开源教育资源
    - 支持更多AI教育项目
    - 为读者提供更好的阅读体验
    """)


def show():
    try:       
        init_db()
        # --- Header Section ---
        st.title("AI全景探索：人工智能的未来之旅")
        st.markdown("### 一本开源书籍，探索人工智能的未来")

        # --- Book Cover and Download ---
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image("image/book_cover.png", caption="Book Cover", use_column_width=True)
            st.markdown("### 引用本书")
            with st.expander("BibTeX 格式"):
                st.code("""@book{liu2024ai,
                    title={AI 全景探索：人工智能的未来之旅},
                    author={刘秀峰 and 王智谨},
                    year={2024},
                    publisher={开源出版},
                    url={https://github.com/xiufengliu/ai-panorama-site},
                    note={开源电子书}
                }""", language="bibtex")

            with st.expander("APA 格式"):
                st.code("""刘秀峰, & 王智谨. (2024). AI 全景探索：人工智能的未来之旅. 开源出版. 
        https://github.com/xiufengliu/ai-panorama-site""")
            

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
                
                ### [📥 Github下载](https://raw.githubusercontent.com/xiufengliu/ai-panorama-site/refs/heads/main/data/AI_book_v1.pdf)
                """
            )
            # Add local file download
            pdf_file_path = "data/AI_book_v1.pdf"
            try:
                with open(pdf_file_path, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(
                    label="📥 本地下载",
                    data=PDFbyte,
                    file_name="AI全景探索.pdf",
                    mime='application/pdf'
                )
            except FileNotFoundError:
                st.error("PDF文件未找到")

            

        # --- Book Introduction ---
        st.markdown("---")
        st.markdown("## 内容简介")
        st.markdown(
            """
           随着人工智能技术的飞速发展，我们正站在一个时代的转折点。《AI全景探索》旨在引导读者踏上一段探索人工智能未来的旅程。本书不仅仅局限于技术层面的探讨，更深入到哲学与文化的层面，思考 AI 对人类社会、工作、生活乃至存在意义的影响。
    **章节概览:**
    *   **第一章：机器的觉醒 - 与 AI 的第一次接触:** 通过故事与案例，介绍 AI 的基本概念与其在不同领域的初次应用。
    *   **第二章：AI 的神话与现实:** 剖析 AI 的误解与现实，深入探讨技术潜力与局限。
    *   **第三章：AI 的基础 - 理解技术与背后的伟大思想:** 解析核心技术与哲学思考，展示技术如何发展至今。
    *   **第四章：无声革命 - AI 如何融入日常生活:** 探索 AI 在家庭、交通、健康等日常领域的深远影响。
    *   **第五章：思维机器的艺术 - 聚焦生成式 AI:** 深入研究生成式 AI 的原理及其带来的文化和技术变革。
    *   **第六章：教育的智变 - AI 如何塑造学习的未来:** 讨论 AI 在教育中的应用，及其如何重新定义学习方式。
    *   **第七章：医疗新前沿 - AI 在健康中的革命:** 阐述 AI 在精准医疗、药物研发与智能诊断中的重要角色。
    *   **第八章：金融与智慧城市 - AI 的深远影响:** 探讨 AI 在金融与城市管理中的突破与挑战。
    *   **第九章：重新定义工作 - 人工智能如何改变职场:** 分析 AI 对就业市场、职业角色及技能需求的改变。
    *   **第十章：数据驱动时代 - 人工智能的战略应用:** 介绍数据在 AI 中的核心地位及其战略意义。
    *   **第十一章：AI 的道德前沿 - 技术的光明与阴影:** 深入剖析 AI 带来的伦理问题，如算法偏见与隐私挑战。
    *   **第十二章：AI 的未来畅想 - 超越人类的可能性:** 展望 AI 在未来发展中可能达成的突破。
    *   **第十三章：人与机器的协作未来:** 探索人类与 AI 协作的可能性，关注和谐共生的愿景。
    *   **第十四章：AI 营养 - 面向每个人的技能增强:** 探讨如何借助 AI 技术提升个人能力。
    *   **第十五章：结语 - 人类与 AI 的未来共舞:** 总结 AI 对社会与人类未来的深远影响，激励共建美好未来。
            """
        )

                # Custom CSS for tab titles
        st.markdown("""
            <style>
            .stTab {
                font-size: 18px !important;
                font-weight: bold !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Tabs with icons and bold text
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💬 读者评论",
            "👥 关于作者",
            "©️ 版权信息",
            "❤️ 支持我们",
            "📧 联系我们"
        ])
        
        with tab1:
            display_comments_section()
            
        with tab2:
            show_authors()

        with tab3:
            show_copyright()
            
        with tab4:
            show_donation()
            
        with tab5:
            show_contact_form()
            

    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        logging.error(f"Application error: {str(e)}")    
