import os
import django
import time
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tracker.settings')
django.setup()

from tracker.models import Bus

# Starting and ending coordinates for 3 buses
route_coords = {
    "01": ((24.3680579, 88.581936), (24.3631223, 88.6297615)),  # C&B More → RUET Main Gate
    "02": ((24.3631223, 88.6297615), (24.3659547, 88.6726807)),  # Ruet Main Gate → Katakhali Bus Stop
    "03": ((24.3797258, 88.5642949), (24.3631223, 88.6297615)),  # Rajshahi Court Railway → Vodra
}

# Get road-following path using OSRM API
def get_osrm_path(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
    res = requests.get(url)
    data = res.json()
    if "routes" not in data or not data["routes"]:
        print("Error:", data.get("message", "No route found"))
        return []
    coords = data["routes"][0]["geometry"]["coordinates"]
    return [(lat, lng) for lng, lat in coords]

# Build paths dictionary
paths = {}
for bus_id, (start, end) in route_coords.items():
    path = get_osrm_path(start, end)
    paths[bus_id] = path
    print(f"Bus {bus_id} path: {len(path)} points")

# Initialize bus index tracking
bus_state = {bus_id: {"i": 0, "forward": True} for bus_id in paths}

# Simulation loop
def simulate_osrm_buses():
    while True:
        for bus_id, path in paths.items():
            if not path:
                continue
            state = bus_state[bus_id]
            i = state["i"]
            forward = state["forward"]

            point = path[i]
            bus, _ = Bus.objects.get_or_create(number=bus_id)
            bus.current_lat, bus.current_lng = point
            bus.save()
            print(f"Bus {bus_id} at {point}")

            # Move to next point
            if forward:
                if i + 1 < len(path):
                    state["i"] += 1
                else:
                    state["forward"] = False
            else:
                if i - 1 >= 0:
                    state["i"] -= 1
                else:
                    state["forward"] = True

        time.sleep(5)

# Run the simulation
if __name__ == '__main__':
    simulate_osrm_buses()
