# generate_key.py

import secrets

# Generate a secure random key
secret_key = secrets.token_hex(16)  # 16 bytes gives a 32-character hex string

print("Generated Flask Secret Key:")
print(secret_key)
