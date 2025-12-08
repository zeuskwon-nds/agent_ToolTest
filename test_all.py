#!/usr/bin/env python3
"""
통합 테스트 스크립트 - 모든 기능 테스트
"""
import sys
import time
from datetime import datetime


def print_section(title):
    """섹션 헤더 출력"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_aws_credentials():
    """AWS 자격 증명 테스트"""
    print_section("1. AWS 자격 증명 확인")
    
    try:
        import boto3
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS 자격 증명 확인 성공")
        print(f"   Account: {identity['Account']}")
        print(f"   User/Role: {identity['Arn'].split('/')[-1]}")
        return True
    except Exception as e:
        print(f"❌ AWS 자격 증명 실패: {e}")
        return False


def test_database():
    """데이터베이스 연결 테스트"""
    print_section("2. 데이터베이스 연결 확인")
    
    try:
        from text_to_sql_tool import TextToSQLTool
        
        tool = TextToSQLTool()
        result = tool.execute_sql("SELECT COUNT(*) as count FROM agent.tb_user_info LIMIT 1")
        
        if result['success']:
            count = result['data'][0]['count']
            print(f"✅ 데이터베이스 연결 성공")
            print(f"   사용자 수: {count}명")
            return True
        else:
            print(f"❌ 쿼리 실패: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False


def test_text_to_sql():
    """Text-to-SQL 도구 테스트"""
    print_section("3. Text-to-SQL 도구 테스트")
    
    try:
        from text_to_sql_tool import TextToSQLTool
        
        tool = TextToSQLTool()
        
        # 간단한 쿼리 테스트
        result = tool.execute_sql(
            "SELECT user_uuid, flnm, eml_addr FROM agent.tb_user_info WHERE flnm LIKE '%User_1%' LIMIT 3"
        )
        
        if result['success']:
            print(f"✅ SQL 실행 성공")
            print(f"   조회 결과: {result['row_count']}건")
            if result['data']:
                print(f"   첫 번째 사용자: {result['data'][0]['flnm']}")
            return True
        else:
            print(f"❌ SQL 실행 실패: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ Text-to-SQL 테스트 실패: {e}")
        return False


def test_strands_agent():
    """Strands Agent 테스트"""
    print_section("4. Strands Agent 테스트")
    
    try:
        from strands_health_agent import HealthChatAgent
        
        print("   Agent 초기화 중...")
        agent = HealthChatAgent()
        print("   ✅ Agent 초기화 성공")
        
        # 간단한 질문 테스트
        print("\n   질문: User_1을 찾아줘")
        start_time = time.time()
        response = agent.chat("User_1 이라는 이름의 사용자를 찾아줘")
        elapsed = time.time() - start_time
        
        print(f"\n   ✅ Agent 응답 성공 (소요 시간: {elapsed:.1f}초)")
        print(f"   응답 길이: {len(response)}자")
        
        # 응답에 User_1이 포함되어 있는지 확인
        if "User_1" in response:
            print("   ✅ 응답 내용 검증 성공")
            return True
        else:
            print("   ⚠️  응답 내용 검증 실패")
            return False
            
    except Exception as e:
        print(f"❌ Strands Agent 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 테스트 실행"""
    print("\n" + "=" * 70)
    print("  건강 데이터 AI Agent - 통합 테스트")
    print("=" * 70)
    print(f"  시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "AWS 자격 증명": test_aws_credentials(),
        "데이터베이스": test_database(),
        "Text-to-SQL": test_text_to_sql(),
        "Strands Agent": test_strands_agent()
    }
    
    # 결과 요약
    print_section("테스트 결과 요약")
    
    for test_name, result in results.items():
        status = "✅ 성공" if result else "❌ 실패"
        print(f"  {test_name:<20} {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n  총 {total_count}개 테스트 중 {success_count}개 성공")
    
    if success_count == total_count:
        print("\n  🎉 모든 테스트 통과! Streamlit UI를 실행하세요:")
        print("     ./run_streamlit.sh")
        return 0
    else:
        print("\n  ⚠️  일부 테스트 실패. 설정을 확인하세요.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
