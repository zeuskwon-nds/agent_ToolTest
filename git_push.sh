#!/bin/bash
# Git 초기화 및 GitHub 푸시 스크립트

echo "=================================="
echo "GitHub에 푸시 준비"
echo "=================================="
echo ""

# Git 초기화 (이미 되어있으면 스킵)
if [ ! -d .git ]; then
    echo "1. Git 초기화..."
    git init
else
    echo "1. Git이 이미 초기화되어 있습니다."
fi

echo ""
echo "2. 파일 추가..."
git add .

echo ""
echo "3. 커밋..."
git commit -m "Initial commit: Health Data AI Agent

- Strands Agents SDK 기반 Text-to-SQL Agent
- 자연어로 데이터베이스 검색
- Streamlit 웹 UI
- CLI 인터페이스
- 완전한 문서화"

echo ""
echo "4. 기본 브랜치 설정..."
git branch -M main

echo ""
echo "5. GitHub 저장소 연결..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/zeuskwon-nds/agent_ToolTest.git

echo ""
echo "6. GitHub에 푸시..."
git push -u origin main --force

echo ""
echo "=================================="
echo "✅ 완료!"
echo "=================================="
echo ""
echo "저장소 URL:"
echo "https://github.com/zeuskwon-nds/agent_ToolTest"
echo ""
echo "동료에게 공유하세요!"
echo ""
