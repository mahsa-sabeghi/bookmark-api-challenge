from fastapi.testclient import TestClient
from app.main import app
from app.storage import bookmarks

client = TestClient(app)


def setup_function():
    bookmarks.clear()


def test_create_bookmark():
    r = client.post("/bookmarks", json={
        "url": "https://example.com",
        "title": "Example",
        "tags": ["Test"]
    })
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["url"].rstrip("/") == "https://example.com"
    assert data["title"] == "Example"
    assert data["tags"] == ["test"]
    assert "created_at" in data


def test_prevent_duplicate_url():
    client.post("/bookmarks", json={
        "url": "https://example.com",
        "title": "Example",
        "tags": ["t"]
    })
    r = client.post("/bookmarks", json={
        "url": "https://example.com",
        "title": "Example 2",
        "tags": ["t2"]
    })
    assert r.status_code == 409


def test_list_bookmarks():
    client.post("/bookmarks", json={
        "url": "https://a.com",
        "title": "A",
        "tags": ["t1"]
    })
    r = client.get("/bookmarks")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_bookmark_by_id():
    created = client.post("/bookmarks", json={
        "url": "https://a.com",
        "title": "A",
        "tags": ["t1"]
    }).json()
    r = client.get(f"/bookmarks/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_missing_bookmark():
    r = client.get("/bookmarks/doesnotexist")
    assert r.status_code == 404


def test_search_by_tag():
    client.post("/bookmarks", json={
        "url": "https://a.com",
        "title": "Alpha",
        "tags": ["Python", "api"]
    })
    client.post("/bookmarks", json={
        "url": "https://b.com",
        "title": "Beta",
        "tags": ["dev"]
    })

    r = client.get("/bookmarks/search", params={"tag": "python"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert "python" in items[0]["tags"]


def test_search_by_q_case_insensitive():
    client.post("/bookmarks", json={
        "url": "https://fastapi.tiangolo.com",
        "title": "FastAPI Documentation",
        "tags": ["python"]
    })
    r = client.get("/bookmarks/search", params={"q": "fastapi"})
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_search_by_tag_and_q_and_logic():
    client.post("/bookmarks", json={
        "url": "https://a.com",
        "title": "FastAPI Docs",
        "tags": ["python"]
    })
    client.post("/bookmarks", json={
        "url": "https://b.com",
        "title": "Python Tips",
        "tags": ["python"]
    })

    r = client.get("/bookmarks/search", params={"tag": "python", "q": "fastapi"})
    assert r.status_code == 200
    assert len(r.json()) == 1
