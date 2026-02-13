import random
import string


def generate_id(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))  # noqa: S311
