import datetime

from pydantic import BaseModel


class UserData(BaseModel):
    name: str
    bio: str | None = None
    birthdate: datetime.date | None = None
