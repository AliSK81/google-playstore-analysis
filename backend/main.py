import logging
import os
import time
import urllib.parse
from datetime import date, datetime
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_serializer
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, TIMESTAMP, ForeignKey, func, event, \
    Index
from sqlalchemy.engine import Engine
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


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info['start_time'] = time.time()
    query = statement
    for param, value in parameters.items():
        query = query.replace(f"%({param})s", str(value))
    logger.debug(f"Executing SQL Query: {query}")


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - conn.info['start_time']
    logger.debug(f"Query executed in {total_time:.4f} seconds")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)


class Developer(Base):
    __tablename__ = "developers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True)


class App(Base):
    __tablename__ = "apps"
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String(255), unique=True, index=True)
    app_name = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    developer_id = Column(Integer, ForeignKey("developers.id"), nullable=True)
    rating = Column(Float)
    rating_count = Column(Integer)
    installs = Column(Integer)
    min_installs = Column(Integer)
    max_installs = Column(Integer)
    free = Column(Boolean)
    price = Column(Float)
    currency = Column(String(50))
    size = Column(Float)
    min_android = Column(String(50))
    released = Column(Date)
    last_updated = Column(Date)
    content_rating = Column(String(50))
    ad_supported = Column(Boolean)
    in_app_purchases = Column(Boolean)
    editors_choice = Column(Boolean)
    scraped_time = Column(TIMESTAMP)
    __table_args__ = (Index('idx_category_free', 'category_id', 'free'),)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FilterResponse(BaseModel):
    categories: List[str]
    content_ratings: List[str]
    min_rating: float
    max_rating: float
    min_price: float
    max_price: float
    min_installs: int
    max_installs: int


class AppResponse(BaseModel):
    id: int
    app_id: str
    app_name: str
    category_id: Optional[int]
    developer_id: Optional[int]
    rating: Optional[float]
    rating_count: Optional[int]
    installs: Optional[int]
    min_installs: Optional[int]
    max_installs: Optional[int]
    free: Optional[bool]
    price: Optional[float]
    currency: Optional[str]
    size: Optional[float]
    min_android: Optional[str]
    released: Optional[date]
    last_updated: Optional[date]
    content_rating: Optional[str]
    ad_supported: Optional[bool]
    in_app_purchases: Optional[bool]
    editors_choice: Optional[bool]
    scraped_time: Optional[datetime]

    class Config:
        from_attributes = True

    @field_serializer("released", "last_updated")
    def serialize_date(self, value: Optional[date]) -> Optional[str]:
        return value.strftime('%Y-%m-%d') if value else None

    @field_serializer("scraped_time")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime('%Y-%m-%d %H:%M:%S') if value else None


app = FastAPI()


@app.get("/filters", response_model=FilterResponse)
def get_filters(db: SessionLocal = Depends(get_db)):
    categories = db.query(Category.name).all()
    categories = [category[0] for category in categories]
    content_ratings = db.query(App.content_rating).distinct().all()
    content_ratings = [content_rating[0] for content_rating in content_ratings]
    min_rating = db.query(func.min(App.rating)).scalar() or 0
    max_rating = db.query(func.max(App.rating)).scalar() or 5.0
    min_price = db.query(func.min(App.price)).scalar() or 0.0
    max_price = db.query(func.max(App.price)).scalar() or 100.0
    min_installs = db.query(func.min(App.installs)).scalar() or 0
    max_installs = db.query(func.max(App.installs)).scalar() or 10000000
    return FilterResponse(
        categories=categories,
        content_ratings=content_ratings,
        min_rating=min_rating,
        max_rating=max_rating,
        min_price=min_price,
        max_price=max_price,
        min_installs=min_installs,
        max_installs=max_installs
    )


@app.get("/apps", response_model=List[AppResponse])
def get_filtered_apps(
        category: Optional[str] = Query(None),
        min_rating: Optional[float] = Query(None),
        max_rating: Optional[float] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        min_installs: Optional[int] = Query(None),
        max_installs: Optional[int] = Query(None),
        content_rating: Optional[str] = Query(None),
        free: Optional[bool] = Query(None),
        ad_supported: Optional[bool] = Query(None),
        in_app_purchases: Optional[bool] = Query(None),
        editors_choice: Optional[bool] = Query(None),
        limit: Optional[int] = Query(100, ge=1),
        db: SessionLocal = Depends(get_db)
):
    query = db.query(App)
    if category:
        category_id = db.query(Category.id).filter(Category.name == category).first()
        if category_id:
            query = query.filter(App.category_id == category_id[0])
    if min_rating is not None:
        query = query.filter(App.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(App.rating <= max_rating)
    if min_price is not None:
        query = query.filter(App.price >= min_price)
    if max_price is not None:
        query = query.filter(App.price <= max_price)
    if min_installs is not None:
        query = query.filter(App.installs >= min_installs)
    if max_installs is not None:
        query = query.filter(App.installs <= max_installs)
    if content_rating:
        query = query.filter(App.content_rating == content_rating)
    if free is not None:
        query = query.filter(App.free == free)
    if ad_supported is not None:
        query = query.filter(App.ad_supported == ad_supported)
    if in_app_purchases is not None:
        query = query.filter(App.in_app_purchases == in_app_purchases)
    if editors_choice is not None:
        query = query.filter(App.editors_choice == editors_choice)
    apps = query.limit(limit).all()
    return apps


@app.get("/apps/release_trend", response_model=List[dict])
def get_app_release_trend(category_name: str | None = None, db: SessionLocal = Depends(get_db)):
    if category_name:
        category_id = db.query(Category.id).filter(Category.name == category_name).first()
        if category_id:
            result = db.query(func.extract('year', App.released).label('year'), func.count().label('count')) \
                .filter(App.category_id == category_id[0]) \
                .group_by(func.extract('year', App.released)) \
                .order_by('year').all()
            return [{"year": int(year), "count": count} for year, count in result]
        return JSONResponse(content={"message": "Category not found."}, status_code=404)

    result = db.query(func.extract('year', App.released).label('year'), func.count().label('count')) \
        .group_by(func.extract('year', App.released)) \
        .order_by('year').all()
    return [{"year": int(year), "count": count} for year, count in result]


@app.get("/apps/average_rating/", response_model=dict)
def get_average_rating(category_name: str | None = None, db: SessionLocal = Depends(get_db)):
    if category_name:
        category_id = db.query(Category.id).filter(Category.name == category_name).first()
        if category_id:
            avg_rating = db.query(func.avg(App.rating)).filter(App.category_id == category_id[0]).scalar()
            return {"category": category_name, "average_rating": avg_rating}
        return JSONResponse(content={"message": "Category not found."}, status_code=404)

    avg_rating = db.query(func.avg(App.rating)).scalar()
    return {"category": "All", "average_rating": avg_rating}
