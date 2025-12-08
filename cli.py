#!/usr/bin/env python3
"""
건강 데이터 AI Agent - CLI 인터페이스
"""
import sys
import argparse
from strands_health_agent import HealthChatAgent


def simple_mode():
    """간단한 대화 모드"""
    print("\n🏥 건강 데이터 AI Agent")
    print("=" * 60)
    print("자연어로 질문하세요. 종료: 'quit'\n")
    
    agent = HealthChatAgent()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n종료합니다.")
                break
            
            print("\nAgent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response + "\n")
        
        except KeyboardInterrupt:
            print("\n\n종료합니다.")
            break
        except Exception as e:
            print(f"\n오류: {e}\n")


def interactive_mode():
    """풍부한 대화 모드"""
    print("\n" + "=" * 70)
    print("🏥 건강 데이터 AI 어시스턴트")
    print("=" * 70)
    print("\n자연어로 질문하시면 AI가 데이터베이스를 조회하여 답변합니다.")
    print("\n명령어:")
    print("  - 'quit', 'exit': 프로그램 종료")
    print("  - 'reset': 대화 기록 초기화")
    print("  - 'help': 예제 질문 보기")
    print("=" * 70 + "\n")
    
    agent = HealthChatAgent()
    
    examples = [
        ("👤 사용자 검색", [
            "User_1 이라는 이름의 사용자를 찾아줘",
            "성별이 여성인 사용자 5명을 보여줘",
            "최근에 가입한 사용자 10명을 알려줘"
        ]),
        ("🩸 혈당 데이터", [
            "User_1의 최근 7일간 혈당 데이터를 보여줘",
            "User_1의 혈당 측정 횟수를 세어줘",
            "User_1의 어제 혈당 수치를 알려줘"
        ]),
        ("📊 혈당 분석", [
            "User_1의 혈당을 분석해줘",
            "User_1의 평균 혈당 수치를 계산해줘",
            "User_1의 고혈당 발생 횟수를 알려줘"
        ])
    ]
    
    print("💡 예제 질문을 보려면 'help'를 입력하세요.\n")
    
    while True:
        try:
            user_input = input("💬 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 대화를 종료합니다. 안녕히 가세요!")
                break
            
            if user_input.lower() in ['reset', 'clear']:
                agent.reset()
                print("\n✓ 대화 기록이 초기화되었습니다.\n")
                continue
            
            if user_input.lower() in ['help', 'h', '?']:
                print("\n" + "=" * 70)
                print("📝 예제 질문")
                print("=" * 70 + "\n")
                
                for category, questions in examples:
                    print(f"{category}")
                    for i, q in enumerate(questions, 1):
                        print(f"  {i}. {q}")
                    print()
                continue
            
            print("\n🤖 Agent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 대화를 종료합니다. 안녕히 가세요!")
            break
        
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            print("다시 시도해주세요.\n")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='건강 데이터 AI Agent CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  %(prog)s                # 간단한 모드 (기본)
  %(prog)s --interactive  # 풍부한 모드
  %(prog)s -i             # 풍부한 모드 (축약)
        """
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='풍부한 대화 모드 (예제, 도움말 포함)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.interactive:
            interactive_mode()
        else:
            simple_mode()
    except Exception as e:
        print(f"\n오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
