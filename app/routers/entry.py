from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security import APIKeyHeader
from ..config import settings
from typing import List, Union
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/entries",
    tags=["Data Entries"]
)

user_header_scheme = APIKeyHeader(name="admin_token")


@router.get("/", response_model=Union[
    List[schemas.DistrictBase], list[schemas.AttractionsBase], list[schemas.TransportationBase],
    List[schemas.ActivityBase], List[schemas.HotelRestaurantBase], List[schemas.ProvinceBase]])
def get_entries(entry: schemas.EntryBase, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    entries = ["transportations", "attractions", "activities", "hotels_and_restaurants", "districts", "provinces"]

    if key == settings.ADMIN_TOKEN:
        if entry.category == entries[0]:
            result = db.query(models.Transportation).all()
        elif entry.category == entries[1]:
            result = db.query(models.Attraction).all()
        elif entry.category == entries[2]:
            result = db.query(models.Activity).all()
        elif entry.category == entries[3]:
            result = db.query(models.HotelsAndRestaurant).all()
        elif entry.category == entries[4]:
            result = db.query(models.District).all()
        elif entry.category == entries[5]:
            result = db.query(models.Province).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such entries")

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such entries")

        return result

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.post("/provinces", status_code=status.HTTP_201_CREATED, response_model=schemas.ProvinceBase)
def add_provinces(entry: schemas.ProvinceCreate, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            new_province = models.Province(**entry.model_dump())
            db.add(new_province)
            db.commit()
            db.refresh(new_province)
            return new_province
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.post("/districts", status_code=status.HTTP_201_CREATED, response_model=schemas.DistrictBase)
def add_districts(entry: schemas.DistrictCreate, db: Session = Depends(get_db),
                  key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            new_district = models.District(**entry.model_dump())
            db.add(new_district)
            db.commit()
            db.refresh(new_district)
            return new_district
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.post("/activities", status_code=status.HTTP_201_CREATED, response_model=schemas.ActivityOut)
def add_activities(entry: schemas.ActivityCreate, db: Session = Depends(get_db),
                 key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            new_activity = models.Activity(**entry.model_dump())
            db.add(new_activity)
            db.commit()
            db.refresh(new_activity)
            return new_activity
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")
