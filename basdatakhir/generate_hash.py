# Helper script to generate password hash for new users
from werkzeug.security import generate_password_hash

def generate_hash(password):
    """Generate password hash"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

if __name__ == '__main__':
    # Generate hash for default password
    default_password = 'admin123'
    hash_value = generate_hash(default_password)
    
    print("="*60)
    print("Password Hash Generator")
    print("="*60)
    print(f"\nPassword: {default_password}")
    print(f"Hash: {hash_value}")
    print("\nCopy this hash to use in SQL INSERT statements")
    print("="*60)
