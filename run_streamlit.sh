#!/bin/bash
# Streamlit 웹 UI 실행 스크립트

echo "=================================="
echo "건강 데이터 AI Agent - Streamlit UI"
echo "=================================="
echo ""
echo "🚀 웹 UI를 실행합니다..."
echo ""
echo "브라우저에서 접속: http://localhost:8501"
echo ""

# 포트 설정 (기본: 8501)
PORT=${1:-8501}

streamlit run app.py --server.port $PORT --server.address 0.0.0.0
