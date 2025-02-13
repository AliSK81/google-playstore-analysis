from typing import List, Optional

from fastapi import Query, Depends, FastAPI
from sqlalchemy import func

from api_models import FilterResponse, AppResponse
from database import SessionLocal, get_db
from db_models import Category, App

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
        category_id = get_category_id(db, category) if category else None
        if category_id:
            query = query.filter(App.category_id == category_id)
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
def get_app_release_trend(category_name: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    category_id = get_category_id(db, category_name) if category_name else None

    query = db.query(func.extract('year', App.released).label('year'), func.count().label('count')) \
        .group_by(func.extract('year', App.released)) \
        .order_by('year')

    if category_id:
        query = query.filter(App.category_id == category_id)

    result = query.all()
    return [{"year": int(year), "count": count} for year, count in result]


@app.get("/apps/average_rating/", response_model=dict)
def get_average_rating(category_name: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    category_id = get_category_id(db, category_name) if category_name else None
    query = db.query(func.avg(App.rating))

    if category_id:
        query = query.filter(App.category_id == category_id)

    avg_rating = query.scalar()
    return {"category": category_name or "All", "average_rating": avg_rating}


def get_category_id(db: SessionLocal, category_name: str) -> Optional[int]:
    category_id = db.query(Category.id).filter(Category.name == category_name).first()
    return category_id[0] if category_id else None
