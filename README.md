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
        Integer user_itinerary_id FK
        Integer district_id FK
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
    UserItinerary ||--o| Itinerary : includes
    Itinerary ||--o| District : belongs_to
    Itinerary ||--o| UserItinerary : linked_to
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

## Models (Tables) Overview

### **Category**
- **Purpose**: Represents different categories of items or topics.
- **Fields**:
  - `id`: Integer (Primary Key)
  - `title`: String
  - `description`: String
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
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Can have `UserItineraries` (if you choose to implement user-specific itineraries).

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
  - `created_at`: TIMESTAMP
- **Relationships**: 
  - Can manage `Categories` and `Itineraries`.
