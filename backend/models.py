from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    birthday: str