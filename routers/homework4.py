import sqlite3 as sql
from fastapi import APIRouter

router = APIRouter()

@router.on_event("startup")
async def startup():
    router.db_connection = sql.connect('./chinook.db')

@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = sql.Row
    tracks = router.db_connection.execute(
        "SELECT * FROM tracks LIMIT :per_page OFFSET :offset",
        {'per_page': per_page, 'offset': page*per_page}).fetchone()

    return tracks,
