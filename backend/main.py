from typing import List, Optional

from fastapi import Query, Depends, FastAPI
from sqlalchemy import func

from models import FilterModel, AppModel, CategoryModel, DeveloperModel, UpsertCategoryModel
from database import SessionLocal, get_db
from entities import Category, App, Developer

app = FastAPI()


@app.get("/filters", response_model=FilterModel)
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
    return FilterModel(
        categories=categories,
        content_ratings=content_ratings,
        min_rating=min_rating,
        max_rating=max_rating,
        min_price=min_price,
        max_price=max_price,
        min_installs=min_installs,
        max_installs=max_installs
    )


@app.get("/apps", response_model=dict)
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
        page: Optional[int] = Query(1, ge=1),
        per_page: Optional[int] = Query(100, ge=1),
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

    offset = (page - 1) * per_page
    apps = query.offset(offset).limit(per_page).all()
    total_apps = query.count()
    total_pages = (total_apps // per_page) + (1 if total_apps % per_page > 0 else 0)

    return {
        "apps": [AppModel.from_orm(app) for app in apps],
        "total_apps": total_apps,
        "total_pages": total_pages,
        "current_page": page,
    }


@app.get("/statistics/rating_distribution", response_model=List[dict])
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


@app.get("/statistics/release_trend", response_model=List[dict])
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


@app.get("/statistics/update_trend", response_model=List[dict])
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


@app.get("/statistics/average_rating/", response_model=dict)
def get_average_rating(category_name: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    query = db.query(func.avg(App.rating))

    filters = {
        "category": category_name
    }
    query = apply_filters_to_query(query, filters, db)

    avg_rating = query.scalar()
    return {"category": category_name or "All", "average_rating": avg_rating}


@app.post("/categories", response_model=CategoryModel)
def create_category(category: UpsertCategoryModel, db: SessionLocal = Depends(get_db)):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return CategoryModel.from_orm(db_category)


@app.get("/categories", response_model=List[CategoryModel])
def get_categories(db: SessionLocal = Depends(get_db)):
    return [CategoryModel.from_orm(category) for category in db.query(Category).all()]


@app.get("/categories/{category_id}", response_model=CategoryModel)
def get_category(category_id: int, db: SessionLocal = Depends(get_db)):
    return CategoryModel.from_orm(db.query(Category).filter(Category.id == category_id).first())


@app.put("/categories/{category_id}", response_model=CategoryModel)
def update_category(category_id: int, category: UpsertCategoryModel, db: SessionLocal = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db_category.name = category.name
        db.commit()
        db.refresh(db_category)
        return CategoryModel.from_orm(db_category)
    return None


@app.delete("/categories/{category_id}", response_model=CategoryModel)
def delete_category(category_id: int, db: SessionLocal = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return CategoryModel.from_orm(db_category)
    return None


@app.post("/developers", response_model=DeveloperModel)
def create_developer(developer: DeveloperModel, db: SessionLocal = Depends(get_db)):
    db_developer = Developer(name=developer.name, email=developer.email)
    db.add(db_developer)
    db.commit()
    db.refresh(db_developer)
    return DeveloperModel.from_orm(db_developer)


@app.get("/developers", response_model=dict)
def get_developers(
        page: Optional[int] = Query(1, ge=1),
        per_page: Optional[int] = Query(10, ge=1),
        db: SessionLocal = Depends(get_db)
):
    total_developers = db.query(Developer).count()
    total_pages = (total_developers // per_page) + (1 if total_developers % per_page > 0 else 0)

    offset = (page - 1) * per_page
    developers = db.query(Developer).offset(offset).limit(per_page).all()

    return {
        "developers": [DeveloperModel.from_orm(developer) for developer in developers],
        "total_developers": total_developers,
        "total_pages": total_pages,
        "current_page": page,
    }


@app.get("/developers/{developer_id}", response_model=DeveloperModel)
def get_developer(developer_id: int, db: SessionLocal = Depends(get_db)):
    return DeveloperModel.from_orm(db.query(Developer).filter(Developer.id == developer_id).first())


@app.put("/developers/{developer_id}", response_model=DeveloperModel)
def update_developer(developer_id: int, developer: DeveloperModel, db: SessionLocal = Depends(get_db)):
    db_developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if db_developer:
        db_developer.name = developer.name
        db_developer.email = developer.email
        db.commit()
        db.refresh(db_developer)
        return DeveloperModel.from_orm(db_developer)
    return None


@app.delete("/developers/{developer_id}", response_model=DeveloperModel)
def delete_developer(developer_id: int, db: SessionLocal = Depends(get_db)):
    db_developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if db_developer:
        db.delete(db_developer)
        db.commit()
        return DeveloperModel.from_orm(db_developer)
    return None


@app.post("/apps", response_model=AppModel)
def create_app(app: AppModel, db: SessionLocal = Depends(get_db)):
    db_app = App(
        app_id=app.app_id,
        app_name=app.app_name,
        category_id=app.category_id,
        developer_id=app.developer_id,
        rating=app.rating,
        rating_count=app.rating_count,
        installs=app.installs,
        min_installs=app.min_installs,
        max_installs=app.max_installs,
        free=app.free,
        price=app.price,
        currency=app.currency,
        size=app.size,
        min_android=app.min_android,
        released=app.released,
        last_updated=app.last_updated,
        content_rating=app.content_rating,
        ad_supported=app.ad_supported,
        in_app_purchases=app.in_app_purchases,
        editors_choice=app.editors_choice
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return AppModel.from_orm(db_app)


@app.get("/apps/{app_id}", response_model=AppModel)
def get_app(app_id: int, db: SessionLocal = Depends(get_db)):
    return AppModel.from_orm(db.query(App).filter(App.id == app_id).first())


@app.put("/apps/{app_id}", response_model=AppModel)
def update_app(app_id: int, app: AppModel, db: SessionLocal = Depends(get_db)):
    db_app = db.query(App).filter(App.id == app_id).first()
    if db_app:
        db_app.app_name = app.app_name
        db_app.category_id = app.category_id
        db_app.developer_id = app.developer_id
        db_app.rating = app.rating
        db_app.rating_count = app.rating_count
        db_app.installs = app.installs
        db_app.min_installs = app.min_installs
        db_app.max_installs = app.max_installs
        db_app.free = app.free
        db_app.price = app.price
        db_app.currency = app.currency
        db_app.size = app.size
        db_app.min_android = app.min_android
        db_app.released = app.released
        db_app.last_updated = app.last_updated
        db_app.content_rating = app.content_rating
        db_app.ad_supported = app.ad_supported
        db_app.in_app_purchases = app.in_app_purchases
        db_app.editors_choice = app.editors_choice
        db.commit()
        db.refresh(db_app)
        return AppModel.from_orm(db_app)
    return None


@app.delete("/apps/{app_id}", response_model=AppModel)
def delete_app(app_id: int, db: SessionLocal = Depends(get_db)):
    db_app = db.query(App).filter(App.id == app_id).first()
    if db_app:
        db.delete(db_app)
        db.commit()
        return AppModel.from_orm(db_app)
    return None


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
