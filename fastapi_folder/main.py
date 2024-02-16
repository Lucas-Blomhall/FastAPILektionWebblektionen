from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DOUBLE_PRECISION, DATE, create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import uvicorn

SQLALCHEMY_DATABASE_CONNECTION_STRING = "postgresql://postgres:Vanligt123!@localhost/"

engine = create_engine(SQLALCHEMY_DATABASE_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
