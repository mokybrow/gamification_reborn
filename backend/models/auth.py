from pydantic import UUID4, BaseModel


class BaseUser(BaseModel):
    email: str
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: UUID4

    class Config:
        from_attributes = True
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResetUser(BaseModel):
    id: UUID4
    email: str
    username: str
    hashed_password: str
