from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List, Optional
from sqlalchemy import or_
# from fastapi.security import APIKeyHeader
# from ..config import settings

router = APIRouter(
    prefix="/itineraries",
    tags=["Itineraries"]
)


@router.get("/", response_model=List[schemas.UserItineraryOut])
def get_itinerary(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                  search: Optional[str] = ""):

    user = db.query(models.User).filter(current_user.id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {current_user.id} was not found")

    itineraries_query = db.query(models.UserItinerary).filter(current_user.id == models.UserItinerary.user_id)
    itineraries = itineraries_query.all()

    if search:

        query = (
            db.query(models.UserItinerary)
            # .join(models.Itinerary, models.UserItinerary.id == models.Itinerary.user_itinerary_id)
            # .join(models.District, models.Itinerary.district_id == models.District.id)
            # .join(models.ItineraryActivity, models.ItineraryActivity.itinerary_id == models.Itinerary.id)
            # .join(models.Activity, models.ItineraryActivity.activity_id == models.Activity.id)
            # .join(models.ItineraryAttraction, models.ItineraryAttraction.itinerary_id == models.Itinerary.id)
            # .join(models.Attraction, models.ItineraryAttraction.attraction_id == models.Attraction.id)
            # .join(models.ItineraryHotelRestaurant,
            # models.ItineraryHotelRestaurant.itinerary_id == models.Itinerary.id)
            # .join(models.HotelsAndRestaurant,
            #       models.ItineraryHotelRestaurant.hotel_restaurant_id == models.HotelsAndRestaurant.id)
            # .join(models.ItineraryTransportation, models.ItineraryTransportation.itinerary_id == models.Itinerary.id)
            # .join(models.Transportation, models.ItineraryTransportation.transportation_id == models.Transportation.id)
            .filter(models.UserItinerary.user_id == current_user.id)
            .filter(
                or_(
                    models.District.title.like(f"%{search}%"),
                    models.District.description.like(f"%{search}%"),
                    models.Activity.title.like(f"%{search}%"),
                    models.Activity.description.like(f"%{search}%"),
                    models.Attraction.title.like(f"%{search}%"),
                    models.Attraction.description.like(f"%{search}%"),
                    models.HotelsAndRestaurant.title.like(f"%{search}%"),
                    models.HotelsAndRestaurant.description.like(f"%{search}%"),
                    models.Transportation.type.like(f"%{search}%"),
                    models.Transportation.description.like(f"%{search}%"),
                    models.Transportation.destination.like(f"%{search}%"),
                    models.Transportation.origin.like(f"%{search}%")
                )
            )
        )

        # Print query for debugging
        # print(str(query))

        itineraries = query.all()

    if not itineraries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This user has no such itineraries.")

    return itineraries


@router.post("/", response_model=schemas.UserItineraryOut)
def create_itinerary(itinerary_data: schemas.ItineraryCreate, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(current_user.id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {current_user.id} was not found")

    user_itinerary = models.UserItinerary(user_id=current_user.id)
    db.add(user_itinerary)
    db.commit()
    db.refresh(user_itinerary)

    itinerary = models.Itinerary(
        user_itinerary_id=user_itinerary.id,
        district_id=itinerary_data.district_id
    )
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)

    if itinerary_data.activity_id:
        # Associate Activities
        for activity_id in itinerary_data.activity_id:
            itinerary_activity = models.ItineraryActivity(
                itinerary_id=itinerary.id,
                activity_id=activity_id
            )
            db.add(itinerary_activity)

    if itinerary_data.hotels_restaurant_id:
        # Associate Hotels/Restaurants
        for hotel_restaurant_id in itinerary_data.hotels_restaurant_id:
            itinerary_hotel_restaurant = models.ItineraryHotelRestaurant(
                itinerary_id=itinerary.id,
                hotel_restaurant_id=hotel_restaurant_id
            )
            db.add(itinerary_hotel_restaurant)

    if itinerary_data.transportation_id:
        # Associate Transportations
        for transportation_id in itinerary_data.transportation_id:
            itinerary_transportation = models.ItineraryTransportation(
                itinerary_id=itinerary.id,
                transportation_id=transportation_id
            )
            db.add(itinerary_transportation)

    if itinerary_data.attraction_id:
        # Associate Attractions
        for attraction_id in itinerary_data.attraction_id:
            itinerary_attraction = models.ItineraryAttraction(
                itinerary_id=itinerary.id,
                attraction_id=attraction_id
            )
            db.add(itinerary_attraction)

    db.commit()

    return user_itinerary


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itinerary(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(current_user.id == models.User.id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: [{current_user.id}] does not exist")

    itinerary_query = db.query(models.UserItinerary).filter(current_user.id == models.UserItinerary.user_id,
                                                            id == models.UserItinerary.id)
    itinerary = itinerary_query.first()

    if not itinerary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Itinerary with id: [{id}] does not exist under this user.")

    itinerary_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/generate/{id}", response_model=schemas.UserItineraryOut)
def generate_itinerary(id: int, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user),
                       duration: int = 2, budget: int = 2000, activities_per_day: int = 2):
    meal_count = duration * 3
    budget_per_day = budget / duration
    total_activity = activities_per_day * duration
    attraction_count, activity_count = utils.divide_into_two_parts(total_activity)

    user = db.query(models.User).filter(current_user.id == models.User.id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: [{current_user.id}] does not exist")

    district = db.query(models.District).filter(id == models.District.id).first()

    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"District with id: [{id}] not found")

    activities_data = db.query(models.Activity).filter(id == models.Activity.district_id).all()
    attractions_data = db.query(models.Attraction).filter(id == models.Attraction.district_id).all()

    if len(attractions_data) < attraction_count:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Not enough attractions found")

    if len(activities_data) < activity_count:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Not enough activities found")

    hotels_and_restaurant_data = db.query(models.HotelsAndRestaurant).filter(
        id == models.HotelsAndRestaurant.district_id,
        budget_per_day >= models.HotelsAndRestaurant.price).all()

    if len(hotels_and_restaurant_data) < meal_count:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                             detail=f"Not enough hotels and restaurants found within your parameters")

    transportation_data = db.query(models.Transportation).filter(
        id == models.Transportation.district_id).all()

    hotel_ids = utils.generate_random_result(len(hotels_and_restaurant_data), meal_count)
    activity_ids = utils.generate_random_result(len(activities_data), activity_count)
    attraction_ids = utils.generate_random_result(len(attractions_data), attraction_count)

    user_itinerary = models.UserItinerary(user_id=current_user.id)
    db.add(user_itinerary)
    db.commit()
    db.refresh(user_itinerary)

    itinerary = models.Itinerary(
        user_itinerary_id=user_itinerary.id,
        district_id=id
    )

    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)

    for ids in hotel_ids:
        itinerary_hotel_restaurant = models.ItineraryHotelRestaurant(
            itinerary_id=itinerary.id,
            hotel_restaurant_id=hotels_and_restaurant_data[ids].id
        )
        db.add(itinerary_hotel_restaurant)

    for ids in activity_ids:
        itinerary_activity = models.ItineraryActivity(
            itinerary_id=itinerary.id,
            activity_id=activities_data[ids].id
        )
        db.add(itinerary_activity)

    for ids in attraction_ids:
        itinerary_attraction = models.ItineraryAttraction(
            itinerary_id=itinerary.id,
            attraction_id=attractions_data[ids].id
        )
        db.add(itinerary_attraction)

    if len(transportation_data) != 0:
        transportation_ids = utils.select_random_result(len(transportation_data))

        for ids in transportation_ids:
            itinerary_transportation = models.ItineraryTransportation(
                itinerary_id=itinerary.id,
                transportation_id=transportation_data[ids].id
            )
            db.add(itinerary_transportation)

    db.commit()

    return user_itinerary
