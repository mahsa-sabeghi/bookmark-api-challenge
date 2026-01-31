from pydantic import BaseModel, HttpUrl
from datetime import datetime


class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str
    tags: list[str] = []


class Bookmark(BookmarkCreate):
    id: str
    created_at: datetime
