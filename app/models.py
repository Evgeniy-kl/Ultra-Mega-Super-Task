from sqlalchemy import Column, String

from engine import Base


class UserTable(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True, index=True)
    password = Column(String)
