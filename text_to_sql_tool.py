"""
Text-to-SQL Tool using Strands Agents
자연어를 SQL로 변환하여 데이터베이스를 조회하는 도구
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any
from config import DB_CONFIG


class TextToSQLTool:
    """자연어를 SQL로 변환하여 실행하는 도구"""
    
    def __init__(self):
        self.config = DB_CONFIG
        self.schema_info = self._get_schema_info()
    
    def _get_schema_info(self) -> str:
        """데이터베이스 스키마 정보를 가져옴"""
        return """
        데이터베이스 스키마 정보:
        
        1. agent.tb_user_info (사용자 정보)
           - user_uuid (VARCHAR(32), PK): 사용자 UUID
           - eml_addr (VARCHAR(320)): 이메일 주소
           - flnm (VARCHAR(300)): 이름
           - gndr_cd (CHAR(1)): 성별 코드 (M/F)
           - brdt (VARCHAR(300)): 생년월일 (YYYYMMDD)
           - ntn_cd (CHAR(2)): 국가 코드
           - ntn_no (VARCHAR(10)): 국가 번호
           - mbl_telno (VARCHAR(300)): 휴대폰 번호
           - user_type_cd (CHAR(5)): 사용자 유형 코드
           - join_dt (TIMESTAMP): 가입일시
           - use_yn (CHAR(1)): 사용 여부 (Y/N)
           - reg_dt (TIMESTAMP): 등록일시
        
        2. agent.tb_glucose_msrmt (혈당 측정 기록)
           - user_uuid (VARCHAR(32), PK): 사용자 UUID
           - sn_nm (VARCHAR(100), PK): 시리얼 번호
           - msrmt_ymd (CHAR(8), PK): 측정일자 (YYYYMMDD)
           - bs_rslt_cn (TEXT): 혈당 측정 결과
           - rd_cn (TEXT): 원시 데이터
           - reg_dt (TIMESTAMP): 등록일시
        
        3. agent.tb_sensor_log (센서 로그)
           - user_uuid (VARCHAR(32), PK): 사용자 UUID
           - sn_nm (VARCHAR(100), PK): 시리얼 번호
           - msrmt_dt (TIMESTAMP WITH TIME ZONE, PK): 측정일시
           - analog_glucose (TEXT): 아날로그 혈당 값
           - rcd_indx_no (TEXT): 레코드 인덱스 번호
           - reg_dt (TIMESTAMP): 등록일시
        
        주의사항:
        - 모든 테이블은 agent 스키마에 있습니다
        - 날짜 형식: YYYYMMDD (예: 20251205)
        - 사용자 검색 시 LIKE 사용 가능
        - JOIN 시 user_uuid 사용
        
        중요: bs_rslt_cn 데이터 형식
        - bs_rslt_cn은 TEXT 타입으로 "Glucose Level: 126" 형식입니다
        - 혈당 값 추출 방법:
          CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER)
        
        예제 쿼리:
        
        1. 사용자 검색:
        SELECT * FROM agent.tb_user_info WHERE flnm LIKE '%User_1%' LIMIT 10
        
        2. 혈당 데이터 조회 (값 추출):
        SELECT 
            user_uuid,
            msrmt_ymd,
            bs_rslt_cn,
            CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER) as glucose_value
        FROM agent.tb_glucose_msrmt
        WHERE user_uuid = 'xxx'
        ORDER BY msrmt_ymd DESC
        LIMIT 10
        
        3. 혈당 분석 (WITH 구문):
        WITH user_glucose AS (
            SELECT 
                msrmt_ymd,
                CAST(SUBSTRING(bs_rslt_cn FROM 'Glucose Level: ([0-9]+)') AS INTEGER) as glucose_value
            FROM agent.tb_glucose_msrmt
            WHERE user_uuid = 'xxx'
        )
        SELECT 
            msrmt_ymd,
            glucose_value,
            CASE 
                WHEN glucose_value < 70 THEN '저혈당'
                WHEN glucose_value > 140 THEN '고혈당'
                ELSE '정상'
            END as status
        FROM user_glucose
        ORDER BY msrmt_ymd DESC
        """
    
    def get_connection(self):
        """데이터베이스 연결 생성"""
        return psycopg2.connect(**self.config)
    
    def execute_sql(self, sql_query: str) -> Dict[str, Any]:
        """
        SQL 쿼리를 실행하고 결과를 반환
        
        Args:
            sql_query: 실행할 SQL 쿼리
            
        Returns:
            실행 결과 딕셔너리 (success, data, error, row_count)
        """
        try:
            # SQL 인젝션 방지를 위한 기본 검증
            sql_lower = sql_query.lower().strip()
            
            # WITH 구문 허용 (CTE - Common Table Expression)
            if sql_lower.startswith('with'):
                # WITH 구문 내에 SELECT가 있는지 확인
                if 'select' not in sql_lower:
                    return {
                        "success": False,
                        "error": "WITH 구문에는 SELECT가 포함되어야 합니다.",
                        "data": [],
                        "row_count": 0
                    }
            elif not sql_lower.startswith('select'):
                # SELECT 또는 WITH로 시작하지 않으면 차단
                return {
                    "success": False,
                    "error": "보안상 SELECT 쿼리 또는 WITH 구문만 허용됩니다.",
                    "data": [],
                    "row_count": 0
                }
            
            # 위험한 키워드 차단 (단, WITH는 허용)
            dangerous_keywords = ['drop', 'delete', 'update', 'insert', 'alter', 'create', 'truncate']
            for keyword in dangerous_keywords:
                if f' {keyword} ' in f' {sql_lower} ' or sql_lower.endswith(keyword):
                    return {
                        "success": False,
                        "error": f"보안상 '{keyword}' 명령은 허용되지 않습니다.",
                        "data": [],
                        "row_count": 0
                    }
            
            # 쿼리 실행
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql_query)
                    results = cur.fetchall()
                    data = [dict(row) for row in results]
                    
                    return {
                        "success": True,
                        "data": data,
                        "row_count": len(data),
                        "error": None
                    }
        
        except psycopg2.Error as e:
            return {
                "success": False,
                "error": f"데이터베이스 오류: {str(e)}",
                "data": [],
                "row_count": 0
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"예상치 못한 오류: {str(e)}",
                "data": [],
                "row_count": 0
            }
    
    def get_schema_description(self) -> str:
        """스키마 정보 반환"""
        return self.schema_info


# Strands Agent에서 사용할 도구 함수
def search_database(natural_language_query: str, sql_query: str) -> str:
    """
    자연어 질의를 SQL로 변환하여 데이터베이스를 검색합니다.
    
    Args:
        natural_language_query: 사용자의 자연어 질문
        sql_query: 생성된 SQL 쿼리
    
    Returns:
        JSON 형식의 검색 결과
    """
    import json
    
    tool = TextToSQLTool()
    result = tool.execute_sql(sql_query)
    
    # 결과를 보기 좋게 포맷팅
    if result["success"]:
        return json.dumps({
            "status": "success",
            "query": sql_query,
            "row_count": result["row_count"],
            "data": result["data"]
        }, ensure_ascii=False, default=str, indent=2)
    else:
        return json.dumps({
            "status": "error",
            "query": sql_query,
            "error": result["error"]
        }, ensure_ascii=False, indent=2)


def get_database_schema() -> str:
    """
    데이터베이스 스키마 정보를 반환합니다.
    SQL 쿼리를 작성하기 전에 이 함수를 호출하여 스키마 정보를 확인하세요.
    
    Returns:
        데이터베이스 스키마 정보
    """
    tool = TextToSQLTool()
    return tool.get_schema_description()
