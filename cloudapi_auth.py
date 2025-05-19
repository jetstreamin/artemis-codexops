from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers, models, schemas
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
SECRET = "SUPERSECRET"
Base: DeclarativeMeta = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base, models.BaseUser):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

user_db = SQLAlchemyUserDatabase(User, SessionLocal())
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
fastapi_users = FastAPIUsers(user_db, [jwt_authentication], User, schemas.BaseUserCreate, schemas.BaseUserUpdate, schemas.BaseUserDB)
app = FastAPI()
app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt")
app.include_router(fastapi_users.get_register_router(), prefix="/auth")

@app.get("/whoami")
async def whoami(user: User = Depends(fastapi_users.get_current_user)):
    return user.email
