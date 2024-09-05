from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas
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


# TODO: ADD search params to entry endpoint


@router.get("/", response_model=Union[
    List[schemas.DistrictBase], list[schemas.AttractionOut], list[schemas.TransportationOut],
    List[schemas.ActivityOut], List[schemas.HotelsAndRestaurantsOut], List[schemas.ProvinceBase]])
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


@router.delete("/provinces/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_province(id: int, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:

        province_query = db.query(models.Province).filter(id == models.Province.id)
        province = province_query.first()

        if province is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Province with id: [{id}] does not exist")

        province_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

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


@router.delete("/districts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_district(id: int, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:

        district_query = db.query(models.District).filter(id == models.District.id)
        district = district_query.first()

        if district is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"District with id: [{id}] does not exist")

        district_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

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


@router.delete("/activities/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_activity(id: int, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:

        activity_query = db.query(models.Activity).filter(id == models.Activity.id)
        activity = activity_query.first()

        if activity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Activity with id: [{id}] does not exist")

        activity_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.post("/hotels_and_restaurants", status_code=status.HTTP_201_CREATED,
             response_model=schemas.HotelsAndRestaurantsOut)
def add_hotels_and_restaurants(entry: schemas.HotelsAndRestaurantsCreate, db: Session = Depends(get_db),
                               key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            new_hotel_and_restaurant = models.HotelsAndRestaurant(**entry.model_dump())
            db.add(new_hotel_and_restaurant)
            db.commit()
            db.refresh(new_hotel_and_restaurant)
            return new_hotel_and_restaurant
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.delete("/hotels_and_restaurants/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_hotels_and_restaurants(id: int, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:

        hotel_and_restaurant_query = db.query(models.HotelsAndRestaurant).filter(id == models.HotelsAndRestaurant.id)
        hotel_and_restaurant = hotel_and_restaurant_query.first()

        if hotel_and_restaurant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Hotel or Restaurant with id: [{id}] does not exist")

        hotel_and_restaurant_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.post("/transportations", status_code=status.HTTP_201_CREATED,
             response_model=schemas.TransportationOut)
def add_transportation(entry: schemas.TransportationCreate, db: Session = Depends(get_db),
                       key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            new_transportation = models.Transportation(**entry.model_dump())
            db.add(new_transportation)
            db.commit()
            db.refresh(new_transportation)
            return new_transportation
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.delete("/transportations/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_transportation(id: int, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:

        transportation_query = db.query(models.Transportation).filter(id == models.Transportation.id)
        transportation = transportation_query.first()

        if transportation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Transportation with id: [{id}] does not exist")

        transportation_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.post("/attractions", status_code=status.HTTP_201_CREATED,
             response_model=schemas.AttractionOut)
def add_attraction(entry: schemas.AttractionsCreate, db: Session = Depends(get_db),
                   key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:
        try:
            new_attraction = models.Attraction(**entry.model_dump())
            db.add(new_attraction)
            db.commit()
            db.refresh(new_attraction)
            return new_attraction
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="already exists")

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")


@router.delete("/attractions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_attraction(id: int, db: Session = Depends(get_db), key: str = Depends(user_header_scheme)):
    if key == settings.ADMIN_TOKEN:

        attraction_query = db.query(models.Attraction).filter(id == models.Attraction.id)
        attraction = attraction_query.first()

        if attraction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Attraction with id: [{id}] does not exist")

        attraction_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to perform this action")
