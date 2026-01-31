from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timezone
from typing import Optional

app = FastAPI()

bookmarks: dict[str, dict] = {}

class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str
    tags: list[str] = []

class Bookmark(BookmarkCreate):
    id: str
    created_at: datetime

def _norm(s: str) -> str:
    return s.strip().lower()

@app.post("/bookmarks", response_model=Bookmark, status_code=201)
def create_bookmark(data: BookmarkCreate):
    # Improvement 1: prevent duplicates by URL (409)
    url_str = str(data.url)
    for b in bookmarks.values():
        if b["url"] == url_str:
            raise HTTPException(status_code=409, detail="Bookmark with this URL already exists")

    import uuid
    bookmark_id = str(uuid.uuid4())[:8]

    # Improvement 2: normalize tags (case-insensitive search later)
    normalized_tags = [_norm(t) for t in data.tags if t and t.strip()]

    bookmark = {
        "id": bookmark_id,
        "url": url_str,
        "title": data.title.strip(),
        "tags": normalized_tags,
        # Improvement 3: UTC timezone-aware timestamps
        "created_at": datetime.now(timezone.utc),
    }

    bookmarks[bookmark_id] = bookmark
    return bookmark

@app.get("/bookmarks", response_model=list[Bookmark])
def list_bookmarks():
    # Improvement 4: sort newest first
    return sorted(list(bookmarks.values()), key=lambda x: x["created_at"], reverse=True)

@app.get("/bookmarks/search", response_model=list[Bookmark])
def search_bookmarks(
    tag: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
):
    tag_n = _norm(tag) if tag else None
    q_n = _norm(q) if q else None

    results = []
    for b in bookmarks.values():
        if tag_n is not None and tag_n not in b.get("tags", []):
            continue
        if q_n is not None and q_n not in _norm(b.get("title", "")):
            continue
        results.append(b)

    return sorted(results, key=lambda x: x["created_at"], reverse=True)

@app.get("/bookmarks/{bookmark_id}", response_model=Bookmark)
def get_bookmark(bookmark_id: str):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmarks[bookmark_id]

@app.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: str):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    del bookmarks[bookmark_id]
