from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from crud import get_user_by_email, create_user
from engine import SessionLocal, engine, Base
from schema import Settings
from schema import User
from services import UserManage

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/registration/", response_model=User)
def create_users(user: User, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.post("/users/login/")
def login(user: User, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    if UserManage.check_user(user, get_user_by_email(db, user.email)):
        access_token = Authorize.create_access_token(subject=user.email, expires_time=timedelta(days=1))
        refresh_token = Authorize.create_refresh_token(subject=user.email, expires_time=timedelta(days=2))
        return {"access_token": access_token, 'refresh_token': refresh_token}
    return JSONResponse(status_code=401, content="Bad email or password")


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.post('/refresh/')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@app.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"app": current_user}
