from datetime import datetime, timedelta

# import jwt
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = "%&GH143243*(&(hkjhk))"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1hour


def get_token(custom_data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = custom_data.copy()

    if expires_delta:
        expiry = datetime.utcnow() + expires_delta
    else:
        expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expiry})

    token = jwt.encode(to_encode, SECRET_KEY)
    return token


def is_token_valid(
    token: str,
    user_id: str = None,
):
    try:

        # verifying whether token is belongs to current user
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        if user_id != payload.get("user_id", None):
            print("Invalid token.")
            return False

        # Convert the expiration time to a datetime object
        expiration_datetime = datetime.utcfromtimestamp(payload["exp"])
        # Get the current time
        current_time = datetime.utcnow()

        # Check if the token has expired
        if current_time > expiration_datetime:
            print("Token expired")
            return False
        return True
    except JWTError as jwt_err:
        print(f"JWT error:{str(jwt_err)}")
        return False
    except Exception as e:
        print(f"Exception in token validation:{str(e)}")
        return False
