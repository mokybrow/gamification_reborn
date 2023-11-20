from pydantic import BaseModel


class Msg(BaseModel):
    msg: str

class VerifyToken(BaseModel):
    access_token: str
    token_type: str
