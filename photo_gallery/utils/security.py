from bcrypt import hashpw, gensalt, checkpw


def hash_password(pw):
    if pw:
        hashed_pw = hashpw(pw.encode('utf-8'), gensalt())
        return hashed_pw.decode('utf-8')
    return None


def check_password(pw, hashed_pw):
    if pw and hashed_pw:
        expected = hashed_pw.encode('utf-8')
        return checkpw(pw.encode('utf-8'), expected)
    return False
