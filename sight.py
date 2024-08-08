import streamlit as st
from streamlit_local_storage import LocalStorage
import pandas as pd
from datetime import datetime
import json

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

# 로컬 스토리지 초기화
local_storage = LocalStorage()

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
    for stage, content in stages.items():
        with st.expander(stage, expanded=True):
            for line in content.split('\n'):
                st.write(line)


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

    # 로컬 스토리지에서 메모 데이터 불러오기
    memos_json = local_storage.getItem("visualization_memos")
    if memos_json:
        memos = json.loads(memos_json)
    else:
        memos = []

    # 메모 기능
    st.subheader("메모 작성")
    col1, col2 = st.columns([1, 2])
    with col1:
        memo_date = st.date_input("날짜 선택", datetime.now())
        memo_stage = st.selectbox("단계 선택", list(stages.keys()))
    with col2:
        user_memo = st.text_area("오늘의 시각화 훈련에 대해 메모를 남겨보세요.", height=100)

    if st.button("메모 저장"):
        new_memo = {
            'date': memo_date.isoformat(),
            'stage': memo_stage,
            'content': user_memo
        }
        memos.append(new_memo)
        local_storage.setItem("visualization_memos", json.dumps(memos))
        st.success("메모가 저장되었습니다!")

    # 과거 메모 보기
    st.subheader("과거 메모 보기")
    view_option = st.radio("보기 방식", ["캘린더", "목록"], horizontal=True)

    if view_option == "캘린더":
        cal_date = st.date_input("날짜 선택", datetime.now(), key="calendar")
        matching_memos = [memo for memo in memos if memo['date'] == cal_date.isoformat()]
        
        if matching_memos:
            for memo in matching_memos:
                with st.expander(f"{memo['stage']} - {memo['date']}", expanded=True):
                    st.markdown(f"<div class='memo-box'>{memo['content']}</div>", unsafe_allow_html=True)
        else:
            st.info("선택한 날짜의 메모가 없습니다.")
    else:
        if memos:
            for memo in sorted(memos, key=lambda x: x['date'], reverse=True):
                with st.expander(f"{memo['date']} - {memo['stage']}", expanded=False):
                    st.markdown(f"<div class='memo-box'>{memo['content']}</div>", unsafe_allow_html=True)
        else:
            st.info("저장된 메모가 없습니다.")

    # 메모 관리
    if memos:
        st.subheader("메모 관리")
        col1, col2 = st.columns(2)
        with col1:
            memo_to_delete = st.selectbox("삭제할 메모 선택", 
                                          [f"{memo['date']} - {memo['stage']}" for memo in memos])
            if st.button("선택한 메모 삭제"):
                index_to_delete = next(i for i, memo in enumerate(memos) 
                                       if f"{memo['date']} - {memo['stage']}" == memo_to_delete)
                del memos[index_to_delete]
                local_storage.setItem("visualization_memos", json.dumps(memos))
                st.success("메모가 삭제되었습니다!")
                st.experimental_rerun()
        
        with col2:
            if st.button("모든 메모 삭제"):
                local_storage.deleteItem("visualization_memos")
                st.success("모든 메모가 삭제되었습니다!")
                st.experimental_rerun()