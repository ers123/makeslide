import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(layout="centered", page_title="시각화 훈련 가이드")

# CSS 스타일 정의
st.markdown("""
<style>
    .main {max-width: 1200px; padding: 2rem; margin: 0 auto;}
    .stExpander {border: none; box-shadow: 0 2px 5px 0 rgba(0,0,0,0.16);}
    .stExpander > div:first-child {
        border-radius: 5px;
        padding: 0.5rem;
        background-color: #f0f2f6;
    }
    .stExpander > div:first-child p {font-weight: bold; margin: 0;}
    .stExpander > div:last-child {padding: 1rem;}
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
        color: white;
    }
    .memo-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 메인 컨테이너
main_container = st.container()

with main_container:
    st.title("시각화 훈련 가이드")

    # 데이터 준비
    stages = {
        "1단계: 기본 시각화 연습": "간단한 도형 상상하기 (원, 삼각형, 정육면체 등)\n눈을 감고 1분간 유지해보기\n색상, 크기, 질감 등 세부 사항에 집중",
        "2단계: 정적 이미지 시각화": "익숙한 물건이나 장소 상상하기 (예: 사과, 집)\n2-3분간 이미지 유지\n세부 사항 (색상, 형태, 질감) 추가하기",
        "3단계: 동적 이미지 시각화": "움직이는 대상 상상하기 (예: 흐르는 강, 날아가는 새)\n3-5분간 장면 유지\n움직임의 세부 사항에 집중",
        "4단계: 복잡한 장면 시각화": "여러 요소가 있는 장면 상상하기 (예: 번화한 거리, 자연 풍경)\n5분 이상 장면 유지\n시각적 요소뿐만 아니라 소리, 냄새 등 다감각적 요소 추가",
        "5단계: 추상적 개념 시각화": "감정, 아이디어 등 추상적 개념을 이미지로 표현\n7-10분간 이미지 유지 및 발전\n개인적 의미와 연관 지어 상상력 확장"
    }

    # 5단계 시각화
    st.subheader("훈련 단계")
    for i, (stage, content) in enumerate(stages.items()):
        with st.expander(stage.split(':')[0], expanded=True):
            for line in content.split('\n'):
                st.write(f"• {line}")

    # 실천 팁과 진전 측정
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("실천 팁")
        tips = [
            "매일 10-15분씩 연습",
            "편안한 자세와 조용한 환경에서 시작",
            "점진적으로 난이도와 지속 시간 증가",
            "시각화 후 내용을 글이나 그림으로 기록",
            "명상 앱이나 가이드 오디오 활용"
        ]
        for tip in tips:
            st.write(f"• {tip}")

    with col2:
        st.subheader("진전 측정")
        progress = [
            "시각화의 선명도, 지속 시간, 복잡성 기록",
            "주간 자가 평가로 발전 상황 체크",
            "다른 인지 기능 (기억력, 창의성 등)의 변화 관찰"
        ]
        for prog in progress:
            st.write(f"• {prog}")

    # 메모 기능
    st.subheader("메모 작성")
    col1, col2 = st.columns([1, 2])
    with col1:
        memo_date = st.date_input("날짜 선택", datetime.now())
        memo_stage = st.selectbox("단계 선택", list(stages.keys()))
    with col2:
        user_memo = st.text_area("오늘의 시각화 훈련에 대해 메모를 남겨보세요.", height=100)

    if st.button("메모 작성"):
        st.success("메모가 작성되었습니다. 이 메모는 임시적으로 표시되며, 페이지를 새로고침하면 사라집니다.")
        st.markdown(f"<div class='memo-box'><strong>{memo_date} - {memo_stage}</strong><br>{user_memo}</div>", unsafe_allow_html=True)

    st.warning("주의: 이 앱은 메모를 저장하지 않습니다. 중요한 내용은 따로 기록해 두세요.")