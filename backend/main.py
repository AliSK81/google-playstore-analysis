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
    filters = {
        "category": category,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "min_price": min_price,
        "max_price": max_price,
        "min_installs": min_installs,
        "max_installs": max_installs,
        "content_rating": content_rating,
        "free": free,
        "ad_supported": ad_supported,
        "in_app_purchases": in_app_purchases,
        "editors_choice": editors_choice,
    }

    query = db.query(App)
    query = apply_filters_to_query(query, filters, db)

    apps = query.limit(limit).all()
    return apps


@app.get("/apps/rating_distribution", response_model=List[dict])
def get_rating_distribution(
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
        db: SessionLocal = Depends(get_db)
):
    filters = {
        "category": category,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "min_price": min_price,
        "max_price": max_price,
        "min_installs": min_installs,
        "max_installs": max_installs,
        "content_rating": content_rating,
        "free": free,
        "ad_supported": ad_supported,
        "in_app_purchases": in_app_purchases,
        "editors_choice": editors_choice,
    }

    query = db.query(App.rating, func.count().label('count')) \
        .group_by(App.rating) \
        .order_by(App.rating)

    query = apply_filters_to_query(query, filters, db)

    result = query.all()
    return [{"rating": round(rating, 1), "count": count} for rating, count in result]


@app.get("/apps/release_trend", response_model=List[dict])
def get_app_release_trend(category_name: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    query = db.query(func.extract('year', App.released).label('year'), func.count().label('count')) \
        .group_by(func.extract('year', App.released)) \
        .order_by('year')

    filters = {
        "category": category_name
    }
    query = apply_filters_to_query(query, filters, db)

    result = query.all()
    return [{"year": int(year), "count": count} for year, count in result]


@app.get("/apps/update_trend", response_model=List[dict])
def get_app_update_trend(category_name: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    query = db.query(func.extract('year', App.last_updated).label('year'), func.count().label('count')) \
        .group_by(func.extract('year', App.last_updated)) \
        .order_by('year')

    filters = {
        "category": category_name
    }
    query = apply_filters_to_query(query, filters, db)

    result = query.all()
    return [{"year": int(year), "count": count} for year, count in result]


@app.get("/apps/average_rating/", response_model=dict)
def get_average_rating(category_name: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    query = db.query(func.avg(App.rating))

    filters = {
        "category": category_name
    }
    query = apply_filters_to_query(query, filters, db)

    avg_rating = query.scalar()
    return {"category": category_name or "All", "average_rating": avg_rating}


def get_category_id(db: SessionLocal, category_name: str) -> Optional[int]:
    category_id = db.query(Category.id).filter(Category.name == category_name).first()
    return category_id[0] if category_id else None


def apply_filters_to_query(
        query,
        filters: dict,
        db: SessionLocal
):
    category_id = get_category_id(db, filters.get("category")) if filters.get("category") else None

    if category_id:
        query = query.filter(App.category_id == category_id)
    if filters.get("min_rating"):
        query = query.filter(App.rating >= filters["min_rating"])
    if filters.get("max_rating"):
        query = query.filter(App.rating <= filters["max_rating"])
    if filters.get("min_price"):
        query = query.filter(App.price >= filters["min_price"])
    if filters.get("max_price"):
        query = query.filter(App.price <= filters["max_price"])
    if filters.get("min_installs"):
        query = query.filter(App.installs >= filters["min_installs"])
    if filters.get("max_installs"):
        query = query.filter(App.installs <= filters["max_installs"])
    if filters.get("content_rating"):
        query = query.filter(App.content_rating == filters["content_rating"])
    if filters.get("free"):
        query = query.filter(App.free == filters["free"])
    if filters.get("ad_supported"):
        query = query.filter(App.ad_supported == filters["ad_supported"])
    if filters.get("in_app_purchases"):
        query = query.filter(App.in_app_purchases == filters["in_app_purchases"])
    if filters.get("editors_choice"):
        query = query.filter(App.editors_choice == filters["editors_choice"])

    return query
