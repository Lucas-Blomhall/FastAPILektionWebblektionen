from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DOUBLE_PRECISION, DATE, create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import uvicorn

SQLALCHEMY_DATABASE_CONNECTION_STRING = "postgresql://postgres:Vanligt123!@localhost/"

engine = create_engine(SQLALCHEMY_DATABASE_CONNECTION_STRING)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Each field is a column in your DB
class HisotricalTableGoogl(base):
    __tablename__ = "googl_historical"
    date = Column(DATE, primary_key=True)
    open = Column(DOUBLE_PRECISION)
    high = Column(DOUBLE_PRECISION)
    low = Column(DOUBLE_PRECISION)
    close = Column(DOUBLE_PRECISION)
    Colume = Column(DOUBLE_PRECISION)
    dividends = Column(DOUBLE_PRECISION)
    stocksplits = Column(DOUBLE_PRECISION)


# Each field is a column in your DB
class HisotricalTableMsft(base):
    __tablename__ = "msft_historical"
    date = Column(DATE, primary_key=True)
    open = Column(DOUBLE_PRECISION)
    high = Column(DOUBLE_PRECISION)
    low = Column(DOUBLE_PRECISION)
    close = Column(DOUBLE_PRECISION)
    Colume = Column(DOUBLE_PRECISION)
    dividends = Column(DOUBLE_PRECISION)
    stocksplits = Column(DOUBLE_PRECISION)


def get_recent(db, table):
    most_recent_record = db.query(table).order_by(table.date.desc()).first()
    return most_recent_record


def get_oldest(db, talbe):
    oldest_record = db.query(table).order_by(table.date).first()
    return oldest_record


class TicketReqest(BaseModel):
    ticker: str
    query: str


class TicketResponse(BaseModel):
    ticker: str
    close_value: float


@app.post("/ticker/record")
async def get_ticker_record(ticker_request: TicketReqest, db=Depends(get_db)):
    valid_tickers = {
        'googl': HisotricalTableGoogl,
        'msft': HisotricalTableMsft,
    }

    valid_queries = ['recent', 'oldest']

    if ticker_request.ticker not in valid_tickers:
        raise HTTPException(status_code=400)

    if ticker_request.query not in valid_queries:
        raise HTTPException(status_code=400)

    table = valid_tickers[ticker_request.ticker]

    if ticker_request.query == 'recent':
        record = get_recent(db, table)
