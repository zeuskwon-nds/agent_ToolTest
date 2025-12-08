# 설치 및 설정 가이드

## 📋 사전 요구사항

- Python 3.9+
- AWS 계정 (Bedrock 접근 권한)
- PostgreSQL 데이터베이스

## 🚀 설치

### 1. 저장소 클론

```bash
git clone https://github.com/zeuskwon-nds/agent_ToolTest.git
cd agent_ToolTest
```

### 2. 가상 환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 설정 파일 생성

```bash
cp config.example.py config.py
```

`config.py` 편집:

```python
DB_CONFIG = {
    'host': 'your-db-host.rds.amazonaws.com',
    'port': 5432,
    'database': 'postgres',
    'user': 'your-username',
    'password': 'your-password',
    'options': '-c search_path=agent,public'
}

AWS_REGION = 'us-east-1'
MODEL_ID = 'us.anthropic.claude-3-5-sonnet-20240620-v1:0'
```

### 5. AWS 자격 증명 설정

#### 방법 1: AWS CLI

```bash
aws configure
```

#### 방법 2: 환경 변수

```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

#### 방법 3: IAM Role (EC2)

EC2에서 실행 시 IAM Role 연결

### 6. 테스트

```bash
python test_all.py
```

## 🔧 AWS Bedrock 설정

### 1. 모델 활성화

1. AWS Console → Amazon Bedrock
2. Model access → Manage model access
3. Claude 3.5 Sonnet 체크
4. Save changes

### 2. IAM 권한

필요한 권한:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/*"
        }
    ]
}
```

## 💾 데이터베이스 스키마

```sql
-- 사용자 정보
CREATE TABLE agent.tb_user_info (
    user_uuid VARCHAR(32) PRIMARY KEY,
    flnm VARCHAR(300),
    eml_addr VARCHAR(320),
    gndr_cd CHAR(1),
    -- ... 기타 컬럼
);

-- 혈당 측정 기록
CREATE TABLE agent.tb_glucose_msrmt (
    user_uuid VARCHAR(32),
    sn_nm VARCHAR(100),
    msrmt_ymd CHAR(8),
    bs_rslt_cn TEXT,
    -- ... 기타 컬럼
    PRIMARY KEY (user_uuid, sn_nm, msrmt_ymd)
);

-- 센서 로그
CREATE TABLE agent.tb_sensor_log (
    user_uuid VARCHAR(32),
    sn_nm VARCHAR(100),
    msrmt_dt TIMESTAMP WITH TIME ZONE,
    -- ... 기타 컬럼
    PRIMARY KEY (user_uuid, sn_nm, msrmt_dt)
);
```

## 🔍 문제 해결

### AWS 자격 증명 오류

```bash
python check_aws_credentials.py
```

### 데이터베이스 연결 오류

1. 호스트 주소 확인
2. 포트 번호 확인 (기본: 5432)
3. 사용자명/비밀번호 확인
4. 보안 그룹 설정 확인

### Bedrock 모델 접근 오류

1. Bedrock 모델 활성화 확인
2. IAM 권한 확인
3. 리전 확인

## 🎉 완료!

설치가 완료되면:

```bash
# 웹 UI 실행
./run_streamlit.sh

# CLI 실행
python cli.py
```

브라우저에서 `http://localhost:8501` 접속
