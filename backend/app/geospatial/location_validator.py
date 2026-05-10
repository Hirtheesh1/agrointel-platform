class LocationValidator:
    """
    Validates geospatial coordinates to ensure they fall within the supported region.
    Specifically, Tamil Nadu bounding box:
    Lat: ~8.0 to ~13.5 N
    Lon: ~76.2 to ~80.3 E
    """
    
    # Tamil Nadu Bounding Box
    MIN_LAT = 8.0
    MAX_LAT = 13.5
    MIN_LON = 76.2
    MAX_LON = 80.3

    @classmethod
    def is_valid_coordinate(cls, lat: float, lon: float) -> bool:
        """Checks if a point is within Tamil Nadu."""
        if not (cls.MIN_LAT <= lat <= cls.MAX_LAT):
            return False
        if not (cls.MIN_LON <= lon <= cls.MAX_LON):
            return False
        return True

    @classmethod
    def validate(cls, lat: float, lon: float):
        """Raises ValueError if outside bounds."""
        if not cls.is_valid_coordinate(lat, lon):
            raise ValueError(f"Coordinates ({lat}, {lon}) are outside the supported Tamil Nadu region.")

location_validator = LocationValidator()
