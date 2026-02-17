#!/usr/bin/env python3
"""
Quick seed for test user
"""

import boto3
import json
from decimal import Decimal

PROFILE = 'pragma-power-user'
REGION = 'us-east-1'
TABLE_NAME = 'poc-wizi-mex-user-profile-dev'

# Initialize DynamoDB
session = boto3.Session(profile_name=PROFILE, region_name=REGION)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Test user matching the format from users_mx.json
test_user = {
    "userId": "test-user-001",
    "firstName": "Carlos",
    "lastName": "Rodríguez",
    "email": "carlos.rodriguez@test.com",
    "personalInfo": {
        "birthDate": "1985-03-15",
        "location": "Ciudad de México, México",
        "occupation": "Ingeniero de Software",
        "maritalStatus": "married",
        "children": 2
    },
    "financialInfo": {
        "incomeAnnual": Decimal('1322595.9'),
        "creditScore": 750,
        "hasMortgage": True
    },
    "creditLine": {
        "isApproved": True,
        "limit": Decimal('400000.0'),
        "available": Decimal('400000.0')
    },
    "habits": {
        "preferredPaymentMethod": "credit_card",
        "savingsRate": Decimal('0.15'),
        "investmentStyle": "moderate",
        "shoppingHabits": ["online", "tecnología", "supermercados"],
        "spendingFrequency": "weekly"
    },
    "goals": {
        "shortTerm": ["pagar_tarjeta_credito", "crear_fondo_emergencia"],
        "mediumTerm": ["ahorrar_vacaciones", "mejoras_hogar"],
        "longTerm": ["ahorros_jubilacion", "educacion_hijos"],
        "targetSavings": Decimal('915000.0')
    },
    "preferences": {
        "language": "Spanish",
        "timezone": "COT",
        "communicationChannel": "email",
        "notificationFrequency": "weekly"
    },
    "importantDates": {
        "anniversary": "2018-06-20",
        "childrenBirthdays": ["2019-08-12", "2021-11-03"],
        "creditCardDueDate": "25th",
        "mortgageDueDate": "15th"
    },
    "joinDate": "2026-02-17T00:00:00.000Z"
}

def seed_test_user():
    """Seed test user to DynamoDB"""
    print(f"Seeding test user to {TABLE_NAME}...")
    
    try:
        table.put_item(Item=test_user)
        print(f"✅ Test user added: {test_user['userId']}")
        print(f"   Name: {test_user['firstName']} {test_user['lastName']}")
        print(f"   Email: {test_user['email']}")
        return True
    except Exception as e:
        print(f"❌ Error adding test user: {e}")
        return False

if __name__ == '__main__':
    seed_test_user()
