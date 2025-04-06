from fastapi import FastAPI
from fastapi.responses import JSONResponse
import google.generativeai as genai
import math
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from difflib import get_close_matches

# Configure Gemini API directly
GEMINI_API_KEY = "AIzaSyC8_NtFk-md14u-867Ws0hMmqiBVCV1cOk"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Predefined locations with name, latitude, and longitude
PREDEFINED_LOCATIONS = [
    {"name": "Udaipur Luxuria", "latitude": 24.57799888, "longitude": 73.68263271},
    {"name": "Udaipur", "latitude": 24.58145726, "longitude": 73.68223671},
    {"name": "Udaipur Verandah", "latitude": 24.58350565, "longitude": 73.68120777},
    {"name": "Jaipur", "latitude": 27.29124839, "longitude": 75.89630143},
    {"name": "Jaisalmer", "latitude": 27.20578572, "longitude": 70.85906998},
    {"name": "Jodhpur", "latitude": 26.30365556, "longitude": 73.03570908},
    {"name": "Agra", "latitude": 27.26156953, "longitude": 78.07524716},
    {"name": "Delhi", "latitude": 28.61257139, "longitude": 77.28423582},
    {"name": "Rishikesh Luxuria", "latitude": 30.13769036, "longitude": 78.32465767},
    {"name": "Rishikesh Riverside Resort", "latitude": 30.10216117, "longitude": 78.38458848},
    {"name": "Hostel Varanasi", "latitude": 25.2992622, "longitude": 82.99691388},
    {"name": "Goa Luxuria", "latitude": 15.6135195, "longitude": 73.75705228},
    {"name": "Koksar Luxuria", "latitude": 32.4357785, "longitude": 77.18518717},
    {"name": "Daman", "latitude": 20.41486263, "longitude": 72.83282455},
    {"name": "Panarpani Retreat", "latitude": 22.52805539, "longitude": 78.43116291},
    {"name": "Pushkar", "latitude": 26.48080513, "longitude": 74.5613783},
    {"name": "Khajuraho", "latitude": 24.84602104, "longitude": 79.93139381},
    {"name": "Manali", "latitude": 32.28818695, "longitude": 77.17702523},
    {"name": "Bhimtal Luxuria", "latitude": 29.36552248, "longitude": 79.53481747},
    {"name": "Srinagar", "latitude": 34.11547314, "longitude": 74.88701741},
    {"name": "Ranthambore Luxuria", "latitude": 26.05471373, "longitude": 76.42953726},
    {"name": "Coimbatore", "latitude": 11.02064612, "longitude": 76.96293531},
    {"name": "Shoja", "latitude": 31.56341267, "longitude": 77.36733331}
]

# Create a lookup dictionary for faster direct matching
LOCATION_LOOKUP = {loc["name"].lower(): loc for loc in PREDEFINED_LOCATIONS}
LOCATION_NAMES = [loc["name"].lower() for loc in PREDEFINED_LOCATIONS]

def normalize_location_with_gemini(query):
    """Use Gemini API to correct and normalize location names."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        I have a user query for a location in India that might have incorrect spelling: "{query}".
        
        Here is a list of valid locations in our database:
        {", ".join([loc["name"] for loc in PREDEFINED_LOCATIONS])}
        
        If the user query matches or is close to one of these locations, return that exact location name.
        If not, provide the correct spelling of the location if it's misspelled, or the closest matching city/town in India.
        
        Return ONLY the corrected location name with proper capitalization without any explanation or additional text.
        """
        
        response = model.generate_content(prompt)
        corrected_location = response.text.strip()
        return corrected_location
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fall back to fuzzy matching if LLM fails
        return find_fuzzy_match(query)

def find_fuzzy_match(query):
    """Find a fuzzy match for a location name using Python's difflib."""
    query_lower = query.lower()
    
    # Try direct match first
    if query_lower in LOCATION_LOOKUP:
        return LOCATION_LOOKUP[query_lower]["name"]
    
    # Use difflib for fuzzy matching
    matches = get_close_matches(query_lower, LOCATION_NAMES, n=1, cutoff=0.6)
    if matches:
        return LOCATION_LOOKUP[matches[0]]["name"]
    
    # If no good match, return original
    return query

def find_location_by_name(location_name):
    """Find a location in our predefined list by name (case-insensitive)."""
    # Exact match (case insensitive)
    location_lower = location_name.lower()
    if location_lower in LOCATION_LOOKUP:
        return LOCATION_LOOKUP[location_lower]
    
    # Try fuzzy matching
    matches = get_close_matches(location_lower, LOCATION_NAMES, n=1, cutoff=0.7)
    if matches:
        return LOCATION_LOOKUP[matches[0]]
    
    return None

def get_coordinates_geopy(location_name):
    """Get coordinates for a location using GeoPy with retry."""
    # First check if it's in our predefined locations
    match = find_location_by_name(location_name)
    if match:
        return (match["latitude"], match["longitude"])
    
    # If not in predefined locations, try geocoding
    geolocator = Nominatim(user_agent="location_distance_calculator/1.0")
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            location = geolocator.geocode(f"{location_name}, India", timeout=10)
            return (location.latitude, location.longitude) if location else (None, None)
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_attempts - 1:
                print(f"Geocoding error after {max_attempts} attempts: {e}")
                return (None, None)
            continue
        except Exception as e:
            print(f"Geocoding error: {e}")
            return (None, None)
    
    return (None, None)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points using Haversine formula."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.get("/nearby-locations")
async def find_nearby_locations(query: str):
    """Find locations within 50km of the query location."""
    # First, try to correct spelling using enhanced methods
    corrected_query = normalize_location_with_gemini(query)
    
    # Check if the corrected query is directly in our database
    direct_match = find_location_by_name(corrected_query)
    if direct_match:
        lat, lon = direct_match["latitude"], direct_match["longitude"]
    else:
        # If not in our database, try geocoding
        lat, lon = get_coordinates_geopy(corrected_query)
        
        # If geocoding fails, try the original query as last resort
        if not lat or not lon:
            direct_match_original = find_location_by_name(query)
            if direct_match_original:
                lat, lon = direct_match_original["latitude"], direct_match_original["longitude"]
            else:
                lat, lon = get_coordinates_geopy(query)
    
    # If all methods fail to get coordinates
    if not lat or not lon:
        close_matches = get_close_matches(query.lower(), LOCATION_NAMES, n=3, cutoff=0.5)
        suggestions = [LOCATION_LOOKUP[match]["name"] for match in close_matches] if close_matches else []
        
        return JSONResponse(content={
            "error": f"Could not find coordinates for location: {corrected_query}",
            "suggestions": suggestions if suggestions else ["Try another location name or check spelling"]
        }, status_code=400)
    
    # Calculate distances to all predefined locations
    results = []
    for loc in PREDEFINED_LOCATIONS:
        distance = haversine(lat, lon, loc["latitude"], loc["longitude"])
        if distance <= 50:  # Within 50km
            results.append({
                "name": loc["name"],
                "distance_km": round(distance, 2)
            })
    
    # Return response
    if not results:
        return JSONResponse(content={"message": "No locations found within 50km radius"})
    
    return JSONResponse(content={
        "query": query,
        "corrected_query": corrected_query,
        "query_coordinates": {"latitude": lat, "longitude": lon},
        "locations_within_50km": sorted(results, key=lambda x: x["distance_km"])
    })

@app.get("/list-locations")
async def list_all_locations():
    """List all predefined locations."""
    return JSONResponse(content={"locations": PREDEFINED_LOCATIONS})

# To run: uvicorn main:app --reload