from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Imagine these categories are given to you as follows in JSON format

districts = {
    [
        {
            "title": "some title 1",
            "description": "description"
        },
        {"title": "some title 2",
         "description": "description"
         }
    ]
}

provinces = {
    [
        {
            "title": "some title 1",
            "description": "description"
        },
        {"title": "some title 2",
         "description": "description"
         }
    ]
}

attractions = {
    [
        {
            "title": "some title 1",
            "description": "description"
        },
        {"title": "some title 2",
         "description": "description"
         }
    ]
}


hotels = {
    [
        {
            "title": "some title 1",
            "description": "description"
        },
        {"title": "some title 2",
         "description": "description"
         }
    ]
}

activities = {
    [
        {
            "title": "some title 1",
            "description": "description"
        },
        {"title": "some title 2",
         "description": "description"
         }
    ]
}


def solution(district, province, attraction, hotel, activity):
    # Your solution
    pass
