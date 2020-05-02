import sqlite3 as sql
from fastapi import APIRouter, Response, status
from pydantic import BaseModel

class Albums(BaseModel):
    title: str
    artist_id: int

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

@router.post("/albums")
async def album_add(response: Response, album: Albums):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    artist = router.db_connection.execute(
        "SELECT Artistid FROM artists WHERE Artistid = :id",
        {'id': album.artist_id}).fetchall()
    if not artist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":{"error":"No Artist with id"}}

    data = router.db_connection.execute(
        "INSERT INTO albums (Title, Artistid) VALUES (:Title , :id)",
        {'Title': album.title, 'id': artist_id})
    router.db_connection.commit()
    new_album_id = cursor.lastrowid
    router.db_connection.row_factory = sql.Row
    album = router.db_connection.execute(
        "SELECT AlbumId, title, artistid FROM albums WHERE albumid = :id",
         {'id': new_album_id}).fetchone()

    response.status_code = status.HTTP_201_CREATED
    return {"AlbumId": cursor.lastrowid, "Title": album.title, "ArtistId": album.artist_id}

@router.get("/albums/{album_id}")
async def Album_check(album_id: int):
	router.db_connection.row_factory = sql.Row
	data = router.db_connection.execute("SELECT * FROM albums WHERE AlbumId = :id",
		{'id':album_id}).fetchone()

	return data
