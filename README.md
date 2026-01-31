# Bookmark API Challenge

A simple bookmarking API built with **FastAPI**.

## Features

- Create a bookmark  
- List all bookmarks  
- Retrieve a bookmark by ID  
- Delete a bookmark by ID  
- Search bookmarks by **tag** and/or **title query** (`AND` logic)

## Improvements

- Prevent duplicate bookmarks by URL (`409 Conflict`)
- Case-insensitive search for tags and title queries
- Store timestamps in UTC for consistency
- Sort results by newest first

## Run locally

Install dependencies:

```bash
pip install fastapi uvicorn
```

Start the server:

```bash
python -m uvicorn main:app --reload
```

Open Swagger UI in your browser:

```
http://127.0.0.1:8000/docs
```
