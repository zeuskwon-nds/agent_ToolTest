# Database Configuration
DB_CONFIG = {
    'host': 'your-database-host.rds.amazonaws.com',
    'port': 5432,
    'database': 'postgres',
    'user': 'your-username',
    'password': 'your-password',
    'options': '-c search_path=agent,public'
}

# AWS Configuration
AWS_REGION = 'us-east-1'

# Model Configuration
# Cross-Region Inference Profile 사용 (권장)
MODEL_ID = 'us.anthropic.claude-3-5-sonnet-20240620-v1:0'

# 또는 다른 모델 사용 가능:
# MODEL_ID = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
# MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
