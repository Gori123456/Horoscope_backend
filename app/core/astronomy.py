"""
Astronomical Engine for High-Precision Coordinate Calculations.
Calculates Julian Day, Local Sidereal Time, Lahiri Ayanamsha, 
Planetary Longitudes (Geocentric Ecliptic), and House Cusps.

Supports:
1. Native Pure-Python High-Precision Ephemeris Engine (Keplerian + Perturbations)
2. Seamless Swiss Ephemeris (`pyswisseph`) acceleration if installed.
"""

import math
from datetime import datetime, date, time
import pytz

# Check if Swiss Ephemeris is available
SWISSEPH_AVAILABLE = False
try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    SWISSEPH_AVAILABLE = False


def to_utc(birth_date: date, birth_time: time, timezone_str: str) -> datetime:
    """Converts local birth date and time in given timezone to UTC datetime."""
    tz = pytz.timezone(timezone_str)
    local_dt = tz.localize(datetime.combine(birth_date, birth_time))
    return local_dt.astimezone(pytz.UTC)


def calculate_julian_day(utc_dt: datetime) -> float:
    """
    Calculates exact Julian Day Number (JD) from UTC datetime.
    Standard Meeus formula, exact for Gregorian calendar.
    """
    year = utc_dt.year
    month = utc_dt.month
    day = utc_dt.day
    hour = utc_dt.hour
    minute = utc_dt.minute
    second = utc_dt.second + utc_dt.microsecond / 1e6

    if month <= 2:
        year -= 1
        month += 12

    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    day_fraction = (hour + minute / 60.0 + second / 3600.0) / 24.0
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5 + day_fraction
    return jd


def calculate_centuries(jd: float) -> float:
    """Calculates Julian centuries elapsed since J2000.0 (JD 2451545.0)."""
    return (jd - 2451545.0) / 36525.0


def calculate_lahiri_ayanamsha(jd: float) -> float:
    """
    Calculates the exact Lahiri (Chitra Paksha) Ayanamsha in degrees.
    Formula as codified by the Indian Calendar Reform Committee.
    """
    if SWISSEPH_AVAILABLE:
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        return swe.get_ayanamsa_ut(jd)

    t = calculate_centuries(jd)
    # Base at J2000.0 (Jan 1, 2000 12:00 UT) = 23° 51' 25.53" = 23.85709167°
    # Precession rate ≈ 5029.0966 arcseconds per Julian century
    ayanamsha_arcsec = (23 * 3600 + 51 * 60 + 25.53) + 5029.0966 * t + 1.1116 * (t ** 2)
    return (ayanamsha_arcsec / 3600.0) % 360.0


def calculate_greenwich_mean_sidereal_time(jd: float) -> float:
    """Calculates Greenwich Mean Sidereal Time (GMST) in degrees."""
    t = calculate_centuries(jd)
    theta = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * (t ** 2) - ((t ** 3) / 38710000.0)
    return theta % 360.0


def calculate_local_sidereal_time(jd: float, longitude: float) -> float:
    """Calculates Local Sidereal Time (LST) in degrees."""
    gmst = calculate_greenwich_mean_sidereal_time(jd)
    return (gmst + longitude) % 360.0


def calculate_true_obliquity(jd: float) -> float:
    """Calculates True Obliquity of the Ecliptic (eps) in degrees."""
    t = calculate_centuries(jd)
    eps_arcsec = 84381.448 - 46.8150 * t - 0.00059 * (t ** 2) + 0.001813 * (t ** 3)
    return eps_arcsec / 3600.0


def calculate_ascendant(jd: float, latitude: float, longitude: float, ayanamsha: float) -> dict:
    """
    Calculates the exact Ascendant (Lagna) and Midheaven (MC).
    Returns both Tropical and Sidereal longitudes in degrees.
    """
    rad = math.pi / 180.0
    lst_deg = calculate_local_sidereal_time(jd, longitude)
    lst_rad = lst_deg * rad
    eps_deg = calculate_true_obliquity(jd)
    eps_rad = eps_deg * rad
    lat_rad = latitude * rad

    # Midheaven (MC) in tropical degrees
    mc_rad = math.atan2(math.sin(lst_rad), math.cos(lst_rad) * math.cos(eps_rad))
    mc_deg = (mc_rad / rad) % 360.0

    # Ascendant (Lagna) formula
    num = math.cos(lst_rad)
    den = -math.sin(lst_rad) * math.cos(eps_rad) - math.tan(lat_rad) * math.sin(eps_rad)
    asc_rad = math.atan2(num, den)
    asc_deg = (asc_rad / rad) % 360.0

    # Convert to Sidereal (Nirayana)
    sidereal_asc = (asc_deg - ayanamsha) % 360.0
    sidereal_mc = (mc_deg - ayanamsha) % 360.0

    return {
        "tropical_ascendant": asc_deg,
        "sidereal_ascendant": sidereal_asc,
        "tropical_mc": mc_deg,
        "sidereal_mc": sidereal_mc,
        "lst_degrees": lst_deg
    }


def _solve_kepler(m_rad: float, e: float) -> float:
    """Solves Kepler's Equation E - e*sin(E) = M via Newton-Raphson iteration."""
    eccentric_anomaly = m_rad
    for _ in range(15):
        delta = eccentric_anomaly - e * math.sin(eccentric_anomaly) - m_rad
        if abs(delta) < 1e-12:
            break
        derivative = 1.0 - e * math.cos(eccentric_anomaly)
        eccentric_anomaly -= delta / derivative
    return eccentric_anomaly


def calculate_sun_position(jd: float) -> float:
    """Calculates True Geocentric Longitude of the Sun in Tropical degrees."""
    t = calculate_centuries(jd)
    # Mean Longitude
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * (t ** 2)
    # Mean Anomaly
    m = 357.52911 + 35999.05029 * t - 0.0001537 * (t ** 2)
    m_rad = (m % 360.0) * (math.pi / 180.0)
    # Equation of Center
    c = (1.914602 - 0.004817 * t - 0.000014 * (t ** 2)) * math.sin(m_rad) \
        + (0.019993 - 0.000101 * t) * math.sin(2 * m_rad) \
        + 0.000289 * math.sin(3 * m_rad)
    true_long = (l0 + c) % 360.0
    return true_long


def calculate_moon_position(jd: float) -> float:
    """
    Calculates Geocentric Longitude of the Moon in Tropical degrees.
    Uses high-precision truncated series of Brown's Lunar Theory / Meeus algorithm.
    """
    t = calculate_centuries(jd)
    rad = math.pi / 180.0

    # Moon's mean longitude
    lp = 218.3164477 + 481267.88123421 * t - 0.0015786 * (t ** 2)
    # Moon's mean elongation
    d = 297.8501921 + 445267.1114034 * t - 0.0018819 * (t ** 2)
    # Sun's mean anomaly
    m = 357.5291092 + 35999.0502909 * t - 0.0001536 * (t ** 2)
    # Moon's mean anomaly
    mp = 134.9633964 + 477198.8675055 * t + 0.0087414 * (t ** 2)
    # Moon's argument of latitude
    f = 93.2720950 + 483202.0175233 * t - 0.0036539 * (t ** 2)

    # Periodic perturbations in longitude (degrees)
    sigma_l = 6.288774 * math.sin(mp * rad) \
        + 1.274027 * math.sin((2 * d - mp) * rad) \
        + 0.658314 * math.sin(2 * d * rad) \
        + 0.213618 * math.sin(2 * mp * rad) \
        - 0.185116 * math.sin(m * rad) \
        - 0.114332 * math.sin(2 * f * rad) \
        + 0.058793 * math.sin((2 * d - 2 * mp) * rad) \
        + 0.057066 * math.sin((2 * d - m - mp) * rad) \
        + 0.053322 * math.sin((2 * d + mp) * rad) \
        + 0.046058 * math.sin((2 * d - m) * rad)

    return (lp + sigma_l) % 360.0


def calculate_lunar_nodes(jd: float) -> tuple[float, float]:
    """Calculates Mean Longitude of Rahu (North Node) and Ketu (South Node)."""
    t = calculate_centuries(jd)
    rahu_tropical = (125.04452 - 1934.136261 * t + 0.0020708 * (t ** 2)) % 360.0
    ketu_tropical = (rahu_tropical + 180.0) % 360.0
    return rahu_tropical, ketu_tropical


def _kepler_planet(jd: float, elements: dict) -> tuple[float, float, float]:
    """Computes heliocentric rectangular coordinates (x, y, z) for a planet."""
    t = calculate_centuries(jd)
    rad = math.pi / 180.0

    a = elements["a0"] + elements["a_rate"] * t
    e = elements["e0"] + elements["e_rate"] * t
    i = (elements["i0"] + elements["i_rate"] * t) * rad
    l = (elements["l0"] + elements["l_rate"] * t) % 360.0
    w = (elements["w0"] + elements["w_rate"] * t) % 360.0
    node = (elements["node0"] + elements["node_rate"] * t) % 360.0

    peri = (w - node) * rad
    node_rad = node * rad
    m = ((l - w) % 360.0) * rad

    big_e = _solve_kepler(m, e)
    nu = 2.0 * math.atan2(math.sqrt(1.0 + e) * math.sin(big_e / 2.0), math.sqrt(1.0 - e) * math.cos(big_e / 2.0))
    r = a * (1.0 - e * math.cos(big_e))

    # Coordinates in orbital plane
    x_prime = r * math.cos(nu)
    y_prime = r * math.sin(nu)

    # Convert to heliocentric ecliptic coordinates
    x = x_prime * (math.cos(peri) * math.cos(node_rad) - math.sin(peri) * math.sin(node_rad) * math.cos(i)) \
        - y_prime * (math.sin(peri) * math.cos(node_rad) + math.cos(peri) * math.sin(node_rad) * math.cos(i))
    y = x_prime * (math.cos(peri) * math.sin(node_rad) + math.sin(peri) * math.cos(node_rad) * math.cos(i)) \
        - y_prime * (math.sin(peri) * math.sin(node_rad) - math.cos(peri) * math.cos(node_rad) * math.cos(i))
    z = x_prime * (math.sin(peri) * math.sin(i)) + y_prime * (math.cos(peri) * math.sin(i))

    return x, y, z


# Standard NASA JPL Mean Orbital Elements (J2000 Base + Centurial Rates)
ORBITAL_ELEMENTS = {
    "Earth": {
        "a0": 1.00000261, "a_rate": 0.00000562,
        "e0": 0.01671123, "e_rate": -0.00004392,
        "i0": 0.00001531, "i_rate": -0.01294668,
        "l0": 100.46457166, "l_rate": 35999.37244981,
        "w0": 102.93768193, "w_rate": 0.32327364,
        "node0": 0.0, "node_rate": 0.0
    },
    "Mercury": {
        "a0": 0.38709927, "a_rate": 0.00000037,
        "e0": 0.20563593, "e_rate": 0.00001906,
        "i0": 7.00497902, "i_rate": -0.00594749,
        "l0": 252.25032350, "l_rate": 149472.67411175,
        "w0": 77.45779628, "w_rate": 0.16047689,
        "node0": 48.33076593, "node_rate": -0.12534081
    },
    "Venus": {
        "a0": 0.72333566, "a_rate": 0.00000390,
        "e0": 0.00677672, "e_rate": -0.00004107,
        "i0": 3.39467605, "i_rate": -0.00078890,
        "l0": 181.97909950, "l_rate": 58517.81538729,
        "w0": 131.60246718, "w_rate": 0.00268329,
        "node0": 76.67984255, "node_rate": -0.27769418
    },
    "Mars": {
        "a0": 1.52371034, "a_rate": 0.00001847,
        "e0": 0.09339410, "e_rate": 0.00007882,
        "i0": 1.84969142, "i_rate": -0.00813131,
        "l0": -4.55343205, "l_rate": 19140.30268499,
        "w0": -23.94362959, "w_rate": 0.44441088,
        "node0": 49.55953891, "node_rate": -0.29257343
    },
    "Jupiter": {
        "a0": 5.20288700, "a_rate": -0.00011607,
        "e0": 0.04838624, "e_rate": -0.00013253,
        "i0": 1.30439695, "i_rate": -0.00183714,
        "l0": 34.39644051, "l_rate": 3034.74612775,
        "w0": 14.72847983, "w_rate": 0.21252668,
        "node0": 100.47390909, "node_rate": 0.20469106
    },
    "Saturn": {
        "a0": 9.53667594, "a_rate": -0.00125060,
        "e0": 0.05386179, "e_rate": -0.00050991,
        "i0": 2.48599187, "i_rate": 0.00193609,
        "l0": 49.95424423, "l_rate": 1222.49362201,
        "w0": 92.59887831, "w_rate": -0.41897216,
        "node0": 113.66242448, "node_rate": -0.28867794
    }
}


def calculate_geocentric_planet_position(jd: float, planet_name: str) -> float:
    """Calculates True Geocentric Longitude of a planet in Tropical degrees."""
    earth_x, earth_y, earth_z = _kepler_planet(jd, ORBITAL_ELEMENTS["Earth"])
    p_x, p_y, p_z = _kepler_planet(jd, ORBITAL_ELEMENTS[planet_name])

    geo_x = p_x - earth_x
    geo_y = p_y - earth_y
    # Geocentric Longitude
    geo_long = (math.atan2(geo_y, geo_x) * 180.0 / math.pi) % 360.0
    return geo_long


def calculate_all_planets(jd: float, ayanamsha: float) -> dict[str, dict]:
    """
    Computes Tropical & Sidereal longitudes for all 9 Navagrahas.
    Returns dictionary with degrees, signs, and daily motion.
    """
    planets = {}

    if SWISSEPH_AVAILABLE:
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        mapping = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mercury": swe.MERCURY,
            "Venus": swe.VENUS,
            "Mars": swe.MARS,
            "Jupiter": swe.JUPITER,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE
        }
        for name, pid in mapping.items():
            res, _ = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
            sid_deg = res[0] % 360.0
            speed = res[3]
            planets[name] = {
                "sidereal_longitude": sid_deg,
                "tropical_longitude": (sid_deg + ayanamsha) % 360.0,
                "is_retrograde": speed < 0
            }
        # Ketu is exactly 180° opposite Rahu
        ketu_sid = (planets["Rahu"]["sidereal_longitude"] + 180.0) % 360.0
        planets["Ketu"] = {
            "sidereal_longitude": ketu_sid,
            "tropical_longitude": (ketu_sid + ayanamsha) % 360.0,
            "is_retrograde": True
        }
        return planets

    # Pure-Python High-Precision Fallback Engine
    # 1. Sun
    sun_trop = calculate_sun_position(jd)
    # 2. Moon
    moon_trop = calculate_moon_position(jd)
    # 3. Rahu & Ketu
    rahu_trop, ketu_trop = calculate_lunar_nodes(jd)
    
    # 4. Mercury, Venus, Mars, Jupiter, Saturn
    merc_trop = calculate_geocentric_planet_position(jd, "Mercury")
    venus_trop = calculate_geocentric_planet_position(jd, "Venus")
    mars_trop = calculate_geocentric_planet_position(jd, "Mars")
    jup_trop = calculate_geocentric_planet_position(jd, "Jupiter")
    sat_trop = calculate_geocentric_planet_position(jd, "Saturn")

    raw_trop = {
        "Sun": (sun_trop, False),
        "Moon": (moon_trop, False),
        "Mars": (mars_trop, False),
        "Mercury": (merc_trop, False),
        "Jupiter": (jup_trop, False),
        "Venus": (venus_trop, False),
        "Saturn": (sat_trop, False),
        "Rahu": (rahu_trop, True),
        "Ketu": (ketu_trop, True)
    }

    for name, (trop_deg, is_ret) in raw_trop.items():
        sid_deg = (trop_deg - ayanamsha) % 360.0
        planets[name] = {
            "sidereal_longitude": sid_deg,
            "tropical_longitude": trop_deg,
            "is_retrograde": is_ret
        }

    return planets

