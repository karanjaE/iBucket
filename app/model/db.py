import os

from sqlalchemy import create_engine

engine = create_engine(os.environ["DB_URL"])

def init_db():
    pass
