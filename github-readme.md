# Location Distance API

A FastAPI application that calculates distances between locations in India and finds nearby locations within a 50km radius.

## Features

- Find nearby locations within 50km of a query location
- Intelligent location name correction using Google's Gemini AI
- Fallback to fuzzy matching for location names
- Geocoding capabilities using GeoPy
- Pre-defined database of popular Indian locations

## Prerequisites

- Python 3.8+
- Google Gemini API key

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/location-distance-api.git
   cd location-distance-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Endpoints

### Find Nearby Locations

```
GET /nearby-locations?query={location_name}
```

Returns all locations within 50km radius of the query location.

#### Example Request:
```
GET /nearby-locations?query=Jaipur
```

#### Example Response:
```json
{
  "query": "Jaipur",
  "corrected_query": "Jaipur",
  "query_coordinates": {
    "latitude": 27.29124839,
    "longitude": 75.89630143
  },
  "locations_within_50km": [
    {
      "name": "Jaipur",
      "distance_km": 0.0
    }
  ]
}
```

### List All Locations

```
GET /list-locations
```

Returns all predefined locations in the database.

## Environment Variables

The application uses the following environment variables:

- `GEMINI_API_KEY`: API key for Google's Gemini AI

## Deployment

This application can be deployed to platforms like Heroku, Google Cloud Run, or AWS Lambda. Make sure to set the environment variables properly in your deployment environment.

## License

[MIT](LICENSE)
