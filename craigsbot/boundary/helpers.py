import os

from shapely.geometry import Polygon, Point

from craigsbot.config import Configuration


def create_boundaries() -> list[Polygon]:
    boundaries = []
    i = 0
    # 0 -> Cow Hollow
    # 1 -> Mission
    # 2 -> Hayes Valley
    while True:
        coord_pairs = []
        coords = os.environ.get(f"COORDINATES_{i}")
        if not coords:
            break
        for coord in coords.split(";"):
            lat, long = map(lambda c: float(c), coord.split(","))
            coord_pairs.append((lat, long,))
        boundaries.append(Polygon(coord_pairs))
        i += 1

    return boundaries


def is_coordinate_in_boundary(latitude: float, longitude: float, boundary: Polygon) -> bool:
    coordinate = Point(latitude, longitude)
    return boundary.contains(coordinate)
