import tkinter as tk
from tkinter import ttk, messagebox
import math
import os
import sys

#pillow for icon generation
try:
    from PIL import Image, ImageDraw, ImageFont,
ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

#the brains

class ConversionEngine:

    # Speed  (base: m/s)
    SPEED = {
        "m/s":          1.0,
        "km/h":         1 / 3.6,
        "mph":          0.44704,
        "ft/s":         0.3048,
        "knots":        0.514444,
        "Mach (sea lvl)": 340.29,
    }
 
    # Length  (base: metres)
    LENGTH = {
        "mm":           0.001,
        "cm":           0.01,
        "m":            1.0,
        "km":           1000.0,
        "in":           0.0254,
        "ft":           0.3048,
        "yd":           0.9144,
        "mi":           1609.344,
        "nautical mi":  1852.0,
        "light-year":   9.461e15,
        "AU":           1.496e11,
    }
 
    # Mass  (base: kg)
    MASS = {
        "kg":           1.0,
        "g":            0.001,
        "mg":           1e-6,
        "t (metric)":   1000.0,
        "lb":           0.453592,
        "oz":           0.0283495,
        "stone":        6.35029,
        "ton (US)":     907.185,
        "ton (UK)":     1016.05,
    }
 
    # Volume  (base: litres)
    VOLUME = {
        "L":            1.0,
        "mL":           0.001,
        "m³":           1000.0,
        "cm³":          0.001,
        "gal (US)":     3.78541,
        "gal (UK)":     4.54609,
        "qt (US)":      0.946353,
        "qt (UK)":      1.13652,
        "pt (US)":      0.473176,
        "pt (UK)":      0.568261,
        "fl oz (US)":   0.0295735,
        "fl oz (UK)":   0.0284131,
        "cup (US)":     0.236588,
        "cup (UK)":     0.284131,
        "tbsp (US)":    0.0147868,
        "tsp (US)":     0.00492892,
    }
 
    # Area  (base: m²)
    AREA = {
        "mm²":          1e-6,
        "cm²":          0.0001,
        "m²":           1.0,
        "km²":          1e6,
        "in²":          0.00064516,
        "ft²":          0.092903,
        "yd²":          0.836127,
        "mi²":          2589988.11,
        "acre":         4046.86,
        "hectare":      10000.0,
    }
 
    # Force  (base: Newton)
    FORCE = {
        "N":            1.0,
        "kN":           1000.0,
        "MN":           1e6,
        "lbf":          4.44822,
        "kgf":          9.80665,
        "dyne":         1e-5,
        "poundal":      0.138255,
        "ton-force (US)": 8896.44,
    }

# Fuel Economy — special: L/100km is inverse-proportional to mpg
    FUEL_UNITS = ["L/100km", "mpg (US)", "mpg (UK)", "km/L"]
 
    # Temperature units
    TEMP_UNITS = ["°C", "°F", "K", "°R"]
 
    # Angle units
    ANGLE_UNITS = ["degrees", "radians", "gradians", "turns"]