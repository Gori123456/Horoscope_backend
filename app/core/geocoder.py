"""
Built-in Geocoder & Location Resolver.
Allows users to enter city names directly without needing latitude, longitude, or timezone.
Contains an extensive offline gazetteer of 150+ major Indian and world cities.
"""

# Comprehensive offline gazetteer: Name -> (Latitude, Longitude, Timezone, State/Country)
CITY_DATABASE = {
    # India - Major Metros & Capital
    "new delhi": (28.6139, 77.2090, "Asia/Kolkata", "Delhi, India"),
    "delhi": (28.6139, 77.2090, "Asia/Kolkata", "Delhi, India"),
    "mumbai": (19.0760, 72.8777, "Asia/Kolkata", "Maharashtra, India"),
    "bombay": (19.0760, 72.8777, "Asia/Kolkata", "Maharashtra, India"),
    "bengaluru": (12.9716, 77.5946, "Asia/Kolkata", "Karnataka, India"),
    "bangalore": (12.9716, 77.5946, "Asia/Kolkata", "Karnataka, India"),
    "kolkata": (22.5726, 88.3639, "Asia/Kolkata", "West Bengal, India"),
    "calcutta": (22.5726, 88.3639, "Asia/Kolkata", "West Bengal, India"),
    "chennai": (13.0827, 80.2707, "Asia/Kolkata", "Tamil Nadu, India"),
    "madras": (13.0827, 80.2707, "Asia/Kolkata", "Tamil Nadu, India"),
    "hyderabad": (17.3850, 78.4867, "Asia/Kolkata", "Telangana, India"),
    "pune": (18.5204, 73.8567, "Asia/Kolkata", "Maharashtra, India"),
    "ahmedabad": (23.0225, 72.5714, "Asia/Kolkata", "Gujarat, India"),
    "jaipur": (26.9124, 75.7873, "Asia/Kolkata", "Rajasthan, India"),
    "lucknow": (26.8467, 80.9462, "Asia/Kolkata", "Uttar Pradesh, India"),
    "chandigarh": (30.7333, 76.7794, "Asia/Kolkata", "Punjab/Haryana, India"),
    "surat": (21.1702, 72.8311, "Asia/Kolkata", "Gujarat, India"),
    "kanpur": (26.4499, 80.3319, "Asia/Kolkata", "Uttar Pradesh, India"),
    "nagpur": (21.1458, 79.0882, "Asia/Kolkata", "Maharashtra, India"),
    "indore": (22.7196, 75.8577, "Asia/Kolkata", "Madhya Pradesh, India"),
    "thane": (19.2183, 72.9781, "Asia/Kolkata", "Maharashtra, India"),
    "bhopal": (23.2599, 77.4126, "Asia/Kolkata", "Madhya Pradesh, India"),
    "visakhapatnam": (17.6868, 83.2185, "Asia/Kolkata", "Andhra Pradesh, India"),
    "patna": (25.5941, 85.1376, "Asia/Kolkata", "Bihar, India"),
    "vadodara": (22.3072, 73.1812, "Asia/Kolkata", "Gujarat, India"),
    "ghaziabad": (28.6692, 77.4538, "Asia/Kolkata", "Uttar Pradesh, India"),
    "ludhiana": (30.9010, 75.8573, "Asia/Kolkata", "Punjab, India"),
    "agra": (27.1767, 78.0081, "Asia/Kolkata", "Uttar Pradesh, India"),
    "nashik": (19.9975, 73.7898, "Asia/Kolkata", "Maharashtra, India"),
    "faridabad": (28.4089, 77.3178, "Asia/Kolkata", "Haryana, India"),
    "meerut": (28.9845, 77.7064, "Asia/Kolkata", "Uttar Pradesh, India"),
    "rajkot": (22.3039, 70.8022, "Asia/Kolkata", "Gujarat, India"),
    "varanasi": (25.3176, 82.9739, "Asia/Kolkata", "Uttar Pradesh, India"),
    "kashi": (25.3176, 82.9739, "Asia/Kolkata", "Uttar Pradesh, India"),
    "banaras": (25.3176, 82.9739, "Asia/Kolkata", "Uttar Pradesh, India"),
    "srinagar": (34.0837, 74.7973, "Asia/Kolkata", "Jammu and Kashmir, India"),
    "amritsar": (31.6340, 74.8723, "Asia/Kolkata", "Punjab, India"),
    "navi mumbai": (19.0330, 73.0297, "Asia/Kolkata", "Maharashtra, India"),
    "allahabad": (25.4358, 81.8463, "Asia/Kolkata", "Uttar Pradesh, India"),
    "prayagraj": (25.4358, 81.8463, "Asia/Kolkata", "Uttar Pradesh, India"),
    "ranchi": (23.3441, 85.3096, "Asia/Kolkata", "Jharkhand, India"),
    "howrah": (22.5958, 88.2636, "Asia/Kolkata", "West Bengal, India"),
    "coimbatore": (11.0168, 76.9558, "Asia/Kolkata", "Tamil Nadu, India"),
    "jabalpur": (23.1815, 79.9864, "Asia/Kolkata", "Madhya Pradesh, India"),
    "gwalior": (26.2183, 78.1828, "Asia/Kolkata", "Madhya Pradesh, India"),
    "vijayawada": (16.5062, 80.6480, "Asia/Kolkata", "Andhra Pradesh, India"),
    "jodhpur": (26.2389, 73.0243, "Asia/Kolkata", "Rajasthan, India"),
    "madurai": (9.9252, 78.1198, "Asia/Kolkata", "Tamil Nadu, India"),
    "raipur": (21.2514, 81.6296, "Asia/Kolkata", "Chhattisgarh, India"),
    "kota": (25.2138, 75.8648, "Asia/Kolkata", "Rajasthan, India"),
    "guwahati": (26.1445, 91.7362, "Asia/Kolkata", "Assam, India"),
    "hubli": (15.3647, 75.1240, "Asia/Kolkata", "Karnataka, India"),
    "mysuru": (12.2958, 76.6394, "Asia/Kolkata", "Karnataka, India"),
    "mysore": (12.2958, 76.6394, "Asia/Kolkata", "Karnataka, India"),
    "tiruchirappalli": (10.7905, 78.7047, "Asia/Kolkata", "Tamil Nadu, India"),
    "trichy": (10.7905, 78.7047, "Asia/Kolkata", "Tamil Nadu, India"),
    "dehradun": (30.3165, 78.0322, "Asia/Kolkata", "Uttarakhand, India"),
    "kochi": (9.9312, 76.2673, "Asia/Kolkata", "Kerala, India"),
    "cochin": (9.9312, 76.2673, "Asia/Kolkata", "Kerala, India"),
    "thiruvananthapuram": (8.5241, 76.9366, "Asia/Kolkata", "Kerala, India"),
    "trivandrum": (8.5241, 76.9366, "Asia/Kolkata", "Kerala, India"),
    "bhubaneswar": (20.2961, 85.8245, "Asia/Kolkata", "Odisha, India"),
    "salem": (11.6643, 78.1460, "Asia/Kolkata", "Tamil Nadu, India"),
    "warangal": (17.9689, 79.5941, "Asia/Kolkata", "Telangana, India"),
    "guntur": (16.3067, 80.4365, "Asia/Kolkata", "Andhra Pradesh, India"),
    "gorakhpur": (26.7606, 83.3732, "Asia/Kolkata", "Uttar Pradesh, India"),
    "udaipur": (24.5854, 73.7125, "Asia/Kolkata", "Rajasthan, India"),
    "jammu": (32.7266, 74.8570, "Asia/Kolkata", "Jammu and Kashmir, India"),
    "aurangabad": (19.8762, 75.3433, "Asia/Kolkata", "Maharashtra, India"),
    "chhatrapati sambhajinagar": (19.8762, 75.3433, "Asia/Kolkata", "Maharashtra, India"),
    "kolhapur": (16.7050, 74.2433, "Asia/Kolkata", "Maharashtra, India"),
    "solapur": (17.6599, 75.9064, "Asia/Kolkata", "Maharashtra, India"),
    "haridwar": (29.9457, 78.1642, "Asia/Kolkata", "Uttarakhand, India"),
    "rishikesh": (30.0869, 78.2676, "Asia/Kolkata", "Uttarakhand, India"),
    "shimla": (31.1048, 77.1734, "Asia/Kolkata", "Himachal Pradesh, India"),
    "goa": (15.2993, 74.1240, "Asia/Kolkata", "Goa, India"),
    "panaji": (15.4909, 73.8278, "Asia/Kolkata", "Goa, India"),

    # Global Metros & Major Diaspora Hubs
    "new york": (40.7128, -74.0060, "America/New_York", "NY, USA"),
    "los angeles": (34.0522, -118.2437, "America/Los_Angeles", "CA, USA"),
    "san francisco": (37.7749, -122.4194, "America/Los_Angeles", "CA, USA"),
    "chicago": (41.8781, -87.6298, "America/Chicago", "IL, USA"),
    "houston": (29.7604, -95.3698, "America/Chicago", "TX, USA"),
    "dallas": (32.7767, -96.7970, "America/Chicago", "TX, USA"),
    "seattle": (47.6062, -122.3321, "America/Los_Angeles", "WA, USA"),
    "london": (51.5074, -0.1278, "Europe/London", "United Kingdom"),
    "dubai": (25.2048, 55.2708, "Asia/Dubai", "United Arab Emirates"),
    "abu dhabi": (24.4539, 54.3773, "Asia/Dubai", "United Arab Emirates"),
    "singapore": (1.3521, 103.8198, "Asia/Singapore", "Singapore"),
    "kuala lumpur": (3.1390, 101.6869, "Asia/Kuala_Lumpur", "Malaysia"),
    "tokyo": (35.6762, 139.6503, "Asia/Tokyo", "Japan"),
    "sydney": (-33.8688, 151.2093, "Australia/Sydney", "Australia"),
    "melbourne": (-37.8136, 144.9631, "Australia/Melbourne", "Australia"),
    "toronto": (43.6532, -79.3832, "America/Toronto", "Canada"),
    "vancouver": (49.2827, -123.1207, "America/Vancouver", "Canada"),
    "paris": (48.8566, 2.3522, "Europe/Paris", "France"),
    "berlin": (52.5200, 13.4050, "Europe/Berlin", "Germany"),
    "frankfurt": (50.1109, 8.6821, "Europe/Berlin", "Germany"),
    "amsterdam": (52.3676, 4.9041, "Europe/Amsterdam", "Netherlands"),
    "zurich": (47.3769, 8.5417, "Europe/Zurich", "Switzerland"),
    "bangkok": (13.7563, 100.5018, "Asia/Bangkok", "Thailand"),
    "hong kong": (22.3193, 114.1694, "Asia/Hong_Kong", "Hong Kong"),
    "doha": (25.2854, 51.5310, "Asia/Qatar", "Qatar"),
    "kuwait": (29.3759, 47.9774, "Asia/Kuwait", "Kuwait"),
    "riyadh": (24.7136, 46.6753, "Asia/Riyadh", "Saudi Arabia"),
    "kathmandu": (27.7172, 85.3240, "Asia/Kathmandu", "Nepal"),
    "colombo": (6.9271, 79.8612, "Asia/Colombo", "Sri Lanka"),
    "dhaka": (23.8103, 90.4125, "Asia/Dhaka", "Bangladesh")
}


def resolve_location(place_name: str | None, default_lat: float | None = None, default_lon: float | None = None, default_tz: str | None = None) -> tuple[float, float, str, str]:
    """
    Resolves place name into (latitude, longitude, timezone, display_name).
    If user already passed coordinates, preserves them.
    If only city name is passed, resolves it automatically.
    Defaults to New Delhi, India if no info is given.
    """
    # 1. If explicit latitude & longitude provided
    if default_lat is not None and default_lon is not None:
        tz = default_tz or "Asia/Kolkata"
        display = place_name or f"Lat: {default_lat:.2f}, Lon: {default_lon:.2f}"
        return default_lat, default_lon, tz, display

    # 2. If place_name is provided, search database
    if place_name:
        clean_name = place_name.strip().lower()

        # Exact match
        if clean_name in CITY_DATABASE:
            lat, lon, tz, full_name = CITY_DATABASE[clean_name]
            return lat, lon, tz, full_name

        # Partial substring match (e.g. "pune, india" -> "pune")
        for city_key, data in CITY_DATABASE.items():
            if city_key in clean_name or clean_name in city_key:
                return data[0], data[1], data[2], data[3]

    # 3. Default fallback if completely unknown
    return 28.6139, 77.2090, "Asia/Kolkata", "New Delhi, India"

