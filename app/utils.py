from passlib.context import CryptContext
import random
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_result(number, count):
    return random.sample(range(number), count)


def select_random_result(number):
    return random.randint(0, number - 1)


def divide_into_two_parts(n):
    part1 = n // 2
    part2 = n - part1

    return part1, part2


def get_one_time_passcode():
    return str(uuid.uuid4())

