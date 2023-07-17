import bcrypt

def hash_password(password: str) -> str:
    # Generate a salt to be used for hashing
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')