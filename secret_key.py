import secrets

# Generate a secure secret key
jwt_secret_key = secrets.token_hex(32)

print(f"JWT_SECRET_KEY={jwt_secret_key}")
