from fastapi import FastAPI
from routers import homework1, homework3, homework4

app = FastAPI()

app.include_router(homework1.router, tags=['endpoint homework1'])
app.include_router(homework3.router, tags=['endpoint homework3'])
app.include_router(homework4.router, tags=['endpoint homework4'])
