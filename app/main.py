from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .routers import item, admin, user, auth, cart, stat
# from . import models
from .database import engine


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

# app.include_router(item.router)
# app.include_router(admin.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(cart.router)
# app.include_router(stat.router)


@app.get("/")
async def root():
    return {"message": "Welcome to 'TravelSense API'"}