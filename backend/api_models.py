from datetime import date, datetime
from typing import List, Optional

from pydantic import field_serializer, BaseModel


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


class PaginatedAppsResponse(BaseModel):
    apps: List[AppResponse]
    total_apps: int
    total_pages: int
    current_page: int
