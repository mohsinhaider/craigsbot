from shapely.geometry import Polygon, Point

from craigsbot.config import Configuration


def create_boundary() -> Polygon:
    coords = Configuration.COORDINATES.split(";")
    coord_pairs = []
    for coord in coords:
        lat, long = map(lambda c: float(c), coord.split(","))
        coord_pairs.append((lat, long))

    return Polygon(coord_pairs)


def is_coordinate_in_boundary(latitude: float, longitude: float, boundary: Polygon) -> bool:
    coordinate = Point(latitude, longitude)
    return boundary.contains(coordinate)
