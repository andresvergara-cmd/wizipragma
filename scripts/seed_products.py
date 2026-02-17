"""
Seed products for demo
"""

import boto3
from decimal import Decimal

PROFILE = 'pragma-power-user'
REGION = 'us-east-1'
PRODUCTS_TABLE = 'poc-wizi-mex-retailers-dev'
RETAILERS_TABLE = 'centli-retailers'

session = boto3.Session(profile_name=PROFILE, region_name=REGION)
dynamodb = session.resource('dynamodb')

# Demo retailers
retailers = [
    {
        'retailer_id': 'ret-001',
        'name': 'Liverpool',
        'category': 'department_store',
        'benefits_offered': ['MSI_3', 'MSI_6', 'MSI_12', 'CASHBACK_5'],
        'logo_url': 'https://example.com/liverpool-logo.png'
    },
    {
        'retailer_id': 'ret-002',
        'name': 'Best Buy',
        'category': 'electronics',
        'benefits_offered': ['MSI_6', 'MSI_12', 'POINTS_2X'],
        'logo_url': 'https://example.com/bestbuy-logo.png'
    }
]

# Demo products
products = [
    {
        'product_id': 'prod-001',
        'retailer_id': 'ret-002',
        'name': 'Laptop HP 15"',
        'description': 'Laptop HP 15 pulgadas, Intel Core i5, 8GB RAM, 256GB SSD',
        'price': Decimal('12999.00'),
        'currency': 'MXN',
        'category': 'electronics',
        'stock': 10,
        'reserved': 0,
        'image_url': 'https://example.com/laptop-hp.jpg',
        'benefits': ['MSI_6', 'MSI_12', 'POINTS_2X']
    },
    {
        'product_id': 'prod-002',
        'retailer_id': 'ret-002',
        'name': 'iPhone 15 Pro',
        'description': 'iPhone 15 Pro 256GB, Titanio Natural',
        'price': Decimal('24999.00'),
        'currency': 'MXN',
        'category': 'electronics',
        'stock': 5,
        'reserved': 0,
        'image_url': 'https://example.com/iphone-15-pro.jpg',
        'benefits': ['MSI_12', 'POINTS_2X']
    },
    {
        'product_id': 'prod-003',
        'retailer_id': 'ret-001',
        'name': 'Smart TV Samsung 55"',
        'description': 'Smart TV Samsung 55 pulgadas 4K UHD',
        'price': Decimal('8999.00'),
        'currency': 'MXN',
        'category': 'electronics',
        'stock': 15,
        'reserved': 0,
        'image_url': 'https://example.com/tv-samsung.jpg',
        'benefits': ['MSI_3', 'MSI_6', 'CASHBACK_5']
    }
]

def seed_retailers():
    """Seed retailers"""
    table = dynamodb.Table(RETAILERS_TABLE)
    print(f"Seeding {len(retailers)} retailers...")
    
    for retailer in retailers:
        try:
            table.put_item(Item=retailer)
            print(f"✓ Added retailer: {retailer['name']}")
        except Exception as e:
            print(f"✗ Error adding retailer {retailer['name']}: {str(e)}")

def seed_products():
    """Seed products"""
    table = dynamodb.Table(PRODUCTS_TABLE)
    print(f"\nSeeding {len(products)} products...")
    
    for product in products:
        try:
            table.put_item(Item=product)
            print(f"✓ Added product: {product['name']} - ${product['price']}")
        except Exception as e:
            print(f"✗ Error adding product {product['name']}: {str(e)}")

if __name__ == '__main__':
    seed_retailers()
    seed_products()
    print(f"\n✅ Seeding complete!")
