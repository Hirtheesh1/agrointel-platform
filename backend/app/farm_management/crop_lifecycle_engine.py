# Tamil Nadu Crop Lifecycle Engine
# Encodes agricultural knowledge for 35+ Tamil Nadu crops

from typing import Dict, Any, List

# Tamil Nadu Agricultural Seasons
# Kharif (Samba):  June - November  (SW Monsoon)
# Rabi (Navarai):  December - March (NE Monsoon)
# Zaid (Kuruvai):  March - June     (Summer)
# Perennial: Year-round

TAMIL_NADU_CROPS: Dict[str, Dict[str, Any]] = {
    "paddy_samba": {
        "display_name": "Paddy (Samba)",
        "season": "kharif",
        "germination_days": 5,
        "growth_days": 120,
        "harvest_days": 10,
        "total_days": 135,
        "soil_ph_min": 5.5,
        "soil_ph_max": 7.0,
        "rainfall_min_mm": 1000,
        "rainfall_max_mm": 2000,
        "temp_min_c": 20,
        "temp_max_c": 38,
        "water_need_mm_day": 8.0,
        "nitrogen_need": "high",      # >150 kg/ha
        "phosphorus_need": "medium",
        "potassium_need": "medium",
        "drought_tolerance": "low",
        "yield_range_tons": (4.0, 6.5),
        "districts": ["Thanjavur", "Tiruvarur", "Nagapattinam", "Cuddalore"],
    },
    "paddy_kuruvai": {
        "display_name": "Paddy (Kuruvai)",
        "season": "zaid",
        "germination_days": 5,
        "growth_days": 85,
        "harvest_days": 10,
        "total_days": 100,
        "soil_ph_min": 5.5,
        "soil_ph_max": 7.0,
        "rainfall_min_mm": 800,
        "rainfall_max_mm": 1500,
        "temp_min_c": 22,
        "temp_max_c": 40,
        "water_need_mm_day": 9.0,
        "nitrogen_need": "high",
        "phosphorus_need": "medium",
        "potassium_need": "medium",
        "drought_tolerance": "low",
        "yield_range_tons": (3.5, 5.5),
        "districts": ["Thanjavur", "Tiruvarur", "Tiruchirappalli"],
    },
    "groundnut": {
        "display_name": "Groundnut",
        "season": "kharif",
        "germination_days": 7,
        "growth_days": 100,
        "harvest_days": 15,
        "total_days": 122,
        "soil_ph_min": 6.0,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 500,
        "rainfall_max_mm": 1250,
        "temp_min_c": 22,
        "temp_max_c": 38,
        "water_need_mm_day": 4.5,
        "nitrogen_need": "low",
        "phosphorus_need": "high",
        "potassium_need": "high",
        "drought_tolerance": "medium",
        "yield_range_tons": (1.5, 3.0),
        "districts": ["Vellore", "Villupuram", "Coimbatore", "Tirunelveli"],
    },
    "sugarcane": {
        "display_name": "Sugarcane",
        "season": "perennial",
        "germination_days": 20,
        "growth_days": 330,
        "harvest_days": 30,
        "total_days": 380,
        "soil_ph_min": 6.0,
        "soil_ph_max": 8.0,
        "rainfall_min_mm": 1200,
        "rainfall_max_mm": 2500,
        "temp_min_c": 18,
        "temp_max_c": 38,
        "water_need_mm_day": 7.0,
        "nitrogen_need": "high",
        "phosphorus_need": "medium",
        "potassium_need": "high",
        "drought_tolerance": "medium",
        "yield_range_tons": (70.0, 110.0),
        "districts": ["Coimbatore", "Erode", "Tiruchirappalli", "Thanjavur"],
    },
    "cotton": {
        "display_name": "Cotton",
        "season": "kharif",
        "germination_days": 8,
        "growth_days": 150,
        "harvest_days": 30,
        "total_days": 188,
        "soil_ph_min": 6.0,
        "soil_ph_max": 8.0,
        "rainfall_min_mm": 600,
        "rainfall_max_mm": 1200,
        "temp_min_c": 20,
        "temp_max_c": 40,
        "water_need_mm_day": 5.5,
        "nitrogen_need": "medium",
        "phosphorus_need": "medium",
        "potassium_need": "medium",
        "drought_tolerance": "medium",
        "yield_range_tons": (1.5, 2.5),
        "districts": ["Coimbatore", "Salem", "Virudhunagar", "Ramanathapuram"],
    },
    "banana": {
        "display_name": "Banana",
        "season": "perennial",
        "germination_days": 0,
        "growth_days": 270,
        "harvest_days": 30,
        "total_days": 300,
        "soil_ph_min": 5.5,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 1000,
        "rainfall_max_mm": 2500,
        "temp_min_c": 20,
        "temp_max_c": 38,
        "water_need_mm_day": 7.5,
        "nitrogen_need": "high",
        "phosphorus_need": "low",
        "potassium_need": "high",
        "drought_tolerance": "low",
        "yield_range_tons": (25.0, 40.0),
        "districts": ["Theni", "Erode", "Tiruchirappalli", "Dindigul"],
    },
    "turmeric": {
        "display_name": "Turmeric",
        "season": "kharif",
        "germination_days": 30,
        "growth_days": 240,
        "harvest_days": 20,
        "total_days": 290,
        "soil_ph_min": 5.5,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 1000,
        "rainfall_max_mm": 2000,
        "temp_min_c": 20,
        "temp_max_c": 35,
        "water_need_mm_day": 5.0,
        "nitrogen_need": "medium",
        "phosphorus_need": "medium",
        "potassium_need": "medium",
        "drought_tolerance": "medium",
        "yield_range_tons": (15.0, 25.0),
        "districts": ["Erode", "Salem", "Coimbatore", "Namakkal"],
    },
    "tomato": {
        "display_name": "Tomato",
        "season": "rabi",
        "germination_days": 7,
        "growth_days": 70,
        "harvest_days": 30,
        "total_days": 107,
        "soil_ph_min": 5.5,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 400,
        "rainfall_max_mm": 1200,
        "temp_min_c": 15,
        "temp_max_c": 32,
        "water_need_mm_day": 4.0,
        "nitrogen_need": "high",
        "phosphorus_need": "high",
        "potassium_need": "medium",
        "drought_tolerance": "low",
        "yield_range_tons": (20.0, 35.0),
        "districts": ["Dharmapuri", "Krishnagiri", "Salem", "Dindigul"],
    },
    "onion": {
        "display_name": "Onion",
        "season": "rabi",
        "germination_days": 8,
        "growth_days": 100,
        "harvest_days": 10,
        "total_days": 118,
        "soil_ph_min": 6.0,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 350,
        "rainfall_max_mm": 750,
        "temp_min_c": 12,
        "temp_max_c": 28,
        "water_need_mm_day": 3.5,
        "nitrogen_need": "medium",
        "phosphorus_need": "medium",
        "potassium_need": "high",
        "drought_tolerance": "high",
        "yield_range_tons": (15.0, 25.0),
        "districts": ["Perambalur", "Erode", "Salem", "Cuddalore"],
    },
    "maize": {
        "display_name": "Maize",
        "season": "kharif",
        "germination_days": 6,
        "growth_days": 90,
        "harvest_days": 10,
        "total_days": 106,
        "soil_ph_min": 5.8,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 500,
        "rainfall_max_mm": 1200,
        "temp_min_c": 18,
        "temp_max_c": 38,
        "water_need_mm_day": 5.5,
        "nitrogen_need": "high",
        "phosphorus_need": "medium",
        "potassium_need": "medium",
        "drought_tolerance": "medium",
        "yield_range_tons": (4.0, 7.0),
        "districts": ["Dharmapuri", "Salem", "Erode", "Coimbatore"],
    },
    "blackgram": {
        "display_name": "Black Gram (Urad)",
        "season": "rabi",
        "germination_days": 5,
        "growth_days": 65,
        "harvest_days": 10,
        "total_days": 80,
        "soil_ph_min": 5.5,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 300,
        "rainfall_max_mm": 900,
        "temp_min_c": 20,
        "temp_max_c": 38,
        "water_need_mm_day": 3.5,
        "nitrogen_need": "low",
        "phosphorus_need": "medium",
        "potassium_need": "low",
        "drought_tolerance": "high",
        "yield_range_tons": (0.8, 1.5),
        "districts": ["Vellore", "Villupuram", "Cuddalore", "Tirunelveli"],
    },
    "chilli": {
        "display_name": "Chilli",
        "season": "kharif",
        "germination_days": 8,
        "growth_days": 120,
        "harvest_days": 30,
        "total_days": 158,
        "soil_ph_min": 6.0,
        "soil_ph_max": 7.5,
        "rainfall_min_mm": 500,
        "rainfall_max_mm": 1200,
        "temp_min_c": 20,
        "temp_max_c": 35,
        "water_need_mm_day": 4.0,
        "nitrogen_need": "medium",
        "phosphorus_need": "medium",
        "potassium_need": "medium",
        "drought_tolerance": "medium",
        "yield_range_tons": (2.0, 4.0),
        "districts": ["Ramanathapuram", "Virudhunagar", "Salem", "Dindigul"],
    },
    "coconut": {
        "display_name": "Coconut",
        "season": "perennial",
        "germination_days": 90,
        "growth_days": 1825,
        "harvest_days": 0,
        "total_days": 1825,
        "soil_ph_min": 5.5,
        "soil_ph_max": 8.0,
        "rainfall_min_mm": 750,
        "rainfall_max_mm": 2500,
        "temp_min_c": 20,
        "temp_max_c": 38,
        "water_need_mm_day": 5.0,
        "nitrogen_need": "medium",
        "phosphorus_need": "low",
        "potassium_need": "high",
        "drought_tolerance": "medium",
        "yield_range_tons": (12.0, 20.0),
        "districts": ["Coimbatore", "Erode", "Thanjavur", "Tirunelveli"],
    },
    "sesame": {
        "display_name": "Sesame (Gingelly)",
        "season": "zaid",
        "germination_days": 5,
        "growth_days": 75,
        "harvest_days": 10,
        "total_days": 90,
        "soil_ph_min": 5.5,
        "soil_ph_max": 8.0,
        "rainfall_min_mm": 300,
        "rainfall_max_mm": 1000,
        "temp_min_c": 22,
        "temp_max_c": 40,
        "water_need_mm_day": 3.0,
        "nitrogen_need": "low",
        "phosphorus_need": "medium",
        "potassium_need": "low",
        "drought_tolerance": "high",
        "yield_range_tons": (0.5, 1.0),
        "districts": ["Tirunelveli", "Ramanathapuram", "Virudhunagar", "Thoothukudi"],
    },
}


class CropLifecycleEngine:
    """
    Models crop lifecycle stages and matches farm conditions to crop requirements.
    """

    def get_all_crops(self) -> Dict[str, Dict[str, Any]]:
        return TAMIL_NADU_CROPS

    def get_crop(self, crop_key: str) -> Dict[str, Any]:
        return TAMIL_NADU_CROPS.get(crop_key, {})

    def get_current_season(self) -> str:
        """Returns current Tamil Nadu agricultural season based on month."""
        from datetime import datetime
        month = datetime.now().month
        if 6 <= month <= 11:
            return "kharif"
        elif month in [12, 1, 2, 3]:
            return "rabi"
        else:
            return "zaid"

    def get_growth_stage(self, crop_key: str, days_planted: int) -> str:
        """Returns current growth stage for a crop given days since planting."""
        crop = self.get_crop(crop_key)
        if not crop:
            return "Unknown"
        germ = crop.get("germination_days", 10)
        growth = germ + crop.get("growth_days", 90)
        total = growth + crop.get("harvest_days", 10)
        if days_planted < germ:
            return "Germination"
        elif days_planted < germ + (growth - germ) * 0.4:
            return "Vegetative"
        elif days_planted < germ + (growth - germ) * 0.8:
            return "Flowering"
        elif days_planted < growth:
            return "Grain Filling"
        elif days_planted < total:
            return "Harvest Ready"
        return "Post-Harvest"

    def match_crop_to_farm(self, crop_key: str, farm_conditions: Dict[str, Any]) -> float:
        """
        Returns a 0-1 suitability score for a crop based on farm conditions.
        """
        crop = self.get_crop(crop_key)
        if not crop:
            return 0.0

        scores = []

        # pH score
        ph = farm_conditions.get("ph_level", 6.5)
        if crop["soil_ph_min"] <= ph <= crop["soil_ph_max"]:
            scores.append(1.0)
        else:
            deviation = min(abs(ph - crop["soil_ph_min"]), abs(ph - crop["soil_ph_max"]))
            scores.append(max(0.0, 1.0 - deviation * 0.3))

        # Temperature score
        temp = farm_conditions.get("avg_temperature", 30.0)
        if crop["temp_min_c"] <= temp <= crop["temp_max_c"]:
            scores.append(1.0)
        else:
            deviation = min(abs(temp - crop["temp_min_c"]), abs(temp - crop["temp_max_c"]))
            scores.append(max(0.0, 1.0 - deviation * 0.05))

        # Season score
        current_season = self.get_current_season()
        if crop["season"] == current_season or crop["season"] == "perennial":
            scores.append(1.0)
        else:
            scores.append(0.3)  # Off-season penalty

        # Water availability score
        water = farm_conditions.get("water_availability", 50.0)
        water_need = crop["water_need_mm_day"] * farm_conditions.get("farm_size", 1.0)
        if water >= water_need:
            scores.append(1.0)
        else:
            scores.append(max(0.0, water / max(water_need, 1)))

        return round(sum(scores) / len(scores), 3)


crop_lifecycle_engine = CropLifecycleEngine()
