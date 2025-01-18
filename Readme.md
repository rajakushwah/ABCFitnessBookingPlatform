# Studio Class Booking API

## Overview
This API allows studio owners to create classes and enables members to book classes.

## Endpoints

### Create a Class
- **POST /classes**
- Request Body:
    ```json
    {
        "class_name": "Yoga",
        "start_date": "2025-01-20",
        "end_date": "2025-01-21",
        "capacity": 10
    }
    ```
- Success Response:
    - **Status:** `201 Created`
    - **Body:** 
    ```json
    {
        "message": "Class created successfully!"
    }
    ```

### Book a Class
- **POST /bookings**
- Request Body:
    ```json
    {
        "name": "John Doe",
        "date": "2025-01-15",
        "class_name": "Yoga"
    }
    ```
- Success Response:
    - **Status:** `201 Created`
    - **Body:**
    ```json
    {
        "message": "Booking successful!"
    }
    ```
- Error Response (Class Not Found):
    - **Status:** `404 Not Found`
    - **Body:**
    ```json
    {
        "error": "Class not found on this date."
    }
    ```



## Requirements
- Python 3.x
- Flask

## Setup
1. Install the required packages:
    ```bash
    pip install Flask
    ```

2. Run the application:
    ```bash
    python app.py
    ```

3. Use the postman collection name "fitness_app_collection "to test the endpoints.
