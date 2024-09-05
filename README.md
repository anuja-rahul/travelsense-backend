![Python](https://img.shields.io/badge/-python-000?style=for-the-badge&logo=python)
![FAST API](https://img.shields.io/badge/-fast_api-000?style=for-the-badge&logo=fastapi)
![POSTMAN](https://img.shields.io/badge/-postman-000?style=for-the-badge&logo=postman)
![PYDANTIC](https://img.shields.io/badge/-pydantic-000?style=for-the-badge&logo=pydantic)
![POSTGRES](https://img.shields.io/badge/-postgresql-000?style=for-the-badge&logo=postgresql)
![SQLALCHEMY](https://img.shields.io/badge/-sqlalchemy-000?style=for-the-badge&logo=sqlalchemy)
![JWT](https://img.shields.io/badge/-JWT-000?style=for-the-badge&logo=json-web-tokens)

# travelsense-backend

![GitHub](https://img.shields.io/github/forks/TravelSenseRC/travelsense-backend?style&logo=github)
&nbsp;
![GitHub](https://img.shields.io/github/license/TravelSenseRC/travelsense-backend?style&logo=github)
&nbsp;
![GitHub](https://img.shields.io/github/stars/TravelSenseRC/travelsense-backend?style&logo=github)
&nbsp;
![Contributors](https://img.shields.io/github/contributors/TravelSenseRC/travelsense-backend?style&logo=github)
&nbsp;
![Watchers](https://img.shields.io/github/watchers/TravelSenseRC/travelsense-backend?style&logo=github)
&nbsp;

## Prerequisites  

- [python ≥ 3.10](https://www.python.org/downloads/)
- [postgresSQL ≥ 16.0](https://www.postgresql.org/download/)



![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=TravelSenseRC&repo=travelsense-backend&theme=nightowl)

---

## Database Table Structure

```mermaid

erDiagram
    Category {
        int id PK
        string title
        string description
        string image_url
        timestamp created_at
        int added_by FK
    }
    Admin {
        int id PK
        string name
        string email
        string password
        string image_url
        timestamp created_at
    }
    Province {
        int id PK
        string title
        string description
        string image_url
        timestamp created_at
    }
    District {
        int id PK
        int province_id FK
        string title
        string description
        string image_url
        timestamp created_at
    }
    Activity {
        int id PK
        int district_id FK
        string title
        string description
        string image_url
        timestamp created_at
    }
    HotelsAndRestaurant {
        int id PK
        int district_id FK
        string type
        string cuisine
        string comfort
        string title
        string description
        string image_url
        timestamp created_at
    }
    Transportation {
        int id PK
        int district_id FK
        string type
        string origin
        string destination
        string description
        string departure
        string arrival
        string image_url
        timestamp created_at
    }
    Attraction {
        int id PK
        int district_id FK
        string type
        string title
        string description
        string image_url
        timestamp created_at
    }
    User {
        int id PK
        string name
        string email
        string password
        boolean verified
        string image_url
        timestamp created_at
    }
    UserVerification {
        int id PK
        int user_id FK
        string verification_code
        timestamp expires_at
        timestamp verified_at
        timestamp created_at
    }
    UserItinerary {
        int id PK
        int user_id FK
    }
    Itinerary {
        int id PK
        int user_itinerary_id FK
        int district_id FK
        timestamp created_at
    }
    ItineraryActivity {
        int id PK
        int itinerary_id FK
        int activity_id FK
    }
    ItineraryHotelRestaurant {
        int id PK
        int itinerary_id FK
        int hotel_restaurant_id FK
    }
    ItineraryTransportation {
        int id PK
        int itinerary_id FK
        int transportation_id FK
    }
    ItineraryAttraction {
        int id PK
        int itinerary_id FK
        int attraction_id FK
    }

    Category ||--o{ Admin: "added_by"
    Province ||--o{ District: "province_id"
    District ||--o{ Activity: "district_id"
    District ||--o{ HotelsAndRestaurant: "district_id"
    District ||--o{ Transportation: "district_id"
    District ||--o{ Attraction: "district_id"
    User ||--o{ UserItinerary: "user_id"
    User ||--o{ UserVerification: "user_id"
    UserItinerary ||--o{ Itinerary: "user_itinerary_id"
    Itinerary ||--o{ ItineraryActivity: "itinerary_id"
    Itinerary ||--o{ ItineraryHotelRestaurant: "itinerary_id"
    Itinerary ||--o{ ItineraryTransportation: "itinerary_id"
    Itinerary ||--o{ ItineraryAttraction: "itinerary_id"
    Activity ||--o{ ItineraryActivity: "activity_id"
    HotelsAndRestaurant ||--o{ ItineraryHotelRestaurant: "hotel_restaurant_id"
    Transportation ||--o{ ItineraryTransportation: "transportation_id"
    Attraction ||--o{ ItineraryAttraction: "attraction_id"

```

---

## Models (Tables) Overview

### **Category**
- **Purpose**: Represents different categories of items or topics.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `title`: String
  - `description`: String
  - `image_url`: String (URL to the image associated with the category)
  - `created_at`: TIMESTAMP
  - `added_by`: Integer (Foreign Key to `Admin`)
- **Relationships**: 
  - Linked to `Admin` (who added the category).

### **Province**
- **Purpose**: Represents geographical provinces.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `title`: String
  - `description`: String
  - `image_url`: String (URL to the image associated with the province)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Has many `Districts`.

### **District**
- **Purpose**: Represents smaller geographical areas within a province.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `province_id`: Integer (Foreign Key to `Province`)
  - `title`: String
  - `description`: String
  - `image_url`: String (URL to the image associated with the district)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Linked to `Province` (each district belongs to one province).
  - Has many `Activities`, `HotelsAndRestaurants`, `Transportation`, and `Attractions`.

### **Activity**
- **Purpose**: Represents various activities that can be done in a district.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `district_id`: Integer (Foreign Key to `District`)
  - `title`: String
  - `description`: String
  - `image_url`: String (URL to the image associated with the activity)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Linked to `District` (each activity is in one district).
  - Associated with itineraries through `ItineraryActivity`.

### **HotelsAndRestaurant**
- **Purpose**: Represents hotels and restaurants in a district.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `district_id`: Integer (Foreign Key to `District`)
  - `type`: String
  - `cuisine`: String
  - `comfort`: String
  - `title`: String
  - `description`: String
  - `image_url`: String (URL to the image associated with the hotel or restaurant)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Linked to `District` (each hotel/restaurant is in one district).
  - Associated with itineraries through `ItineraryHotelRestaurant`.

### **Transportation**
- **Purpose**: Represents transportation options within a district.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `district_id`: Integer (Foreign Key to `District`)
  - `type`: String
  - `origin`: String
  - `destination`: String
  - `description`: String
  - `departure`: String
  - `arrival`: String
  - `image_url`: String (URL to the image associated with the transportation)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Linked to `District` (each transportation option is in one district).
  - Associated with itineraries through `ItineraryTransportation`.

### **Attraction**
- **Purpose**: Represents tourist attractions in a district.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `district_id`: Integer (Foreign Key to `District`)
  - `type`: String
  - `title`: String
  - `description`: String
  - `image_url`: String (URL to the image associated with the attraction)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Linked to `District` (each attraction is in one district).
  - Associated with itineraries through `ItineraryAttraction`.

### **User**
- **Purpose**: Represents the users of the application.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `name`: String
  - `email`: String
  - `password`: String
  - `verified`: Boolean
  - `image_url`: String (URL to the user's profile image)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Can have `UserItineraries`.
  - Can have `UserVerification` records.

### **UserVerification**
- **Purpose**: Represents verification codes sent to users for account verification.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `user_id`: Integer (Foreign Key to `User`)
  - `verification_code`: String (Verification code sent to the user)
  - `expires_at`: TIMESTAMP (When the code expires)
  - `verified_at`: TIMESTAMP (When the user was verified, nullable)
  - `created_at`: TIMESTAMP
- **Relationships**:
  - Linked to `User` (each verification record is for one user).

### **UserItinerary**
- **Purpose**: Links users to itineraries, allowing users to have personal itineraries.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `user_id`: Integer (Foreign Key to `User`)
- **Relationships**: 
  - Linked to `User` (each itinerary belongs to a user).
  - Can be linked to multiple `Itineraries`, but this relationship is optional.

### **Itinerary**
- **Purpose**: Represents a planned itinerary that includes activities, hotels/restaurants, transportation, and attractions for a specific district.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `user_itinerary_id`: Integer (Foreign Key to `UserItinerary`)
  - `district_id`: Integer (Foreign Key to `District`)
  - `image_url`: String (URL to an image representing the itinerary)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Linked to `District` (each itinerary is for one district).
  - Optionally linked to a `UserItinerary`.
  - Has many `Activities`, `HotelsAndRestaurants`, `Transportations`, and `Attractions` through their respective models.

### **ItineraryActivity**
- **Purpose**: Links activities to specific itineraries.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `itinerary_id`: Integer (Foreign Key to `Itinerary`)
  - `activity_id`: Integer (Foreign Key to `Activity`)
- **Relationships**: 
  - Linked to `Itinerary` (each record associates an activity with an itinerary).
  - Linked to `Activity` (each record specifies which activity is included in the itinerary).

### **ItineraryHotelRestaurant**
- **Purpose**: Links hotels and restaurants to specific itineraries.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `itinerary_id`: Integer (Foreign Key to `Itinerary`)
  - `hotel_restaurant_id`: Integer (Foreign Key to `HotelsAndRestaurant`)
- **Relationships**: 
  - Linked to `Itinerary` (each record associates a hotel/restaurant with an itinerary).
  - Linked to `HotelsAndRestaurant` (each record specifies which hotel/restaurant is included in the itinerary).

### **ItineraryTransportation**
- **Purpose**: Links transportation options to specific itineraries.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `itinerary_id`: Integer (Foreign Key to `Itinerary`)
  - `transportation_id`: Integer (Foreign Key to `Transportation`)
- **Relationships**: 
  - Linked to `Itinerary` (each record associates a transportation option with an itinerary).
  - Linked to `Transportation` (each record specifies which transportation option is included in the itinerary).

### **ItineraryAttraction**
- **Purpose**: Links attractions to specific itineraries.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `itinerary_id`: Integer (Foreign Key to `Itinerary`)
  - `attraction_id`: Integer (Foreign Key to `Attraction`)
- **Relationships**: 
  - Linked to `Itinerary` (each record associates an attraction with an itinerary).
  - Linked to `Attraction` (each record specifies which attraction is included in the itinerary).

### **Admin**
- **Purpose**: Represents the administrators of the system.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `name`: String
  - `email`: String
  - `password`: String
  - `image_url`: String (URL to the admin's profile image)
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Can manage `Categories` and `Itineraries`.

