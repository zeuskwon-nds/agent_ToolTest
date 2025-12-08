# GitHub 푸시 가이드

## 🚀 바로 푸시하기

```bash
./git_push.sh
```

이 스크립트가 자동으로:
1. Git 초기화
2. 파일 추가
3. 커밋
4. GitHub에 푸시

## 📦 저장소 정보

- **URL**: https://github.com/zeuskwon-nds/agent_ToolTest
- **브랜치**: main

## 👥 동료가 사용하는 방법

### 1. 클론

```bash
git clone https://github.com/zeuskwon-nds/agent_ToolTest.git
cd agent_ToolTest
```

### 2. 설치

```bash
pip install -r requirements.txt
```

### 3. 설정

```bash
cp config.example.py config.py
# config.py 편집 (데이터베이스 및 AWS 정보)
```

### 4. 실행

```bash
# 테스트
python test_all.py

# 웹 UI
./run_streamlit.sh

# CLI
python cli.py
```

## 📋 동료에게 전달할 정보

1. **저장소 URL**
   ```
   https://github.com/zeuskwon-nds/agent_ToolTest
   ```

2. **데이터베이스 정보** (별도로 안전하게 공유)
   - Host
   - Port
   - Database
   - Username
   - Password

3. **AWS 설정**
   - AWS CLI 설정 필요
   - Bedrock 모델 활성화 필요

## 📚 문서

- [README.md](README.md) - 프로젝트 소개
- [SETUP.md](SETUP.md) - 설치 가이드
- [HOW_IT_WORKS.md](HOW_IT_WORKS.md) - 동작 원리

## ✅ 완료!

이제 동료들이 프로젝트를 사용할 수 있습니다! 🎉
