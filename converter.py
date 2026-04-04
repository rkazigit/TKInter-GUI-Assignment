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

def convert_linear(value, from_unit, to_unit, unit_table):
    """
    Converts between any two units that are in the same factor table.
    Works for speed, length, mass, volume, area, force.
 
    Formula:  result = value × factor_from ÷ factor_to
    """
    base_value = value * unit_table[from_unit]   # convert to base unit first
    result     = base_value / unit_table[to_unit] # then convert to target unit
    return result
 
 
def convert_temperature(value, from_unit, to_unit):
    """
    Temperature needs special handling because it uses addition/subtraction,
    not just multiplication.
    Strategy: first convert anything to Celsius, then convert Celsius to the target.
    """
 
    # convert TO Celsius
    if from_unit == "°C (Celsius)":
        celsius = value
    elif from_unit == "°F (Fahrenheit)":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "K (Kelvin)":
        if value < 0:
            raise ValueError("Kelvin cannot be negative (0 K = absolute zero)")
        celsius = value - 273.15
 
    # convert FROM Celsius to the target unit
    if to_unit == "°C (Celsius)":
        result = celsius
    elif to_unit == "°F (Fahrenheit)":
        result = celsius * 9 / 5 + 32
    elif to_unit == "K (Kelvin)":
        result = celsius + 273.15
        if result < 0:
            raise ValueError("Result would be below absolute zero (0 K)")
 
    return result
 
 
def convert_fuel(value, from_unit, to_unit):
    """
    Fuel economy is tricky because L/100km and mpg are INVERSELY related.
    (Lower L/100km means MORE efficient; Higher mpg means MORE efficient.)
    Strategy: convert everything to L/100km first, then to the target.
    """
    US_FACTOR = 235.215   # 235.215 ÷ mpg(US) = L/100km
    UK_FACTOR = 282.481   # 282.481 ÷ mpg(UK) = L/100km
 
    #  convert to L/100km
    if from_unit == "L/100km":
        l100 = value
    elif from_unit == "mpg (US)":
        if value <= 0:
            raise ValueError("mpg must be greater than 0")
        l100 = US_FACTOR / value
    elif from_unit == "mpg (UK)":
        if value <= 0:
            raise ValueError("mpg must be greater than 0")
        l100 = UK_FACTOR / value
    elif from_unit == "km/L":
        if value <= 0:
            raise ValueError("km/L must be greater than 0")
        l100 = 100 / value
 
    #  convert from L/100km to target
    if to_unit == "L/100km":
        return l100
    elif to_unit == "mpg (US)":
        if l100 <= 0:
            raise ValueError("L/100km must be greater than 0")
        return US_FACTOR / l100
    elif to_unit == "mpg (UK)":
        if l100 <= 0:
            raise ValueError("L/100km must be greater than 0")
        return UK_FACTOR / l100
    elif to_unit == "km/L":
        if l100 <= 0:
            raise ValueError("L/100km must be greater than 0")
        return 100 / l100
 
 
def convert_angle(value, from_unit, to_unit):
    """
    Angle conversion — uses degrees as the go-between.
    400 gradians = 360 degrees = 2π radians = 1 full turn
    """
 
    # to degrees
    if from_unit == "degrees":
        deg = value
    elif from_unit == "radians":
        deg = math.degrees(value)       #  built-in radians→degrees
    elif from_unit == "gradians":
        deg = value * 0.9               # 400 grad = 360 deg  →  1 grad = 0.9 deg
    elif from_unit == "turns":
        deg = value * 360
 
    # from degrees to target
    if to_unit == "degrees":
        return deg
    elif to_unit == "radians":
        return math.radians(deg)         # built-in degrees→radians
    elif to_unit == "gradians":
        return deg / 0.9
        return deg / 360
 
 
def format_result(number, decimal_places):
    """
    Turns a float into a nicely formatted string.
    Uses scientific notation for very big or very tiny numbers.
    """
    abs_val = abs(number)
 
    # Use scientific notation if the number is huge or tiny
    if abs_val != 0 and (abs_val >= 1e12 or abs_val < 0.000001):
        return f"{number:.{decimal_places}e}"   # now this will print things like 1.23e+12 or 4.56e-7
 
    # or just use regular decimal notation with commas
    return f"{number:,.{decimal_places}f}"      # 1,234.5678

def make_icon(bg_colour, symbol_text):
    """
    Creates a small 44×44 coloured square icon using Pillow.
    If Pillow isn't installed, returns None (no icon shown).
    """
    if not PILLOW_AVAILABLE:
        return None
 
    size = 44
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
 
   
    draw.rounded_rectangle([1, 1, size - 1, size - 1],
                            radius=6, fill=bg_colour)
 
  
    try:
        from PIL import ImageFont
        font_paths = [
            "arialbd.ttf",                                             # Windows
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",    # Linux
            "/System/Library/Fonts/Helvetica.ttc",                     # macOS
        ]
        font = None
        for path in font_paths:
            try:
                font = ImageFont.truetype(path, 13)
                break
            except Exception:
                continue
 
        if font:
            bbox = draw.textbbox((0, 0), symbol_text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            x = (size - text_w) // 2
            y = (size - text_h) // 2
            draw.text((x, y), symbol_text, fill="white", font=font)
    except Exception:
        pass  # if anything goes wrong with text, just skip it
 
    return ImageTk.PhotoImage(img)
 
 
def add_hover_effect(button, normal_colour, hover_colour):
    """
    Makes a button change colour when the mouse moves over it.
    We bind two mouse events:
      <Enter> = mouse enters the button area  → change to hover colour
      <Leave> = mouse leaves the button area  → change back to normal
    """
    button.bind("<Enter>", lambda event: button.config(bg=hover_colour))
    button.bind("<Leave>", lambda event: button.config(bg=normal_colour))

# Colours used throughout the app
COLOUR_DARK       = "#1C2833"   # dark navy — used for title bars
COLOUR_BG         = "#F2F3F4"   # light grey — main background
COLOUR_RESULT_BG  = "#212F3D"   # dark blue — result panel background
COLOUR_BTN_GREEN  = "#1E8449"   # green — Convert button
COLOUR_BTN_BLUE   = "#1F618D"   # blue — Swap button
COLOUR_ERROR      = "#C0392B"   # red — error messages
COLOUR_RESULT_TXT = "#27AE60"   # bright green — result text
COLOUR_LIGHT_TXT  = "#EAECEE"   # near-white — text on dark backgrounds
FONT_TITLE        = ("Segoe UI", 13, "bold")
FONT_LABEL        = ("Segoe UI", 10, "bold")
FONT_NORMAL       = ("Segoe UI", 10)
FONT_RESULT       = ("Consolas", 20, "bold")    

def build_tab_frame(notebook, tab_label, title_text, icon_colour, icon_symbol):
    """
    Creates the outer frame and title bar that every tab shares.
    Returns (frame, body_frame) so the caller can add more widgets.
    """
    frame = ttk.Frame(notebook)             # the container for this whole tab
    notebook.add(frame, text=tab_label)     # register it as a tab
 
    # ---- Title bar (dark strip at the top) ----
    title_bar = tk.Frame(frame, bg=COLOUR_DARK, pady=10)
    title_bar.pack(fill=tk.X)
 
    # Icon on the left of the title bar
    icon = make_icon(icon_colour, icon_symbol)
    if icon:
        icon_label = tk.Label(title_bar, image=icon, bg=COLOUR_DARK, padx=10)
        icon_label.image = icon    # IMPORTANT: must keep a reference or image disappears!
        icon_label.pack(side=tk.LEFT)
 
    tk.Label(title_bar, text=title_text,
             font=FONT_TITLE, fg=COLOUR_LIGHT_TXT,
             bg=COLOUR_DARK).pack(side=tk.LEFT)
 