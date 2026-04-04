import tkinter as tk
from tkinter import ttk
import math

#pillow for icon generation
try:
    from PIL import Image, ImageDraw, ImageTK
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

#the brains

SPEED_UNITS = {
    "m/s"           : 1.0,
    "km/h"          : 1 / 3.6,       # 1 km/h = 0.2778 m/s
    "mph"           : 0.44704,
    "ft/s"          : 0.3048,
    "knots"         : 0.514444,
}
 
LENGTH_UNITS = {
    "mm"            : 0.001,
    "cm"            : 0.01,
    "m"             : 1.0,
    "km"            : 1000.0,
    "inches"        : 0.0254,
    "feet"          : 0.3048,
    "yards"         : 0.9144,
    "miles"         : 1609.344,
}
 
MASS_UNITS = {
    "kg"            : 1.0,
    "g"             : 0.001,
    "mg"            : 0.000001,
    "metric ton"    : 1000.0,
    "pounds (lb)"   : 0.453592,
    "ounces (oz)"   : 0.0283495,
    "stone"         : 6.35029,
    "US ton"        : 907.185,
    "UK ton"        : 1016.05,
}
 
VOLUME_UNITS = {
    "litres (L)"    : 1.0,
    "mL"            : 0.001,
    "m³"            : 1000.0,
    "gallons (US)"  : 3.78541,
    "gallons (UK)"  : 4.54609,
    "pints (US)"    : 0.473176,
    "pints (UK)"    : 0.568261,
    "fl oz (US)"    : 0.0295735,
    "fl oz (UK)"    : 0.0284131,
    "cups (US)"     : 0.236588,
    "tbsp (US)"     : 0.0147868,
    "tsp (US)"      : 0.00492892,
}
 
AREA_UNITS = {
    "mm²"           : 0.000001,
    "cm²"           : 0.0001,
    "m²"            : 1.0,
    "km²"           : 1000000.0,
    "sq inches"     : 0.00064516,
    "sq feet"       : 0.092903,
    "sq yards"      : 0.836127,
    "sq miles"      : 2589988.11,
    "acres"         : 4046.86,
    "hectares"      : 10000.0,
}
 
FORCE_UNITS = {
    "Newtons (N)"   : 1.0,
    "kN"            : 1000.0,
    "pounds-force"  : 4.44822,
    "kgf"           : 9.80665,
    "dyne"          : 0.00001,
}
 
TEMPERATURE_UNITS = ["°C (Celsius)", "°F (Fahrenheit)", "K (Kelvin)"]
 
FUEL_UNITS = ["L/100km", "mpg (US)", "mpg (UK)", "km/L"]
 
ANGLE_UNITS = ["degrees", "radians", "gradians", "turns"]

