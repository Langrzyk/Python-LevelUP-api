import sqlite3 as sql
from fastapi import APIRouter, Response, status

router = APIRouter()

@router.on_event("startup")
async def startup():
    router.db_connection = sql.connect("chinook.db")

@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()

@router.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = sql.Row
    tracks = router.db_connection.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT :per_page OFFSET :offset",
        {'per_page': per_page, 'offset': page*per_page}).fetchall()

    return tracks

@router.get("/tracks/composers")
async def composers(response: Response, composer_name: str):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    data = router.db_connection.execute(
        "SELECT Name FROM tracks WHERE Composer = :composer ORDER By name",
        {'composer': composer_name}).fetchall()
    if len(data) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":{"error":"No tracks for composer"}}

    return data
