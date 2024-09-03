from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, user, itinerary, auth, entry
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TravelSense-API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

origins = ["*"]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(itinerary.router)
app.include_router(entry.router)


@app.get("/")
async def root():
    return {"message": "Welcome to 'TravelSense API'"}