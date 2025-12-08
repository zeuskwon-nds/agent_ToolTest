# 🔍 Text-to-SQL Agent 동작 원리

## 핵심 질문에 대한 답변

### Q: SQL을 미리 저장해두고 사용하나요?

**A: 아니요! AI가 실시간으로 SQL을 생성합니다.** ✨

이 프로젝트는 **동적 Text-to-SQL** 방식으로, 사용자의 자연어 질문을 받아서 그때그때 새로운 SQL 쿼리를 생성합니다.

---

## 🎯 동작 방식 (단계별)

### 1단계: 사용자 질문 입력

```
사용자: "User_1의 최근 7일간 혈당 데이터를 보여줘"
```

### 2단계: AI Agent가 스키마 확인

Agent는 먼저 `get_database_schema()` 도구를 호출하여 데이터베이스 구조를 파악합니다.

```python
@tool
def get_database_schema() -> str:
    """데이터베이스 스키마 정보를 반환"""
    return sql_tool.get_schema_description()
```

**반환되는 정보:**
- 테이블 이름 및 구조
- 컬럼 이름 및 타입
- 관계 (JOIN 방법)
- 예제 쿼리

### 3단계: AI가 SQL 쿼리 생성

Claude 3.5 Sonnet 모델이 스키마 정보를 바탕으로 **새로운 SQL 쿼리를 생성**합니다.

```sql
-- AI가 생성한 쿼리 예시
SELECT 
    user_uuid,
    msrmt_ymd,
    bs_rslt_cn,
    CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER) as glucose_value
FROM agent.tb_glucose_msrmt
WHERE user_uuid = 'b1c7ac6c33769a2f0c8bf0fbb08ecfb8'
  AND msrmt_ymd >= '20251201'
ORDER BY msrmt_ymd DESC
LIMIT 7
```

### 4단계: SQL 실행

Agent가 `execute_sql_query()` 도구를 호출하여 생성한 SQL을 실행합니다.

```python
@tool
def execute_sql_query(sql_query: str) -> str:
    """SQL 쿼리를 실행하여 데이터베이스를 조회"""
    result = sql_tool.execute_sql(sql_query)
    return json.dumps(result)
```

### 5단계: 결과 분석 및 응답

AI가 쿼리 결과를 분석하고 사용자가 이해하기 쉽게 설명합니다.

```
Agent: "User_1의 최근 7일간 혈당 데이터를 분석했습니다.

날짜      | 혈당 수치 | 상태
----------|-----------|--------
2025-12-02 | 126 mg/dL | 정상
2025-12-01 | 102 mg/dL | 정상
2025-11-30 | 166 mg/dL | 고혈당
...

평균 혈당: 119.6 mg/dL
고혈당 발생: 1회 (11월 30일)
전반적으로 양호한 상태입니다."
```

---

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                         사용자                               │
│              "User_1의 혈당 데이터를 보여줘"                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Strands Agent                              │
│              (Claude 3.5 Sonnet)                             │
│                                                              │
│  1. 자연어 이해                                               │
│  2. 도구 선택 및 호출                                         │
│  3. 결과 분석 및 응답 생성                                    │
└────────────┬──────────────────────────┬─────────────────────┘
             │                          │
             ▼                          ▼
┌────────────────────────┐  ┌──────────────────────────────┐
│  get_database_schema() │  │  execute_sql_query(sql)      │
│                        │  │                              │
│  - 테이블 구조 반환     │  │  - SQL 실행                  │
│  - 컬럼 정보 반환       │  │  - 결과 반환                 │
│  - 예제 쿼리 제공       │  │  - 보안 검증                 │
└────────────┬───────────┘  └──────────┬───────────────────┘
             │                         │
             ▼                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   TextToSQLTool                              │
│                                                              │
│  - 스키마 정보 관리                                           │
│  - SQL 실행 (psycopg2)                                       │
│  - 보안 검증 (SELECT만 허용)                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                        │
│                                                              │
│  - agent.tb_user_info                                        │
│  - agent.tb_glucose_msrmt                                    │
│  - agent.tb_sensor_log                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 핵심 특징

### 1. 동적 SQL 생성 (Dynamic Text-to-SQL)

**저장된 쿼리 방식 (X)**
```python
# 이런 방식이 아닙니다!
queries = {
    "사용자 검색": "SELECT * FROM users WHERE name = ?",
    "혈당 조회": "SELECT * FROM glucose WHERE user_id = ?"
}
```

**AI 생성 방식 (O)**
```python
# 이렇게 작동합니다!
def chat(user_message):
    # 1. AI가 질문 이해
    # 2. 스키마 확인
    # 3. 새로운 SQL 생성
    # 4. SQL 실행
    # 5. 결과 분석
    return ai_response
```

### 2. 유연한 질의 처리

사용자가 어떤 방식으로 질문해도 AI가 이해하고 적절한 SQL을 생성합니다:

```
✅ "User_1을 찾아줘"
✅ "User_1 이라는 이름의 사용자 정보를 알려줘"
✅ "User_1의 데이터를 보여줘"
✅ "User_1 검색"

→ 모두 같은 의미로 이해하고 적절한 SQL 생성
```

### 3. 복잡한 쿼리도 생성 가능

```
사용자: "User_1의 최근 30일간 평균 혈당을 계산하고, 
        고혈당이 발생한 날짜를 알려줘"

AI 생성 SQL:
WITH user_glucose AS (
    SELECT 
        msrmt_ymd,
        CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER) as glucose_value
    FROM agent.tb_glucose_msrmt
    WHERE user_uuid = 'xxx'
      AND msrmt_ymd >= '20251108'
)
SELECT 
    AVG(glucose_value) as avg_glucose,
    COUNT(CASE WHEN glucose_value > 140 THEN 1 END) as high_glucose_days,
    STRING_AGG(
        CASE WHEN glucose_value > 140 THEN msrmt_ymd END, 
        ', '
    ) as high_glucose_dates
FROM user_glucose
```

### 4. 에러 자동 수정

SQL 실행이 실패하면 AI가 에러를 읽고 쿼리를 수정합니다:

```
1차 시도: SELECT * FROM users WHERE name = 'User_1'
→ 실패: "테이블 'users'가 존재하지 않습니다"

2차 시도: SELECT * FROM agent.tb_user_info WHERE flnm = 'User_1'
→ 실패: "결과가 없습니다"

3차 시도: SELECT * FROM agent.tb_user_info WHERE flnm LIKE '%User_1%'
→ 성공! ✅
```

---

## 🔒 보안 메커니즘

### 1. SQL 인젝션 방지

```python
def execute_sql(self, sql_query: str):
    sql_lower = sql_query.lower().strip()
    
    # SELECT 또는 WITH만 허용
    if not (sql_lower.startswith('select') or sql_lower.startswith('with')):
        return {"error": "SELECT 쿼리만 허용됩니다"}
    
    # 위험한 키워드 차단
    dangerous = ['drop', 'delete', 'update', 'insert', 'alter', 'create']
    for keyword in dangerous:
        if keyword in sql_lower:
            return {"error": f"'{keyword}' 명령은 허용되지 않습니다"}
```

### 2. 결과 제한

```python
# 최대 20개 행만 반환 (성능 보호)
"data": result.get("data", [])[:20]
```

---

## 🎓 예제: 전체 흐름

### 입력
```
사용자: "User_1의 혈당이 140을 넘은 날을 찾아줘"
```

### Agent 내부 동작

**Step 1: 스키마 확인**
```
Tool: get_database_schema()
→ 테이블 구조, 컬럼 정보 확인
```

**Step 2: SQL 생성**
```sql
SELECT 
    msrmt_ymd,
    bs_rslt_cn,
    CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER) as glucose_value
FROM agent.tb_glucose_msrmt
WHERE user_uuid = (
    SELECT user_uuid 
    FROM agent.tb_user_info 
    WHERE flnm = 'User_1'
)
AND CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER) > 140
ORDER BY msrmt_ymd DESC
```

**Step 3: SQL 실행**
```
Tool: execute_sql_query(sql)
→ 데이터베이스 조회
```

**Step 4: 결과 분석**
```json
{
  "success": true,
  "row_count": 3,
  "data": [
    {"msrmt_ymd": "20251130", "glucose_value": 166},
    {"msrmt_ymd": "20251125", "glucose_value": 152},
    {"msrmt_ymd": "20251120", "glucose_value": 145}
  ]
}
```

**Step 5: 응답 생성**
```
Agent: "User_1의 혈당이 140을 넘은 날은 총 3일입니다:

1. 2025년 11월 30일: 166 mg/dL (고혈당)
2. 2025년 11월 25일: 152 mg/dL (고혈당)
3. 2025년 11월 20일: 145 mg/dL (경미한 고혈당)

최근 고혈당 발생 빈도가 증가하고 있으니 주의가 필요합니다."
```

---

## 🆚 비교: 저장된 쿼리 vs AI 생성

### 저장된 쿼리 방식 (전통적)

**장점:**
- 빠른 실행
- 예측 가능한 동작

**단점:**
- ❌ 미리 정의된 질문만 가능
- ❌ 새로운 질문마다 코드 수정 필요
- ❌ 유연성 부족
- ❌ 복잡한 쿼리 조합 어려움

### AI 생성 방식 (이 프로젝트)

**장점:**
- ✅ 자유로운 자연어 질문
- ✅ 코드 수정 없이 새로운 질문 처리
- ✅ 복잡한 쿼리 자동 생성
- ✅ 에러 자동 수정
- ✅ 맥락 이해 (연속 대화)

**단점:**
- 응답 시간 (25-30초)
- LLM 비용

---

## 🎯 결론

이 프로젝트는 **완전한 동적 Text-to-SQL 시스템**입니다:

1. ✅ SQL을 미리 저장하지 않음
2. ✅ AI가 실시간으로 SQL 생성
3. ✅ 자연어 질문을 자유롭게 처리
4. ✅ 복잡한 분석 쿼리도 자동 생성
5. ✅ 에러 발생 시 자동 수정

**핵심 기술:**
- Strands Agents SDK (Agent 프레임워크)
- AWS Bedrock Claude 3.5 Sonnet (LLM)
- PostgreSQL (데이터베이스)
- psycopg2 (DB 연결)

---

## 📚 더 알아보기

- [strands_health_agent.py](strands_health_agent.py) - Agent 구현
- [text_to_sql_tool.py](text_to_sql_tool.py) - SQL 실행 도구
- [CHAT_GUIDE.md](CHAT_GUIDE.md) - 사용 예제
- [Strands Agents 문서](https://strandsagents.com)
