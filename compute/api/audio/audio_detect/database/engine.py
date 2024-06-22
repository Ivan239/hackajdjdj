import os

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv("POSTGRES_DB")

from sqlalchemy import create_engine

from .models import Base

import logging
logging.getLogger('uvicorn').info((POSTGRES_HOST, POSTGRES_PORT, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB))

def get_engine():
    return create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

def get_session():
    from sqlalchemy.orm import sessionmaker
    return sessionmaker(bind=get_engine())()

def create_tables():
    Base.metadata.create_all(get_engine())
    
    
create_tables()
