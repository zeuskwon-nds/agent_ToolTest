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

```
You: User_1의 최근 7일간 혈당 데이터를 분석해서 미래 혈당을 예측해줘

Agent: [AI가 자동으로 SQL 생성 및 실행]
네, User_1의 최근 7일간의 혈당 데이터를 분석하고 미래 혈당을 예측해보도록 하겠습니다. 먼저 데이터베이스 스키마를 확인한 후 적절한 SQL 쿼리를 작성하여 데이터를 조회하겠습니다.
Tool #1: get_database_schema
데이터베이스 스키마 정보를 확인했습니다. 이제 User_1의 최근 7일간의 혈당 데이터를 조회하기 위한 SQL 쿼리를 작성하고 실행하겠습니다.
Tool #2: execute_sql_query
User_1의 최근 7일간의 혈당 데이터를 분석한 결과, 다음과 같은 정보를 얻었습니다:

1. 데이터 기간: 최근 7일 중 2025년 12월 2일 하루의 데이터만 있습니다.
2. 혈당 수치: 126 mg/dL
3. 상태: 정상 (70-140 mg/dL 범위 내)

분석 결과:
1. 데이터의 제한: 7일간의 데이터를 요청했으나 단 하루의 데이터만 있어 전체적인 추세를 파악하기 어렵습니다.
2. 현재 상태: 측정된 혈당 수치는 정상 범위 내에 있지만, 정상 범위의 상한선에 가깝습니다.

미래 혈당 예측:
단일 데이터 포인트로는 정확한 예측을 하기 어렵지만, 현재 상황을 바탕으로 다음과 같은 가능성을 고려할 수 있습니다:

1. 현상 유지: 현재 혈당 수준이 정상 범위 내에 있으므로, 생활 습관을 유지한다면 비슷한 수준을 유지할 가능성이 있습니다.

2. 상승 가능성: 현재 수치가 정상 범위의 상한선에 가깝기 때문에, 식습관이나 운동량에 변화가 없다면 향후 고혈당으로 진입할 위험이 있습니다.

3. 변동성: 단일 측정치만으로는 일중 변동이나 식후 변화 등을 파악할 수 없으므로, 실제로는 더 큰 변동성이 있을 수 있습니다.

권장사항:
1. 더 빈번한 측정: 혈당의 추세를 정확히 파악하기 위해 하루에 여러 번, 특히 식전과 식후에 측정을 권장합니다.
2. 식습관 관리: 현재 수치가 정상 상한선에 가깝기 때문에, 탄수화물 섭취를 조절하고 균형 잡힌 식단을 유지하는 것이 중요합니다.
3. 규칙적인 운동: 적절한 운동은 혈당 조절에 도움이 될 수 있습니다.
4. 지속적인 모니터링: 앞으로의 변화를 주시하며 정기적으로 혈당을 체크하는 것이 중요합니다.

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


## 📝 라이선스

This project is proprietary software owned by NDS Corp.
Unauthorized use, distribution, or modification is strictly prohibited.
- 자세한 내용은 [LICENSE](LICENSE) 파일 참조

