from sqlalchemy import Column, Integer, String, Float, Boolean, Date, TIMESTAMP, ForeignKey, Index

from database import Base


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
