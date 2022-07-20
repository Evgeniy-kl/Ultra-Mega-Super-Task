from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
