"""
Run all seed scripts
"""

import subprocess
import sys

scripts = [
    'scripts/seed_accounts.py',
    'scripts/seed_products.py',
    'scripts/seed_beneficiaries.py'
]

def run_seed_script(script):
    """Run a seed script"""
    print(f"\n{'='*60}")
    print(f"Running: {script}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}:")
        print(e.stderr)
        return False

def main():
    """Run all seed scripts"""
    print("CENTLI - Seeding all demo data")
    print("="*60)
    
    success_count = 0
    for script in scripts:
        if run_seed_script(script):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Seeding complete! {success_count}/{len(scripts)} scripts succeeded.")
    print('='*60)

if __name__ == '__main__':
    main()
