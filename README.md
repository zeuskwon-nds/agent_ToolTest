# 🏥 건강 데이터 AI Agent

자연어로 데이터베이스를 검색하는 AI Agent입니다. AWS Bedrock의 Claude 모델과 Strands Agents SDK를 사용하여 실시간으로 SQL을 생성하고 실행합니다.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Strands Agents](https://img.shields.io/badge/Strands-Agents-green.svg)](https://strandsagents.com)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 주요 기능

- 🗣️ **자연어 질의**: "User_1의 최근 혈당 데이터를 보여줘" → AI가 자동으로 SQL 생성
- 🤖 **실시간 SQL 생성**: 저장된 쿼리가 아닌 AI가 매번 새로운 SQL 생성
- 🌐 **웹 UI**: Streamlit 기반의 깔끔한 인터페이스
- 💻 **CLI 지원**: 터미널에서도 사용 가능
- 🔒 **보안**: SELECT만 허용, SQL 인젝션 방지

## 🚀 빠른 시작

### 1. 클론 및 설치

```bash
git clone https://github.com/zeuskwon-nds/agent_ToolTest.git
cd agent_ToolTest
pip install -r requirements.txt
```

### 2. 설정

```bash
cp config.example.py config.py
# config.py 편집하여 데이터베이스 및 AWS 정보 입력
```

### 3. 테스트

```bash
python scripts/test_all.py
```

### 4. 실행

```bash
# 웹 UI (추천)
./scripts/run_streamlit.sh

# CLI
python src/cli.py
```

## 💬 사용 예제

```
You: User_1의 최근 7일간 혈당 데이터를 보여줘

Agent: [AI가 자동으로 SQL 생성 및 실행]

날짜      | 혈당 수치 | 상태
----------|-----------|--------
2025-12-02 | 126 mg/dL | 정상
2025-12-01 | 102 mg/dL | 정상
2025-11-30 | 166 mg/dL | 고혈당
...

평균 혈당: 119.6 mg/dL
전반적으로 양호한 상태입니다.
```

## 📁 프로젝트 구조

```
agent_ToolTest/
├── 📄 README.md                    # 프로젝트 소개 (이 파일)
├── 📄 LICENSE                      # MIT 라이선스
├── 📄 requirements.txt             # Python 패키지 목록
├── 📄 config.example.py            # 설정 파일 예제
├── 📄 config.py                    # 실제 설정 (생성 필요)
├── 📄 .gitignore                   # Git 제외 파일
├── 📄 git_push.sh                  # GitHub 푸시 스크립트
│
├── 📂 src/                         # 소스 코드
│   ├── app.py                      # Streamlit 웹 UI
│   ├── cli.py                      # CLI 인터페이스
│   ├── strands_health_agent.py     # Strands Agent 핵심 로직
│   └── text_to_sql_tool.py         # Text-to-SQL 도구
│
├── 📂 scripts/                     # 실행 스크립트
│   ├── run_streamlit.sh            # Streamlit 실행
│   ├── test_all.py                 # 통합 테스트
│   └── check_aws_credentials.py    # AWS 자격 증명 확인
│
└── 📂 docs/                        # 문서
    ├── SETUP.md                    # 설치 및 설정 가이드
    ├── HOW_IT_WORKS.md             # 동작 원리 설명
    └── PUSH_GUIDE.md               # GitHub 푸시 가이드
```

## 🔧 기술 스택

- **AI Framework**: Strands Agents SDK
- **LLM**: AWS Bedrock (Claude 3.5 Sonnet)
- **Database**: PostgreSQL
- **Web UI**: Streamlit
- **Language**: Python 3.9+

## 📋 사전 요구사항

- Python 3.9+
- AWS 계정 (Bedrock 접근 권한)
- PostgreSQL 데이터베이스

## 📖 문서

### 📘 시작하기
- **[SETUP.md](docs/SETUP.md)** - 설치 및 설정 가이드
  - 패키지 설치 방법
  - AWS Bedrock 설정
  - 데이터베이스 설정
  - 문제 해결

### 🔍 이해하기
- **[HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md)** - 동작 원리 설명
  - Text-to-SQL이란?
  - AI가 SQL을 생성하는 방법
  - 전체 아키텍처
  - 보안 메커니즘

### 🚀 공유하기
- **[PUSH_GUIDE.md](docs/PUSH_GUIDE.md)** - GitHub 푸시 가이드
  - Git 초기화 방법
  - 동료와 공유하는 방법
  - 동료가 사용하는 방법

## 🎯 주요 명령어

```bash
# 테스트
python scripts/test_all.py

# 웹 UI 실행
./scripts/run_streamlit.sh

# CLI 실행 (간단)
python src/cli.py

# CLI 실행 (풍부한 모드)
python src/cli.py -i

# AWS 자격 증명 확인
python scripts/check_aws_credentials.py
```

## 🔒 보안

- SELECT 쿼리만 허용
- DROP, DELETE, UPDATE 등 위험한 명령 차단
- SQL 인젝션 방지
- config.py는 Git에서 제외 (.gitignore)

## 🤝 기여

기여를 환영합니다! Pull Request를 보내주세요.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

This project is proprietary software owned by NDS Corp.
Unauthorized use, distribution, or modification is strictly prohibited.
- 자세한 내용은 [LICENSE](LICENSE) 파일 참조

## 🙏 감사

- [Strands Agents](https://strandsagents.com) - AI Agent 프레임워크
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - LLM 서비스
- [Streamlit](https://streamlit.io) - 웹 UI 프레임워크

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!

## 📞 문의

프로젝트에 대한 질문이나 제안이 있으시면 GitHub Issues를 통해 연락주세요.

