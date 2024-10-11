from pydantic import BaseModel


class SUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class SUserInDB(SUser):
    hashed_password: str


class SCreateUserInDB(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    disabled: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None