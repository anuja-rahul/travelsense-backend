from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_result(number, count):
    return random.sample(range(number), count)


def select_random_result(number):
    return random.randint(0, number - 1)


def divide_into_two_parts(n):
    part1 = n // 2
    part2 = n - part1

    return part1, part2


# def generate_itineraryKESHAWA(budget, duration, diet_preference, activities):
#     # Step 1: Initialize and gather inputs
#     itinerary = []
#
#     # Step 2: Retrieve data based on user inputs
#     accommodations = get_accommodations(budget)
#     restaurants = get_restaurants(diet_preference, budget)
#     attractions = get_attractions(activities, budget)
#
#     # Step 3: Construct day-by-day itinerary
#     for day in range(1, duration + 1):
#         daily_plan = {}
#
#         # Morning activity
#         morning_activity = select_activity(attractions)
#         daily_plan['morning'] = morning_activity
#
#         # Lunch
#         lunch_spot = select_restaurant(restaurants, morning_activity['location'])
#         daily_plan['lunch'] = lunch_spot
#
#         # Afternoon activity
#         afternoon_activity = select_activity(attractions)
#         daily_plan['afternoon'] = afternoon_activity
#
#         # Dinner
#         dinner_spot = select_restaurant(restaurants, afternoon_activity['location'])
#         daily_plan['dinner'] = dinner_spot
#
#         # Accommodation
#         night_stay = select_accommodation(accommodations, dinner_spot['location'])
#         daily_plan['accommodation'] = night_stay
#
#         itinerary.append(daily_plan)
#
#     # Step 4: Budget Allocation
#     if not within_budget(itinerary, budget):
#         adjust_itinerary_to_fit_budget(itinerary, budget)
#
#     # Step 5: Final Adjustment
#     optimize_itinerary(itinerary)
#
#     # Step 6: Output Generation
#     output_itinerary(itinerary)
#
#     # Step 7: Save Itinerary
#     save_itinerary_to_database(itinerary)
#
#     return itinerary
# #Ill take a look at the variables in this total code and make some changes, this is just from what ive written on paper...
