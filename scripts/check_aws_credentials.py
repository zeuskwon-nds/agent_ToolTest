#!/usr/bin/env python3
"""
AWS 자격 증명 및 권한 확인 스크립트
"""
import boto3
import requests
from botocore.exceptions import ClientError, NoCredentialsError
import json


def check_ec2_metadata():
    """EC2 메타데이터 확인"""
    print("=" * 60)
    print("1. EC2 인스턴스 정보 확인")
    print("=" * 60)
    
    try:
        # 인스턴스 ID
        instance_id = requests.get(
            'http://169.254.169.254/latest/meta-data/instance-id',
            timeout=2
        ).text
        print(f"✓ 인스턴스 ID: {instance_id}")
        
        # 리전
        region = requests.get(
            'http://169.254.169.254/latest/meta-data/placement/region',
            timeout=2
        ).text
        print(f"✓ 리전: {region}")
        
        # IAM Role 확인
        iam_role = requests.get(
            'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
            timeout=2
        ).text
        
        if iam_role.strip():
            print(f"✓ IAM Role: {iam_role.strip()}")
            return True, instance_id, region
        else:
            print("✗ IAM Role이 연결되어 있지 않습니다!")
            return False, instance_id, region
            
    except Exception as e:
        print(f"✗ EC2 메타데이터 접근 실패: {e}")
        print("  (EC2 인스턴스가 아니거나 메타데이터 서비스에 접근할 수 없습니다)")
        return False, None, None


def check_aws_credentials():
    """AWS 자격 증명 확인"""
    print("\n" + "=" * 60)
    print("2. AWS 자격 증명 확인")
    print("=" * 60)
    
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("✓ AWS 자격 증명 확인 성공!")
        print(f"  - Account: {identity['Account']}")
        print(f"  - User/Role: {identity['Arn']}")
        print(f"  - UserId: {identity['UserId']}")
        return True
        
    except NoCredentialsError:
        print("✗ AWS 자격 증명을 찾을 수 없습니다!")
        print("  해결 방법:")
        print("  1. EC2 인스턴스에 IAM Role 연결")
        print("  2. aws configure 실행")
        print("  3. 환경 변수 설정 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
        return False
        
    except Exception as e:
        print(f"✗ 자격 증명 확인 실패: {e}")
        return False


def check_bedrock_access():
    """Bedrock 접근 권한 확인"""
    print("\n" + "=" * 60)
    print("3. Amazon Bedrock 접근 권한 확인")
    print("=" * 60)
    
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        
        # 모델 목록 조회 시도
        try:
            response = bedrock.list_foundation_models()
            print("✓ Bedrock 모델 목록 조회 성공!")
            
            # Claude 모델 확인
            claude_models = [
                m for m in response.get('modelSummaries', [])
                if 'claude' in m.get('modelId', '').lower()
            ]
            
            if claude_models:
                print(f"✓ Claude 모델 {len(claude_models)}개 발견")
                for model in claude_models[:3]:
                    print(f"  - {model['modelId']}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDeniedException':
                print("⚠ 모델 목록 조회 권한 없음 (선택사항)")
            else:
                raise
        
        # 실제 모델 호출 테스트
        print("\n테스트: Claude 모델 호출...")
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        from config import MODEL_ID
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[{
                "role": "user",
                "content": [{"text": "Hello"}]
            }]
        )
        
        print("✓ Bedrock 모델 호출 성공!")
        print("✓ 모든 권한이 정상적으로 설정되었습니다!")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        if error_code == 'AccessDeniedException':
            print("✗ Bedrock 접근 권한이 없습니다!")
            print("\n해결 방법:")
            print("1. IAM Role에 다음 권한 추가:")
            print("   - bedrock:InvokeModel")
            print("   - bedrock:InvokeModelWithResponseStream")
            print("\n2. Bedrock 모델 접근 활성화:")
            print("   AWS Console → Bedrock → Model access")
            
        elif error_code == 'ResourceNotFoundException':
            print("✗ 모델을 찾을 수 없습니다!")
            print("  Bedrock 모델 접근 권한을 활성화해야 합니다.")
            print("  AWS Console → Bedrock → Model access")
            
        else:
            print(f"✗ Bedrock 접근 실패: {error_code}")
            print(f"  메시지: {e.response['Error']['Message']}")
        
        return False
        
    except NoCredentialsError:
        print("✗ AWS 자격 증명이 없습니다!")
        return False
        
    except Exception as e:
        print(f"✗ 예상치 못한 오류: {e}")
        return False


def check_database_connection():
    """데이터베이스 연결 확인"""
    print("\n" + "=" * 60)
    print("4. PostgreSQL 데이터베이스 연결 확인")
    print("=" * 60)
    
    try:
        from db_tools import DatabaseTools
        
        db = DatabaseTools()
        users = db.get_user_info()
        
        if users and 'error' not in users[0]:
            print(f"✓ 데이터베이스 연결 성공!")
            print(f"✓ 사용자 데이터 {len(users)}건 조회 완료")
            return True
        else:
            print(f"✗ 데이터베이스 쿼리 실패: {users}")
            return False
            
    except Exception as e:
        print(f"✗ 데이터베이스 연결 실패: {e}")
        return False


def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("AWS 자격 증명 및 권한 확인 도구")
    print("=" * 60 + "\n")
    
    results = {}
    
    # 1. EC2 메타데이터 확인
    has_role, instance_id, region = check_ec2_metadata()
    results['ec2_metadata'] = has_role
    
    # 2. AWS 자격 증명 확인
    results['credentials'] = check_aws_credentials()
    
    # 3. Bedrock 접근 권한 확인
    if results['credentials']:
        results['bedrock'] = check_bedrock_access()
    else:
        results['bedrock'] = False
        print("\n" + "=" * 60)
        print("3. Amazon Bedrock 접근 권한 확인")
        print("=" * 60)
        print("⊘ AWS 자격 증명이 없어 건너뜁니다.")
    
    # 4. 데이터베이스 연결 확인
    results['database'] = check_database_connection()
    
    # 최종 결과
    print("\n" + "=" * 60)
    print("최종 결과")
    print("=" * 60)
    
    print(f"\n{'항목':<30} {'상태':<10}")
    print("-" * 40)
    print(f"{'EC2 IAM Role':<30} {'✓' if results['ec2_metadata'] else '✗':<10}")
    print(f"{'AWS 자격 증명':<30} {'✓' if results['credentials'] else '✗':<10}")
    print(f"{'Bedrock 접근 권한':<30} {'✓' if results['bedrock'] else '✗':<10}")
    print(f"{'데이터베이스 연결':<30} {'✓' if results['database'] else '✗':<10}")
    
    print("\n" + "=" * 60)
    
    if all([results['credentials'], results['bedrock'], results['database']]):
        print("✓ 모든 확인 완료! Agent를 실행할 수 있습니다.")
        print("\n실행 명령어:")
        print("  python simple_health_agent.py")
    elif results['database'] and not results['credentials']:
        print("⚠ AWS 자격 증명이 없습니다.")
        print("\n대안:")
        print("  1. IAM Role 설정: SETUP_IAM_ROLE.md 참조")
        print("  2. CLI 사용: python simple_cli.py")
    else:
        print("✗ 일부 설정이 필요합니다.")
        print("\n다음 문서를 참조하세요:")
        print("  - SETUP_IAM_ROLE.md (IAM Role 설정)")
        print("  - AWS_SETUP.md (AWS 설정)")
    
    print("=" * 60 + "\n")
    
    if instance_id:
        print(f"현재 인스턴스 ID: {instance_id}")
        print(f"리전: {region}")
        print("\nIAM Role 연결이 필요한 경우 관리자에게 전달하세요.")


if __name__ == "__main__":
    main()
