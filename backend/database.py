import logging
import os
import time
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

encoded_password = urllib.parse.quote(os.getenv('DB_PASSWORD', ''))
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{encoded_password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info['start_time'] = time.time()
    query = statement
    for param, value in parameters.items():
        query = query.replace(f"%({param})s", str(value))
    logger.debug(f"Executing SQL Query: {query}")


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - conn.info['start_time']
    logger.debug(f"Query executed in {total_time:.4f} seconds")
