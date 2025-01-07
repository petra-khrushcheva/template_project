import bcrypt


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.

    :param password: Пароль в виде строки.
    :return: Хэшированный пароль в виде строки.
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля и хэша.

    :param plain_password: Пароль в виде строки.
    :param hashed_password: Хэш пароля в виде строки.
    :return: True, если пароль совпадает, иначе False.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except ValueError:
        return False
