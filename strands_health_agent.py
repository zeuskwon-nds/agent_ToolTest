#!/usr/bin/env python3
"""
Strands Agents SDK를 사용한 건강 데이터 AI Agent
Text-to-SQL 기능으로 자연어를 SQL로 변환하여 데이터베이스 조회
"""
import warnings
warnings.filterwarnings(action="ignore", message=r"datetime.datetime.utcnow")

from strands import Agent, tool
from text_to_sql_tool import TextToSQLTool
from config import MODEL_ID


# Text-to-SQL 도구 초기화
sql_tool = TextToSQLTool()


@tool
def get_database_schema() -> str:
    """
    데이터베이스 스키마 정보를 반환합니다.
    SQL 쿼리를 작성하기 전에 반드시 이 함수를 먼저 호출하세요.
    
    Returns:
        데이터베이스 스키마 정보 (테이블 구조, 컬럼 정보, 예제 쿼리)
    """
    return sql_tool.get_schema_description()


@tool
def execute_sql_query(sql_query: str) -> str:
    """
    SQL 쿼리를 실행하여 데이터베이스를 조회합니다.
    SELECT 쿼리 또는 WITH 구문을 사용할 수 있습니다.
    
    Args:
        sql_query: 실행할 SQL SELECT 쿼리 (WITH 구문 사용 가능)
    
    Returns:
        쿼리 실행 결과 (JSON 형식)
    """
    import json
    
    result = sql_tool.execute_sql(sql_query)
    
    # 결과를 더 명확하게 반환
    if result["success"]:
        return json.dumps({
            "success": True,
            "row_count": result.get("row_count", 0),
            "data": result.get("data", [])[:20],  # 최대 20개만 반환
            "message": f"쿼리 실행 성공! {result.get('row_count', 0)}건의 데이터를 조회했습니다."
        }, ensure_ascii=False, default=str, indent=2)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error"),
            "message": "쿼리 실행 실패. 에러 메시지를 확인하고 다른 방법을 시도하세요."
        }, ensure_ascii=False, indent=2)


# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 건강 데이터 분석 전문 AI 어시스턴트입니다.
사용자의 자연어 질문을 이해하고, 적절한 SQL 쿼리를 생성하여 데이터베이스에서 정보를 조회합니다.
한국어로 자연스럽게 대화하며, 데이터를 이해하기 쉽게 설명합니다.

**중요한 작업 순서:**
1. 먼저 get_database_schema()를 호출하여 데이터베이스 스키마를 확인합니다
2. 스키마 정보를 바탕으로 적절한 SQL 쿼리를 생성합니다
3. execute_sql_query()를 호출하여 쿼리를 실행합니다
4. 쿼리 실행 결과를 확인합니다:
   - success가 true이면 데이터를 분석하고 설명합니다
   - success가 false이면 error 메시지를 확인하고 쿼리를 수정합니다
5. 에러가 발생하면 다른 접근 방식을 시도합니다

**SQL 작성 규칙:**
- 모든 테이블은 agent 스키마에 있습니다 (예: agent.tb_user_info)
- SELECT 쿼리 또는 WITH 구문 사용 가능
- 날짜 형식은 YYYYMMDD (문자열)입니다
- 사용자 검색 시 flnm 컬럼에 LIKE '%검색어%' 사용 (대소문자 구분: User_1)
- 결과는 LIMIT을 사용하여 제한 (기본 10개)
- JOIN 시 user_uuid 사용

**중요: 데이터 형식**
- bs_rslt_cn 컬럼은 TEXT 타입으로 "Glucose Level: 126" 형식입니다
- 혈당 값을 추출하려면: CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER)
- JSON 함수를 사용하지 마세요 (데이터가 JSON이 아닙니다)

**데이터 분석:**
- 혈당 정상 범위: 70-140 mg/dL
- 저혈당: 70 미만
- 고혈당: 140 초과
- 추세 분석 시 최근 데이터의 패턴 설명
- 예측 요청 시 과거 데이터 기반으로 합리적인 추정 제공

**에러 처리:**
- 쿼리 실행 실패 시 에러 메시지를 읽고 다른 방법을 시도하세요
- 같은 쿼리를 반복하지 마세요
- 간단한 쿼리부터 시작하세요
"""


class HealthChatAgent:
    """Strands Agents SDK를 사용한 건강 데이터 대화형 Agent"""
    
    def __init__(self):
        """Agent 초기화"""
        self.agent = Agent(
            model=MODEL_ID,
            tools=[get_database_schema, execute_sql_query],
            system_prompt=SYSTEM_PROMPT
        )
    
    def chat(self, user_message: str) -> str:
        """
        사용자와 대화
        
        Args:
            user_message: 사용자 메시지
        
        Returns:
            Agent 응답
        """
        try:
            response = self.agent(user_message)
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"오류 발생: {str(e)}"
    
    def reset(self):
        """대화 기록 초기화"""
        # Strands Agent는 자동으로 대화 기록을 관리하므로
        # 새로운 Agent 인스턴스를 생성하여 초기화
        self.agent = Agent(
            model=MODEL_ID,
            tools=[get_database_schema, execute_sql_query],
            system_prompt=SYSTEM_PROMPT
        )


def main():
    """대화형 인터페이스"""
    print("=" * 70)
    print("건강 데이터 AI 어시스턴트 (Strands Agents SDK)")
    print("=" * 70)
    print("자연어로 질문하세요. Agent가 자동으로 SQL을 생성하여 조회합니다.")
    print("종료하려면 'quit' 또는 'exit'를 입력하세요.\n")
    
    agent = HealthChatAgent()
    
    # 예제 질문들
    example_questions = [
        "User_1 이라는 이름의 사용자를 찾아줘",
        "User_1의 최근 7일간 혈당 데이터를 보여줘",
        "User_1의 혈당을 분석해서 이상이 있는지 확인해줘",
        "성별이 여성인 사용자 5명을 보여줘",
        "User_1의 혈당 측정 횟수를 세어줘"
    ]
    
    print("예제 질문:")
    for i, q in enumerate(example_questions, 1):
        print(f"  {i}. {q}")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("\n대화를 종료합니다.")
                break
            
            if user_input.lower() == 'reset':
                agent.reset()
                print("\n대화 기록이 초기화되었습니다.\n")
                continue
            
            if not user_input:
                continue
            
            print("\n🤖 Agent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print("\n\n대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
