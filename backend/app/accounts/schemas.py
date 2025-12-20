from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Annotated
from zxcvbn import zxcvbn


class LoginSchema(BaseModel):
    email: EmailStr
    # It is recommended as per new docs to use Annotated for field constraints
    password: Annotated[str, Field(min_length=8, max_length=30)]

class RegisterSchema(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr
    # It is recommended as per new docs to use Annotated for field constraints
    password: Annotated[str, Field(min_length=8, max_length=30)]
    
    @field_validator('password')
    @classmethod
    def password_validator(cls, value):
        password_strength = zxcvbn(value)
        if password_strength['score'] < 3:
            raise ValueError('Password is too weak')
        return value

class VerifyEmailRequest(BaseModel):
    token: str