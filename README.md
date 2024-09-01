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
        Integer id PK
        String title
        String description
        TIMESTAMP created_at
        Integer added_by FK
    }
    Admin {
        Integer id PK
        String name
        String email
        String password
        TIMESTAMP created_at
    }
    Province {
        Integer id PK
        String title
        String description
        TIMESTAMP created_at
    }
    District {
        Integer id PK
        Integer province_id FK
        String title
        String description
        TIMESTAMP created_at
    }
    Activity {
        Integer id PK
        Integer district_id FK
        String title
        String description
        TIMESTAMP created_at
    }
    HotelsAndRestaurant {
        Integer id PK
        Integer district_id FK
        String type
        String cuisine
        String comfort
        String title
        String description
        TIMESTAMP created_at
    }
    Transportation {
        Integer id PK
        Integer district_id FK
        String type
        String origin
        String destination
        String description
        String departure
        String arrival
        TIMESTAMP created_at
    }
    Attraction {
        Integer id PK
        Integer district_id FK
        String type
        String title
        String description
        TIMESTAMP created_at
    }
    User {
        Integer id PK
        String name
        String email
        String password
        Boolean verified
        TIMESTAMP created_at
    }
    UserItinerary {
        Integer id PK
        Integer user_id FK
    }
    Itinerary {
        Integer id PK
        Integer district_id FK
        Integer admin_id FK
        TIMESTAMP created_at
    }
    ItineraryActivity {
        Integer id PK
        Integer itinerary_id FK
        Integer activity_id FK
    }
    ItineraryHotelRestaurant {
        Integer id PK
        Integer itinerary_id FK
        Integer hotel_restaurant_id FK
    }
    ItineraryTransportation {
        Integer id PK
        Integer itinerary_id FK
        Integer transportation_id FK
    }
    ItineraryAttraction {
        Integer id PK
        Integer itinerary_id FK
        Integer attraction_id FK
    }

    Category ||--o| Admin : added_by
    Province ||--o| District : has
    District ||--o| Activity : has
    District ||--o| HotelsAndRestaurant : has
    District ||--o| Transportation : has
    District ||--o| Attraction : has
    Activity ||--o| District : belongs_to
    HotelsAndRestaurant ||--o| District : belongs_to
    Transportation ||--o| District : belongs_to
    Attraction ||--o| District : belongs_to
    User ||--o| UserItinerary : has
    Itinerary ||--o| District : belongs_to
    Itinerary ||--o| Admin : created_by
    ItineraryActivity ||--o| Itinerary : includes
    ItineraryActivity ||--o| Activity : includes
    ItineraryHotelRestaurant ||--o| Itinerary : includes
    ItineraryHotelRestaurant ||--o| HotelsAndRestaurant : includes
    ItineraryTransportation ||--o| Itinerary : includes
    ItineraryTransportation ||--o| Transportation : includes
    ItineraryAttraction ||--o| Itinerary : includes
    ItineraryAttraction ||--o| Attraction : includes


```

---

## Models Overview

### **Category**
- **Purpose**: Represents different categories of items or topics.
- **Relationships**: 
  - Linked to `Admin` (who added the category).

### **Province**
- **Purpose**: Represents geographical provinces.
- **Relationships**: 
  - Has many `Districts`.

### **District**
- **Purpose**: Represents smaller geographical areas within a province.
- **Relationships**: 
  - Linked to `Province` (each district belongs to one province).
  - Has many `Activities`, `HotelsAndRestaurants`, `Transportation`, and `Attractions`.

### **Activity**
- **Purpose**: Represents various activities that can be done in a district.
- **Relationships**: 
  - Linked to `District` (each activity is in one district).
  - Associated with itineraries through `ItineraryActivity`.

### **HotelsAndRestaurant**
- **Purpose**: Represents hotels and restaurants in a district.
- **Relationships**: 
  - Linked to `District` (each hotel/restaurant is in one district).
  - Associated with itineraries through `ItineraryHotelRestaurant`.

### **Transportation**
- **Purpose**: Represents transportation options within a district.
- **Relationships**: 
  - Linked to `District` (each transportation option is in one district).
  - Associated with itineraries through `ItineraryTransportation`.

### **Attraction**
- **Purpose**: Represents tourist attractions in a district.
- **Relationships**: 
  - Linked to `District` (each attraction is in one district).
  - Associated with itineraries through `ItineraryAttraction`.

### **User**
- **Purpose**: Represents the users of the application.
- **Relationships**: 
  - Can have `UserItineraries` (if you choose to implement user-specific itineraries).

### **UserItinerary**
- **Purpose**: (Currently not used) Links users to itineraries, allowing users to have personal itineraries.
- **Relationships**: 
  - Linked to `User` (each itinerary belongs to a user).

### **Itinerary**
- **Purpose**: Represents a planned itinerary which includes activities, hotels/restaurants, transportation, and attractions for a specific district.
- **Relationships**: 
  - Linked to `District` (each itinerary is for one district).
  - Linked to `Admin` (each itinerary is created by an admin).
  - Has many `Activities`, `HotelsAndRestaurants`, `Transportations`, and `Attractions` through their respective models.

### **ItineraryActivity**
- **Purpose**: Links activities to specific itineraries.
- **Relationships**: 
  - Linked to `Itinerary` (each record associates an activity with an itinerary).
  - Linked to `Activity` (each record specifies which activity is included in the itinerary).

### **ItineraryHotelRestaurant**
- **Purpose**: Links hotels and restaurants to specific itineraries.
- **Relationships**: 
  - Linked to `Itinerary` (each record associates a hotel/restaurant with an itinerary).
  - Linked to `HotelsAndRestaurant` (each record specifies which hotel/restaurant is included in the itinerary).

### **ItineraryTransportation**
- **Purpose**: Links transportation options to specific itineraries.
- **Relationships**: 
  - Linked to `Itinerary` (each record associates a transportation option with an itinerary).
  - Linked to `Transportation` (each record specifies which transportation option is included in the itinerary).

### **ItineraryAttraction**
- **Purpose**: Links attractions to specific itineraries.
- **Relationships**: 
  - Linked to `Itinerary` (each record associates an attraction with an itinerary).
  - Linked to `Attraction` (each record specifies which attraction is included in the itinerary).

### **Admin**
- **Purpose**: Represents the administrators of the system.
- **Relationships**: 
  - Can manage `Categories`, `SubCategories`, and `Itineraries`.





