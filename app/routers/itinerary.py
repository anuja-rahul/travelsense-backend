from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security import APIKeyHeader
from ..config import settings


router = APIRouter(
    prefix="/itineraries",
    tags=["Itineraries"]
)



