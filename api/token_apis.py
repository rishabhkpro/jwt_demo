from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from dtos.user_dto import (
    UserCreateResponseDto,
    UserCreateDto,
    UserLoginRequestDto,
    UserLoginResponseDto,
    UserDto,
)
from database import get_db
from models.user import User
from datetime import datetime
from security.secrets import get_password_hash, verify_password
from security.jwt_token import get_token, is_token_valid

router = APIRouter(tags=["tokenAPIs"])


@router.post(
    "/create",
    status_code=201,
    response_model=UserCreateResponseDto,
)
async def create_user(
    request_body: UserCreateDto,
    db: Session = Depends(get_db),
):

    user_data = (
        db.query(User)
        .filter(User.user_email == request_body.user_email.lower())
        .first()
    )
    if user_data:
        raise HTTPException(status_code=409, detail="User already exists.")

    # To store hashed password instead of plain text
    hashed_password = get_password_hash(request_body.user_password)

    user_data = User(
        user_name=request_body.user_name.lower(),
        user_email=request_body.user_email.lower(),
        user_password=hashed_password,
        created_at=datetime.now(),
    )

    db.add(user_data)
    db.flush()
    db.commit()

    user_obj = UserDto(
        user_name=user_data.user_name,
        user_email=user_data.user_email,
        user_id=user_data.id,
    )

    return UserCreateResponseDto(
        body=user_obj,
        msg="User created successfully.",
    )


@router.post("/login", status_code=200, response_model=UserLoginResponseDto)
async def login(
    request_body: UserLoginRequestDto,
    db: Session = Depends(get_db),
):
    user_data = (
        db.query(User)
        .filter(User.user_email == request_body.user_email.lower())
        .first()
    )
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found.")

    if not verify_password(request_body.user_password, user_data.user_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # login is successfull, generate a token
    data_for_token = {
        "user_id": user_data.id,
        "user_email": user_data.user_email,
    }
    token = get_token(custom_data=data_for_token)

    user_obj = UserDto(
        user_name=user_data.user_name,
        user_email=user_data.user_email,
        user_id=user_data.id,
    )
    return UserLoginResponseDto(body=user_obj, token=token, msg="Login success.")


@router.get(
    "/validate/{user_id}",
    status_code=200,
)
async def validate(
    user_id: int,
    x_token: str = Header(),
):
    if not is_token_valid(x_token, user_id):
        return "Invalid token"
    return "Valid token"
