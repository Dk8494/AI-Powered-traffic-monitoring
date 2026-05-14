import googlemaps
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_directions(api_key, origin, destination):
    """
    Fetches driving directions and alternative routes from Google Maps API.
    
    Args:
        api_key (str): Google Maps API Key
        origin (str): Source location address or coordinates
        destination (str): Destination address or coordinates
        
    Returns:
        list: A list of parsed route dictionaries containing:
            - summary
            - distance
            - duration
            - duration_in_traffic (if available)
    """
    if not api_key:
        logger.error("No API key provided.")
        return []
        
    try:
        gmaps = googlemaps.Client(key=api_key)
        
        # Request directions (with alternatives) and departure time for traffic estimation
        now = datetime.now()
        directions_result = gmaps.directions(
            origin,
            destination,
            mode="driving",
            alternatives=True,
            departure_time=now
        )
        
        if not directions_result:
            logger.warning("No routes found between the provided locations.")
            return []
            
        parsed_routes = []
        for i, route in enumerate(directions_result):
            leg = route['legs'][0] # usually a single leg for simple A to B
            
            route_info = {
                "route_number": i + 1,
                "summary": route.get("summary", "Unnamed Route"),
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
            }
            
            # duration_in_traffic is only returned if departure_time is provided
            if "duration_in_traffic" in leg:
                route_info["traffic_time"] = leg["duration_in_traffic"]["text"]
            else:
                route_info["traffic_time"] = "Not available"
                
            parsed_routes.append(route_info)
            
        return parsed_routes
        
    except Exception as e:
        logger.error(f"Failed to fetch directions from Google Maps API: {e}")
        return []

if __name__ == "__main__":
    # Example usage for testing standalone
    # Replace 'YOUR_API_KEY' with an actual key to run
    TEST_API_KEY = "YOUR_API_KEY"
    src = "San Francisco, CA"
    dst = "San Jose, CA"
    
    print(f"Fetching routes from {src} to {dst}...")
    routes = fetch_directions(TEST_API_KEY, src, dst)
    
    if routes:
        print("\n--- Available Routes ---")
        for r in routes:
            print(f"\nRoute {r['route_number']}: {r['summary']}")
            print(f"Distance: {r['distance']}")
            print(f"Typical Duration: {r['duration']}")
            print(f"Duration w/ Traffic: {r['traffic_time']}")
    else:
        print("No routes could be fetched. Ensure your API key is valid.")
