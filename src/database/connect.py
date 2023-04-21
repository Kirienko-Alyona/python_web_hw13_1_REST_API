import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


file_config = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.RawConfigParser()
#config.read("./src/database/config.ini")
config.read(file_config)
username = config.get("DB", "username")
password = config.get("DB", "password")
db_name = config.get("DB", "db_name")
host = config.get("DB", "host")
port = config.get("DB", "port")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))    #костиль, щоб не падав сервер)
    finally:
        db.close()
