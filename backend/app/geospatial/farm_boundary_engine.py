import json
from typing import Dict, Any, Tuple

class FarmBoundaryEngine:
    """
    Parses and manages geospatial boundaries (GeoJSON polygons) or radius representations.
    Provides mathematical utilities since PostGIS is not yet active.
    """

    @classmethod
    def get_centroid(cls, geojson: Dict[str, Any]) -> Tuple[float, float]:
        """
        Calculates a simple centroid from a GeoJSON Polygon.
        Assumes standard GeoJSON: {'type': 'Polygon', 'coordinates': [[[lon, lat], ...]]}
        Returns (lat, lon)
        """
        try:
            if geojson.get("type") != "Polygon":
                raise ValueError("Only Polygon GeoJSON is currently supported for farm boundaries.")
            
            # Extract coordinates. GeoJSON format is [lon, lat]
            coords = geojson["coordinates"][0]
            
            sum_lon = sum(pt[0] for pt in coords)
            sum_lat = sum(pt[1] for pt in coords)
            num_points = len(coords)
            
            if num_points == 0:
                raise ValueError("Empty polygon.")
                
            return (sum_lat / num_points, sum_lon / num_points)
        except Exception as e:
            raise ValueError(f"Invalid GeoJSON: {str(e)}")

    @classmethod
    def haversine_distance(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on the earth (specified in decimal degrees)
        Returns distance in kilometers.
        """
        from math import radians, cos, sin, asin, sqrt

        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return c * r

farm_boundary_engine = FarmBoundaryEngine()
