# Location Distance API

A FastAPI application that calculates distances between locations in India and finds nearby locations within a 50km radius.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/binny1446/formi.git
   cd formi
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
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

## Environment Variables

The application uses the following environment variables:

- `GEMINI_API_KEY`: API key for Google's Gemini AI

