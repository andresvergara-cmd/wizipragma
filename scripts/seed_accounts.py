"""
Seed user accounts for demo
"""

import boto3
from decimal import Decimal

# AWS configuration
PROFILE = '777937796305_Ps-HackatonAgentic-Mexico'
REGION = 'us-east-1'
TABLE_NAME = 'centli-accounts'

# Initialize DynamoDB
session = boto3.Session(profile_name=PROFILE, region_name=REGION)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Demo accounts
accounts = [
    {
        'user_id': 'user-demo-001',
        'account_id': 'acc-checking-001',
        'account_type': 'checking',
        'balance': Decimal('50000.00'),
        'currency': 'MXN',
        'status': 'active',
        'version': 0,
        'created_at': '2026-02-17T00:00:00Z',
        'updated_at': '2026-02-17T00:00:00Z'
    },
    {
        'user_id': 'user-demo-001',
        'account_id': 'acc-savings-001',
        'account_type': 'savings',
        'balance': Decimal('100000.00'),
        'currency': 'MXN',
        'status': 'active',
        'version': 0,
        'created_at': '2026-02-17T00:00:00Z',
        'updated_at': '2026-02-17T00:00:00Z'
    },
    {
        'user_id': 'user-demo-001',
        'account_id': 'acc-credit-001',
        'account_type': 'credit',
        'balance': Decimal('25000.00'),
        'currency': 'MXN',
        'status': 'active',
        'version': 0,
        'created_at': '2026-02-17T00:00:00Z',
        'updated_at': '2026-02-17T00:00:00Z'
    }
]

def seed_accounts():
    """Seed accounts to DynamoDB"""
    print(f"Seeding {len(accounts)} accounts to {TABLE_NAME}...")
    
    for account in accounts:
        try:
            table.put_item(Item=account)
            print(f"✓ Added account: {account['account_id']} ({account['account_type']}) - Balance: ${account['balance']}")
        except Exception as e:
            print(f"✗ Error adding account {account['account_id']}: {str(e)}")
    
    print(f"\n✅ Seeding complete! Added {len(accounts)} accounts.")

if __name__ == '__main__':
    seed_accounts()
