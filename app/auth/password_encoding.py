from bcrypt import hashpw, checkpw, gensalt


def hash_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return hashpw(plain_text_password, gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return checkpw(plain_text_password, hashed_password)
