from typing import Dict, Any, List
from datetime import datetime, timedelta


# Tamil Nadu monsoon and risk calendar
TAMIL_NADU_CALENDAR = {
    1:  {"season": "Rabi",   "rainfall": "low",    "risk": "dry_spell",    "risk_label": "Dry Spell Risk"},
    2:  {"season": "Rabi",   "rainfall": "low",    "risk": "none",         "risk_label": "Stable"},
    3:  {"season": "Zaid",   "rainfall": "low",    "risk": "heat_stress",  "risk_label": "Heat Stress"},
    4:  {"season": "Zaid",   "rainfall": "low",    "risk": "heat_stress",  "risk_label": "Heat Stress"},
    5:  {"season": "Zaid",   "rainfall": "low",    "risk": "drought",      "risk_label": "Pre-Monsoon Drought"},
    6:  {"season": "Kharif", "rainfall": "medium", "risk": "fungal",       "risk_label": "Fungal Disease Risk"},
    7:  {"season": "Kharif", "rainfall": "high",   "risk": "flood",        "risk_label": "Flood Risk"},
    8:  {"season": "Kharif", "rainfall": "high",   "risk": "flood",        "risk_label": "Flood Risk"},
    9:  {"season": "Kharif", "rainfall": "medium", "risk": "fungal",       "risk_label": "Fungal Disease Risk"},
    10: {"season": "Kharif", "rainfall": "medium", "risk": "none",         "risk_label": "Good Conditions"},
    11: {"season": "Rabi",   "rainfall": "high",   "risk": "flood",        "risk_label": "NE Monsoon Flood Risk"},
    12: {"season": "Rabi",   "rainfall": "medium", "risk": "none",         "risk_label": "Stable"},
}

ACTIVITY_TEMPLATES = {
    "Germination": {"icon": "🌱", "color": "emerald"},
    "Land Preparation": {"icon": "🚜", "color": "amber"},
    "Sowing": {"icon": "🌾", "color": "green"},
    "Vegetative Growth": {"icon": "🌿", "color": "green"},
    "Flowering": {"icon": "🌸", "color": "pink"},
    "Grain Filling": {"icon": "🌽", "color": "yellow"},
    "Harvest": {"icon": "🏆", "color": "orange"},
    "Nutrient Application": {"icon": "💊", "color": "blue"},
    "Pest Monitoring": {"icon": "🔍", "color": "red"},
    "Irrigation": {"icon": "💧", "color": "cyan"},
    "Post-Harvest": {"icon": "📦", "color": "slate"},
}

RISK_COLORS = {
    "none": "green",
    "heat_stress": "orange",
    "drought": "red",
    "fungal": "yellow",
    "flood": "blue",
    "dry_spell": "amber",
}


class AgriculturalTimelineEngine:
    """
    Generates a 10-month farming activity calendar for a given farm and crop.
    Includes risk windows, activity milestones, and Tamil Nadu seasonal context.
    """

    def generate_timeline(
        self,
        crop_name: str,
        crop_total_days: int,
        farm_conditions: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generates a 10-month agricultural timeline starting from today.
        """
        today = datetime.now()
        months_data = []

        germination_days = 10
        growth_days = int(crop_total_days * 0.7)
        harvest_days = int(crop_total_days * 0.1)
        post_harvest_days = int(crop_total_days * 0.1)

        for i in range(10):
            target_date = today + timedelta(days=i * 30)
            month_num = target_date.month
            day_offset = i * 30

            cal = TAMIL_NADU_CALENDAR[month_num]
            risk_key = cal["risk"]

            # Determine crop activity for this month
            activities = self._get_activities_for_offset(
                day_offset, germination_days, growth_days, harvest_days, crop_name
            )

            months_data.append({
                "month_index": i,
                "month_label": target_date.strftime("%b %Y"),
                "season": cal["season"],
                "rainfall_level": cal["rainfall"],
                "risk_key": risk_key,
                "risk_label": cal["risk_label"],
                "risk_color": RISK_COLORS.get(risk_key, "green"),
                "activities": activities,
            })

        # Generate key milestones (important dates)
        milestones = self._generate_milestones(crop_name, crop_total_days, today)

        return {
            "crop_name": crop_name,
            "start_date": today.strftime("%b %d, %Y"),
            "end_date": (today + timedelta(days=300)).strftime("%b %d, %Y"),
            "months": months_data,
            "milestones": milestones,
        }

    def _get_activities_for_offset(
        self, day_offset: int, germ: int, growth: int, harvest: int, crop: str
    ) -> List[str]:
        """Determines farm activities for a given day offset."""
        activities = []
        if day_offset < germ:
            activities.extend(["Land Preparation", "Sowing"])
        elif day_offset < germ + growth * 0.3:
            activities.extend(["Germination", "Irrigation"])
        elif day_offset < germ + growth * 0.6:
            activities.extend(["Vegetative Growth", "Nutrient Application", "Irrigation"])
        elif day_offset < germ + growth * 0.85:
            activities.extend(["Flowering", "Pest Monitoring"])
        elif day_offset < germ + growth:
            activities.extend(["Grain Filling", "Irrigation"])
        elif day_offset < germ + growth + harvest:
            activities.extend(["Harvest"])
        else:
            activities.extend(["Post-Harvest", "Land Preparation"])
        return activities

    def _generate_milestones(self, crop: str, total_days: int, start: datetime) -> List[Dict[str, Any]]:
        """Key milestone events for the crop lifecycle."""
        milestones = [
            {"day": 0,              "label": f"Plant {crop}",            "type": "start"},
            {"day": 10,             "label": "First germination expected", "type": "info"},
            {"day": int(total_days * 0.35), "label": "Begin fertilizer schedule", "type": "action"},
            {"day": int(total_days * 0.65), "label": "Flowering stage — monitor pests", "type": "warning"},
            {"day": int(total_days * 0.85), "label": "Prepare harvesting equipment", "type": "action"},
            {"day": total_days,     "label": f"Harvest {crop}",           "type": "harvest"},
        ]
        for m in milestones:
            m["date"] = (start + timedelta(days=m["day"])).strftime("%b %d, %Y")
        return milestones


agricultural_timeline_engine = AgriculturalTimelineEngine()
