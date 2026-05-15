"""
Heatmap engine adapted for API use (returns JSON data).
Generates hotspots along the Noida-Delhi corridor for realistic traffic visualization.
"""
import numpy as np


def generate_corridor_hotspots(num_spots=150):
    """Generate hotspots along the Sector 18 Noida → Akshardham Delhi corridor."""
    np.random.seed(42)
    points = []

    # Corridor waypoints (spread across the route area)
    corridor = [
        (28.5696, 77.3219),  # Sector 18 Noida
        (28.5750, 77.3125),  # Sector 15
        (28.5790, 77.3080),  # DND Entry
        (28.5870, 77.2960),  # DND Flyway
        (28.5990, 77.2790),  # Maharani Bagh
        (28.5700, 77.2780),  # Ashram Chowk
        (28.5530, 77.3130),  # Sector 37
        (28.5480, 77.2980),  # Kalindi Kunj
        (28.5610, 77.2810),  # Jasola
        (28.6030, 77.2770),  # Ring Road
        (28.6127, 77.2773),  # Akshardham
    ]

    for _ in range(num_spots):
        # Pick a random corridor point and scatter around it
        base = corridor[np.random.randint(0, len(corridor))]
        lat = base[0] + np.random.normal(0, 0.012)
        lng = base[1] + np.random.normal(0, 0.012)
        intensity = float(np.random.uniform(0.3, 1.0))
        points.append([round(lat, 6), round(lng, 6), round(intensity, 3)])

    return points


def get_heatmap_data(base_lat=28.5900, base_lng=77.2990):
    hotspots = generate_corridor_hotspots(num_spots=150)

    # Incidents placed at realistic locations along the routes
    incidents = [
        {"position": [28.5790, 77.3080], "label": "Heavy Congestion — DND Entry", "type": "congestion"},
        {"position": [28.5870, 77.2960], "label": "Accident on DND Flyway", "type": "accident"},
        {"position": [28.5480, 77.3060], "label": "Road Construction — Kalindi Kunj", "type": "construction"},
        {"position": [28.6000, 77.2900], "label": "Signal Malfunction — Mayur Vihar", "type": "signal"},
    ]

    return {
        "hotspots": hotspots,
        "incidents": incidents,
        "center": [28.5900, 77.2990],  # Center between Noida and Akshardham
    }
