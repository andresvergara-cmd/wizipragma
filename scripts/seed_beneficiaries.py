"""
Seed beneficiaries for demo
"""

import boto3

PROFILE = 'pragma-power-user'
REGION = 'us-east-1'
TABLE_NAME = 'centli-beneficiaries'

session = boto3.Session(profile_name=PROFILE, region_name=REGION)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Demo beneficiaries
beneficiaries = [
    {
        'user_id': 'user-demo-001',
        'beneficiary_id': 'ben-001',
        'name': 'Juan López García',
        'alias': 'mi hermano',
        'alias_lower': 'mi hermano',
        'account_id': 'acc-external-001',
        'relationship': 'brother',
        'created_at': '2026-02-17T00:00:00Z'
    },
    {
        'user_id': 'user-demo-001',
        'beneficiary_id': 'ben-002',
        'name': 'María Rodríguez',
        'alias': 'mi hermana',
        'alias_lower': 'mi hermana',
        'account_id': 'acc-external-002',
        'relationship': 'sister',
        'created_at': '2026-02-17T00:00:00Z'
    },
    {
        'user_id': 'user-demo-001',
        'beneficiary_id': 'ben-003',
        'name': 'Carlos Martínez',
        'alias': 'mi amigo',
        'alias_lower': 'mi amigo',
        'account_id': 'acc-external-003',
        'relationship': 'friend',
        'created_at': '2026-02-17T00:00:00Z'
    }
]

def seed_beneficiaries():
    """Seed beneficiaries to DynamoDB"""
    print(f"Seeding {len(beneficiaries)} beneficiaries to {TABLE_NAME}...")
    
    for beneficiary in beneficiaries:
        try:
            table.put_item(Item=beneficiary)
            print(f"✓ Added beneficiary: {beneficiary['name']} (alias: {beneficiary['alias']})")
        except Exception as e:
            print(f"✗ Error adding beneficiary {beneficiary['name']}: {str(e)}")
    
    print(f"\n✅ Seeding complete! Added {len(beneficiaries)} beneficiaries.")

if __name__ == '__main__':
    seed_beneficiaries()
