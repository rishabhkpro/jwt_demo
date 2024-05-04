from typing import List, Literal, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from pydantic import BaseModel, Field
from humps import camelize


def to_camel(string):
    return camelize(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserDto(CamelModel):
    user_name: str
    user_email: str
    user_id: int


class UserCreateDto(CamelModel):
    user_name: str
    user_email: str
    user_password: str


class UserCreateResponseDto(CamelModel):
    body: UserDto
    msg: str


class UserLoginRequestDto(CamelModel):
    user_email: str
    user_password: str


class UserLoginResponseDto(CamelModel):
    body: UserDto
    token: str
    msg: str
