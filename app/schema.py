from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
