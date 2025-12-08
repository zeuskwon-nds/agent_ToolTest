#!/usr/bin/env python3
"""
건강 데이터 AI Agent - 고급 Streamlit 웹 UI
DB Search 최적화 버전
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from strands_health_agent import HealthChatAgent
from text_to_sql_tool import TextToSQLTool
from datetime import datetime
import json
import re

# 페이지 설정
st.set_page_config(
    page_title="건강 데이터 AI Agent",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
        border-left: 4px solid #4caf50;
    }
    .quick-action {
        background-color: #fff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .quick-action:hover {
        border-color: #2196f3;
        box-shadow: 0 2px 8px rgba(33,150,243,0.2);
    }
    .stButton>button {
        border-radius: 0.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'agent' not in st.session_state:
    st.session_state.agent = HealthChatAgent()
if 'sql_tool' not in st.session_state:
    st.session_state.sql_tool = TextToSQLTool()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0
if 'last_query_result' not in st.session_state:
    st.session_state.last_query_result = None

# 헤더
st.markdown('<div class="main-header">🏥 건강 데이터 AI Agent</div>', unsafe_allow_html=True)
st.markdown("### 자연어로 데이터베이스를 검색하세요")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Health+AI+Agent", use_container_width=True)
    
    st.markdown("### 📊 통계")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 질문", st.session_state.query_count, delta=None)
    with col2:
        st.metric("대화 수", len(st.session_state.messages), delta=None)
    
    st.markdown("---")
    
    # 빠른 검색
    st.markdown("### 🔍 빠른 검색")
    
    quick_searches = {
        "👤 사용자": [
            ("User_1 찾기", "User_1 이라는 이름의 사용자를 찾아줘"),
            ("여성 사용자", "성별이 여성인 사용자 5명을 보여줘"),
            ("최근 가입자", "최근에 가입한 사용자 10명을 알려줘")
        ],
        "🩸 혈당": [
            ("최근 7일", "User_1의 최근 7일간 혈당 데이터를 보여줘"),
            ("측정 횟수", "User_1의 혈당 측정 횟수를 세어줘"),
            ("혈당 분석", "User_1의 혈당을 분석해줘")
        ],
        "📈 통계": [
            ("평균 혈당", "User_1의 평균 혈당 수치를 계산해줘"),
            ("고혈당 횟수", "User_1의 고혈당 발생 횟수를 알려줘"),
            ("혈당 추세", "User_1의 최근 혈당 추세를 분석해줘")
        ]
    }
    
    for category, searches in quick_searches.items():
        with st.expander(category, expanded=False):
            for label, query in searches:
                if st.button(label, key=f"quick_{label}", use_container_width=True):
                    st.session_state.quick_query = query
    
    st.markdown("---")
    
    # 데이터베이스 정보
    st.markdown("### 💾 데이터베이스")
    
    if st.button("📋 스키마 보기", use_container_width=True):
        st.session_state.show_schema = True
    
    st.markdown("---")
    
    # 설정
    st.markdown("### ⚙️ 설정")
    
    show_sql = st.checkbox("SQL 쿼리 표시", value=False)
    show_raw_data = st.checkbox("원본 데이터 표시", value=False)
    
    st.markdown("---")
    
    # 초기화
    if st.button("🔄 대화 초기화", type="secondary", use_container_width=True):
        st.session_state.agent.reset()
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.last_query_result = None
        st.rerun()

# 메인 영역
tab1, tab2, tab3 = st.tabs(["💬 대화", "📊 데이터 분석", "📖 가이드"])

with tab1:
    # 대화 영역
    st.markdown("### 대화 기록")
    
    if len(st.session_state.messages) == 0:
        st.info("👋 안녕하세요! 건강 데이터에 대해 무엇이든 물어보세요.")
        
        # 예제 카드
        st.markdown("#### 💡 시작하기 좋은 질문들")
        cols = st.columns(3)
        
        example_cards = [
            ("👤 사용자 검색", "User_1을 찾아줘", "사용자 정보 조회"),
            ("🩸 혈당 조회", "User_1의 최근 혈당 데이터", "혈당 측정 기록"),
            ("📊 데이터 분석", "User_1의 혈당 분석", "건강 상태 평가")
        ]
        
        for col, (title, query, desc) in zip(cols, example_cards):
            with col:
                if st.button(f"{title}\n\n{desc}", key=f"card_{title}", use_container_width=True):
                    st.session_state.quick_query = query
    
    # 대화 기록 표시
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You</strong> <small style="color: #666;">({message.get('timestamp', datetime.now()).strftime('%H:%M:%S')})</small><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message agent-message">
                <strong>🤖 Agent</strong> <small style="color: #666;">({message.get('timestamp', datetime.now()).strftime('%H:%M:%S')})</small><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # SQL 쿼리 표시 (옵션)
            if show_sql and 'sql' in message:
                with st.expander("🔍 실행된 SQL 쿼리"):
                    st.code(message['sql'], language='sql')
            
            # 원본 데이터 표시 (옵션)
            if show_raw_data and 'data' in message and message['data']:
                with st.expander("📋 원본 데이터"):
                    df = pd.DataFrame(message['data'])
                    st.dataframe(df, use_container_width=True)
    
    # 입력 영역
    st.markdown("---")
    
    # 빠른 질문 처리
    if 'quick_query' in st.session_state:
        default_query = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        default_query = ""
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            query = st.text_input(
                "질문을 입력하세요",
                value=default_query,
                placeholder="예: User_1의 최근 7일간 혈당 데이터를 보여줘",
                label_visibility="collapsed"
            )
        
        with col2:
            submit = st.form_submit_button("전송 📤", type="primary", use_container_width=True)
    
    # 질문 처리
    if submit and query:
        # 사용자 메시지 추가
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now()
        })
        
        # Agent 응답 생성
        with st.spinner("🤔 AI가 생각하고 있습니다..."):
            try:
                response = st.session_state.agent.chat(query)
                
                # Agent 응답 추가
                st.session_state.messages.append({
                    "role": "agent",
                    "content": response,
                    "timestamp": datetime.now()
                })
                
                st.session_state.query_count += 1
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
        
        st.rerun()

with tab2:
    st.markdown("### 📊 데이터 분석 도구")
    
    st.info("💡 왼쪽 사이드바에서 '원본 데이터 표시'를 활성화하면 대화 탭에서 데이터를 볼 수 있습니다.")
    
    # 직접 SQL 실행
    st.markdown("#### 🔧 직접 SQL 쿼리 실행")
    
    with st.expander("SQL 쿼리 실행기", expanded=False):
        sql_query = st.text_area(
            "SQL 쿼리를 입력하세요 (SELECT만 허용)",
            placeholder="SELECT * FROM agent.tb_user_info LIMIT 10",
            height=100
        )
        
        if st.button("실행", type="primary"):
            if sql_query:
                with st.spinner("쿼리 실행 중..."):
                    result = st.session_state.sql_tool.execute_sql(sql_query)
                    
                    if result['success']:
                        st.success(f"✅ {result['row_count']}건의 데이터를 조회했습니다.")
                        
                        if result['data']:
                            df = pd.DataFrame(result['data'])
                            st.dataframe(df, use_container_width=True)
                            
                            # 다운로드 버튼
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                "📥 CSV 다운로드",
                                csv,
                                "query_result.csv",
                                "text/csv",
                                key='download-csv'
                            )
                    else:
                        st.error(f"❌ 오류: {result['error']}")

with tab3:
    st.markdown("### 📖 사용 가이드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 사용 방법
        
        1. **자연어로 질문**
           - 일반 대화처럼 질문하세요
           - 예: "User_1의 혈당 데이터를 보여줘"
        
        2. **AI가 자동 처리**
           - SQL 쿼리 자동 생성
           - 데이터베이스 조회
           - 결과 분석 및 설명
        
        3. **결과 확인**
           - 이해하기 쉬운 설명
           - 필요시 원본 데이터 확인
           - SQL 쿼리 확인 가능
        
        #### 💡 팁
        
        - **구체적으로 질문**: "최근 7일간" 등 기간 명시
        - **연속 대화 가능**: 이전 대화 맥락 유지
        - **빠른 검색**: 사이드바의 버튼 활용
        """)
    
    with col2:
        st.markdown("""
        #### 🩸 혈당 기준
        
        - **정상**: 70-140 mg/dL
        - **저혈당**: 70 미만 ⚠️
        - **고혈당**: 140 초과 ⚠️
        
        #### 📊 데이터베이스 테이블
        
        1. **tb_user_info**: 사용자 정보
           - user_uuid, flnm, eml_addr, gndr_cd 등
        
        2. **tb_glucose_msrmt**: 혈당 측정
           - user_uuid, msrmt_ymd, bs_rslt_cn 등
        
        3. **tb_sensor_log**: 센서 로그
           - user_uuid, sn_nm, msrmt_dt 등
        
        #### 🔒 보안
        
        - SELECT 쿼리만 허용
        - 위험한 명령 자동 차단
        - SQL 인젝션 방지
        """)

# 스키마 모달
if st.session_state.get('show_schema', False):
    with st.expander("📋 데이터베이스 스키마", expanded=True):
        schema = st.session_state.sql_tool.get_schema_description()
        st.code(schema, language='text')
        
        if st.button("닫기"):
            st.session_state.show_schema = False
            st.rerun()

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>
        🏥 건강 데이터 AI Agent v2.0 | Powered by Strands Agents SDK & AWS Bedrock<br>
        Made with ❤️ using Streamlit
    </small>
</div>
""", unsafe_allow_html=True)
