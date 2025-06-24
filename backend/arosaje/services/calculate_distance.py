from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meter
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def move_latitude(lat: float, meters_north: int) -> float:
    delta_lat = meters_north / 111320
    return lat + delta_lat

def move_longitude(lat: float, lon: float, meters_east: int) -> float:
    delta_lon = meters_east / (111320 * cos(radians(lat)))
    return lon + delta_lon
