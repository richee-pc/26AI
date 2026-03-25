import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 페이지 기본 설정 (브라우저 탭 이름, 아이콘, 레이아웃)
st.set_page_config(
    page_title="AI와 함께 스마트하게 일하기: 광주아이온 특강 자료",
    page_icon="🌸",
    layout="wide"
)

# 2. 상단 Streamlit 기본 메뉴 및 여백 제거 (HTML이 가득 차 보이게 함)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    iframe {
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

def load_html():
    # 3. htmls 폴더 내 index.html 파일 경로 설정
    file_path = os.path.join("htmls", "index.html")
    
    # 4. 파일 존재 여부 확인 후 읽기
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        st.error(f"파일을 찾을 수 없습니다: {file_path}. htmls 폴더 안에 index.html 파일이 있는지 확인해 주세요!")
        return None

# 5. HTML 실행 및 화면 렌더링
html_content = load_html()

if html_content:
    # PC/노트북 환경에서 스크롤이 자연스럽게 작동하도록 높이를 넉넉히 설정(vh 사용)
    # components.html은 iframe으로 띄워지므로 스크롤 기능을 true로 설정합니다.
    components.html(html_content, height=1000, scrolling=True)

# 팁: 배포 시 로컬 서버에서는 st.write() 대신 위와 같이 components.html을 사용하여
# 기존 HTML/JS 기능을 완벽하게 보존하는 것이 가장 좋습니다.
