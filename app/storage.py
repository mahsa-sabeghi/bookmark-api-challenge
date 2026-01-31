from datetime import datetime, timezone
from typing import Optional
import uuid

from .models import BookmarkCreate

bookmarks: dict[str, dict] = {}


def normalize(s: str) -> str:
    return s.strip().lower()


def list_all() -> list[dict]:
    return sorted(list(bookmarks.values()), key=lambda b: b["created_at"], reverse=True)


def get_by_id(bookmark_id: str) -> Optional[dict]:
    return bookmarks.get(bookmark_id)


def delete_by_id(bookmark_id: str) -> bool:
    if bookmark_id not in bookmarks:
        return False
    del bookmarks[bookmark_id]
    return True


def exists_url(url: str) -> bool:
    return any(b["url"] == url for b in bookmarks.values())


def create(data: BookmarkCreate) -> dict:
    bookmark_id = str(uuid.uuid4())[:8]
    url_str = str(data.url)

    bookmark = {
        "id": bookmark_id,
        "url": url_str,
        "title": data.title.strip(),
        "tags": [normalize(t) for t in data.tags if t and t.strip()],
        "created_at": datetime.now(timezone.utc),
    }
    bookmarks[bookmark_id] = bookmark
    return bookmark


def search(tag: Optional[str], q: Optional[str]) -> list[dict]:
    tag_n = normalize(tag) if tag else None
    q_n = normalize(q) if q else None

    results: list[dict] = []
    for b in bookmarks.values():
        if tag_n is not None and tag_n not in b.get("tags", []):
            continue
        if q_n is not None and q_n not in normalize(b.get("title", "")):
            continue
        results.append(b)

    return sorted(results, key=lambda b: b["created_at"], reverse=True)
