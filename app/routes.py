from fastapi import APIRouter, HTTPException, Query

from .models import BookmarkCreate, Bookmark
from . import storage

router = APIRouter()


@router.post("/bookmarks", response_model=Bookmark, status_code=201)
def create_bookmark(data: BookmarkCreate):
    url_str = str(data.url)
    if storage.exists_url(url_str):
        raise HTTPException(status_code=409, detail="Bookmark with this URL already exists")
    return storage.create(data)


@router.get("/bookmarks", response_model=list[Bookmark])
def list_bookmarks():
    return storage.list_all()


@router.get("/bookmarks/search", response_model=list[Bookmark])
def search_bookmarks(
    tag: str | None = Query(default=None),
    q: str | None = Query(default=None),
):
    return storage.search(tag=tag, q=q)


@router.get("/bookmarks/{bookmark_id}", response_model=Bookmark)
def get_bookmark(bookmark_id: str):
    b = storage.get_by_id(bookmark_id)
    if not b:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return b


@router.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: str):
    ok = storage.delete_by_id(bookmark_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return None
