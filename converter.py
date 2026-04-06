import tkinter as tk
from tkinter import ttk
import math

#pillow for icon generation
try:
    from PIL import Image, ImageDraw, ImageTk
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
    elif to_unit == "turns":
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
 
    # Title bar 
    title_bar = tk.Frame(frame, bg=COLOUR_DARK, pady=10)
    title_bar.pack(fill=tk.X)
 
    # Icon on the left of the title bar
    icon = make_icon(icon_colour, icon_symbol)
    if icon:
        icon_label = tk.Label(title_bar, image=icon, bg=COLOUR_DARK, padx=10)
        icon_label.image = icon    
        icon_label.pack(side=tk.LEFT)
 
    tk.Label(title_bar, text=title_text,
             font=FONT_TITLE, fg=COLOUR_LIGHT_TXT,
             bg=COLOUR_DARK).pack(side=tk.LEFT)
 
  # Body
    body = tk.Frame(frame, bg=COLOUR_BG, padx=30, pady=20)
    body.pack(fill=tk.BOTH, expand=True)
 
    return frame, body
 
 
def build_standard_tab(notebook, tab_label, title_text,
                        icon_colour, icon_symbol,
                        unit_list, unit_table_or_fn,
                        conversion_type="linear"):
    
    _frame, body = build_tab_frame(notebook, tab_label,
                                   title_text, icon_colour, icon_symbol)
    
    
    from_unit_var = tk.StringVar(value=unit_list[0])
    to_unit_var   = tk.StringVar(value=unit_list[min(1, len(unit_list)-1)])
    input_var     = tk.StringVar()
    result_var    = tk.StringVar(value="—")
    error_var     = tk.StringVar(value="")
 
    # run the conversion and update the display
    def do_convert(*args):
        """Called whenever the user types, changes a dropdown, or clicks Convert."""
        raw_input = input_var.get().strip()
 
        # Case 1: input box is empty — just reset quietly
        if raw_input == "":
            result_var.set("—")
            result_label.config(fg=COLOUR_RESULT_TXT)
            error_var.set("")
            return
 
        # Case 2: input is not a number — show a friendly error
        try:
            value = float(raw_input)
        except ValueError:
            error_var.set("⚠  Please enter a number  (e.g. 42, -7.5, 3.14)")
            result_var.set("—")
            result_label.config(fg=COLOUR_ERROR)
            return
 
        # Case 3: run the conversion
        try:
            if conversion_type == "linear":
                result = convert_linear(value, from_unit_var.get(),
                                        to_unit_var.get(), unit_table_or_fn)
            elif conversion_type == "temperature":
                result = convert_temperature(value, from_unit_var.get(),
                                             to_unit_var.get())
            elif conversion_type == "fuel":
                result = convert_fuel(value, from_unit_var.get(),
                                      to_unit_var.get())
            elif conversion_type == "angle":
                result = convert_angle(value, from_unit_var.get(),
                                       to_unit_var.get())
 
        except ValueError as e:
            # conversion functions raise ValueError for things like 0 mpg
            error_var.set(f"⚠  {e}")
            result_var.set("—")
            result_label.config(fg=COLOUR_ERROR)
            return
 
        # Conversion succeeded — format and display the result
        error_var.set("")    # clear any old error message
        decimals = precision_var.get()
        formatted = format_result(result, decimals)
        result_var.set(f"{formatted}  {to_unit_var.get()}")
        result_label.config(fg=COLOUR_RESULT_TXT)
 
    # swap the two units
    def swap_units():
        a = from_unit_var.get()
        b = to_unit_var.get()
        from_unit_var.set(b)
        to_unit_var.set(a)
        do_convert()
 
    # button
    def make_button(parent, text, bg_colour, hover_colour, command):
        btn = tk.Button(parent, text=text,
                        font=FONT_LABEL,
                        bg=bg_colour, fg="white",
                        activebackground=hover_colour,
                        activeforeground="white",
                        relief=tk.FLAT, padx=14, pady=6,
                        cursor="hand2", command=command)
        add_hover_effect(btn, bg_colour, hover_colour)
        return btn
    
    # FROM unit dropdown
    tk.Label(body, text="From unit:", font=FONT_LABEL,
             fg="#2C3E50", bg=COLOUR_BG).grid(row=0, column=0,
                                              sticky="w", pady=6)
    from_combo = ttk.Combobox(body, textvariable=from_unit_var,
                               values=unit_list, state="readonly",
                               font=FONT_NORMAL, width=22)
    from_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=6)
    from_combo.bind("<<ComboboxSelected>>", do_convert)   # convert on change
 
    # VALUE entry
    tk.Label(body, text="Value:", font=FONT_LABEL,
             fg="#2C3E50", bg=COLOUR_BG).grid(row=1, column=0,
                                              sticky="w", pady=6)
    entry = ttk.Entry(body, textvariable=input_var,
                      font=("Consolas", 13), width=22)
    entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=6)
    entry.bind("<KeyRelease>", do_convert)    # convert on every keystroke
    entry.bind("<Return>",     do_convert)    # also convert when Enter is pressed
 
    # TO unit dropdown
    tk.Label(body, text="To unit:", font=FONT_LABEL,
             fg="#2C3E50", bg=COLOUR_BG).grid(row=2, column=0,
                                              sticky="w", pady=6)
    to_combo = ttk.Combobox(body, textvariable=to_unit_var,
                             values=unit_list, state="readonly",
                             font=FONT_NORMAL, width=22)
    to_combo.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=6)
    to_combo.bind("<<ComboboxSelected>>", do_convert)
 
    # RESULT display
    result_panel = tk.Frame(body, bg=COLOUR_RESULT_BG, padx=14, pady=12)
    result_panel.grid(row=3, column=0, columnspan=2,
                      sticky="ew", pady=(16, 8))
 
    tk.Label(result_panel, text="Result",
             font=("Segoe UI", 8), fg="#808B96",
             bg=COLOUR_RESULT_BG).pack(anchor="w")
 
    result_label = tk.Label(result_panel, textvariable=result_var,
                             font=FONT_RESULT, fg=COLOUR_RESULT_TXT,
                             bg=COLOUR_RESULT_BG, wraplength=360,
                             justify="left")
    result_label.pack(anchor="w")
 
    # CONVERT button
    convert_btn = make_button(body, "  Convert  ",
                               COLOUR_BTN_GREEN, "#145A32", do_convert)
    convert_btn.grid(row=4, column=0, sticky="ew", pady=(4, 0),
                     padx=(0, 4))
 
    # SWAP button
    swap_btn = make_button(body, "⇅  Swap",
                            COLOUR_BTN_BLUE, "#154360", swap_units)
    swap_btn.grid(row=4, column=1, sticky="ew", pady=(4, 0),
                  padx=(4, 0))
 
    # ERROR message label
    # this is probably gonna be invisible most of the time
    tk.Label(body, textvariable=error_var,
             font=("Segoe UI", 9), fg=COLOUR_ERROR,
             bg=COLOUR_BG, wraplength=380,
             justify="left").grid(row=5, column=0, columnspan=2,
                                  sticky="w", pady=(6, 0))
 
    # for column 1 to stretch when the window is resized
    body.columnconfigure(1, weight=1)
 
    # return input variable so the main window can clear all tabs
    return input_var, result_var, error_var

#main window setup

root = tk.Tk()
root.title("Universal Unit Converter")
root.geometry("600x680")
root.minsize(500, 560)
root.configure(bg="#D5D8DC")
precision_var = tk.IntVar(value=4)
style = ttk.Style()
style.theme_use("clam") #clam is just for more colors
style.configure("TNotebook",
                background=COLOUR_DARK)
style.configure("TNotebook.Tab",
                background="#2C3E50",
                foreground="#BDC3C7",
                padding=[9, 5],
                font=("Segoe UI", 8, "bold"))
style.map("TNotebook.Tab",
          background=[("selected", "#2980B9"), ("active", "#1A6FA3")],
          foreground=[("selected", "white"),   ("active", "white")])

#toolbar
toolbar = tk.Frame(root, bg="#ECF0F1", pady=6)
toolbar.pack(fill=tk.X)
 
tk.Label(toolbar, text="Decimal places:",
         font=("Segoe UI", 9), bg="#ECF0F1",
         fg="#2C3E50").pack(side=tk.LEFT, padx=(14, 4))

#i wanted a spinbox
precision_spinbox = ttk.Spinbox(toolbar, from_=0, to=10, width=4,
                                 textvariable=precision_var,
                                 font=("Segoe UI", 10))
precision_spinbox.pack(side=tk.LEFT)

# divider line
tk.Frame(toolbar, width=1, bg="#BDC3C7").pack(
    side=tk.LEFT, fill=tk.Y, padx=12, pady=2)
 
# clear all button
def clear_all_tabs():
    """Resets every tab's input and result back to blank."""
    for input_v, result_v, error_v in all_tab_vars:
        input_v.set("")
        result_v.set("—")
        error_v.set("")
 
clear_btn = tk.Button(toolbar, text="🗑  Clear All",
                       font=("Segoe UI", 9, "bold"),
                       bg="#E74C3C", fg="white",
                       activebackground="#C0392B",
                       relief=tk.FLAT, padx=10, pady=2,
                       cursor="hand2", command=clear_all_tabs)
clear_btn.pack(side=tk.LEFT)
add_hover_effect(clear_btn, "#E74C3C", "#C0392B")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

# build_standard_tab() returns (input_var, result_var, error_var) for each tab
# storing them in a list so the "Clear All" button can reset all of it
 
all_tab_vars = []

# speed tab
vars_speed = build_standard_tab(
    notebook,
    tab_label="⚡ Speed",
    title_text="Speed Converter",
    icon_colour="#C0392B",
    icon_symbol="km",
    unit_list=list(SPEED_UNITS.keys()),
    unit_table_or_fn=SPEED_UNITS,
    conversion_type="linear"
)
all_tab_vars.append(vars_speed)
 
# temp tab
vars_temp = build_standard_tab(
    notebook,
    tab_label="🌡 Temp",
    title_text="Temperature Converter",
    icon_colour="#D35400",
    icon_symbol="°C",
    unit_list=TEMPERATURE_UNITS,
    unit_table_or_fn=None,           # no table needed — uses its own function
    conversion_type="temperature"
)
all_tab_vars.append(vars_temp)
 
# length tab
vars_length = build_standard_tab(
    notebook,
    tab_label="📏 Length",
    title_text="Length Converter",
    icon_colour="#1A7A4A",
    icon_symbol="m",
    unit_list=list(LENGTH_UNITS.keys()),
    unit_table_or_fn=LENGTH_UNITS,
    conversion_type="linear"
)
all_tab_vars.append(vars_length)
 
# weight / mass tab
vars_mass = build_standard_tab(
    notebook,
    tab_label="⚖ Weight",
    title_text="Weight / Mass Converter",
    icon_colour="#1A5276",
    icon_symbol="kg",
    unit_list=list(MASS_UNITS.keys()),
    unit_table_or_fn=MASS_UNITS,
    conversion_type="linear"
)
all_tab_vars.append(vars_mass)
 
# volume tab
vars_volume = build_standard_tab(
    notebook,
    tab_label="🧪 Volume",
    title_text="Volume Converter",
    icon_colour="#6C3483",
    icon_symbol="L",
    unit_list=list(VOLUME_UNITS.keys()),
    unit_table_or_fn=VOLUME_UNITS,
    conversion_type="linear"
)
all_tab_vars.append(vars_volume)
 
# area tab
vars_area = build_standard_tab(
    notebook,
    tab_label="▦ Area",
    title_text="Area Converter",
    icon_colour="#0E6655",
    icon_symbol="m²",
    unit_list=list(AREA_UNITS.keys()),
    unit_table_or_fn=AREA_UNITS,
    conversion_type="linear"
)
all_tab_vars.append(vars_area)
 
# fuel econ tab
vars_fuel = build_standard_tab(
    notebook,
    tab_label="⛽ Fuel",
    title_text="Fuel Economy Converter",
    icon_colour="#B7770D",
    icon_symbol="mpg",
    unit_list=FUEL_UNITS,
    unit_table_or_fn=None,
    conversion_type="fuel"
)
all_tab_vars.append(vars_fuel)
 
# angle tab
vars_angle = build_standard_tab(
    notebook,
    tab_label="∠ Angle",
    title_text="Angle Converter",
    icon_colour="#922B21",
    icon_symbol="°",
    unit_list=ANGLE_UNITS,
    unit_table_or_fn=None,
    conversion_type="angle"
)
all_tab_vars.append(vars_angle)
 
# force tab
vars_force = build_standard_tab(
    notebook,
    tab_label="↗ Force",
    title_text="Force Converter",
    icon_colour="#424949",
    icon_symbol="N",
    unit_list=list(FORCE_UNITS.keys()),
    unit_table_or_fn=FORCE_UNITS,
    conversion_type="linear"
)
all_tab_vars.append(vars_force)

# menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)
 
# file menu
file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(label="Clear All  (Ctrl+L)",
                       command=clear_all_tabs)
file_menu.add_separator()
file_menu.add_command(label="Exit  (Ctrl+Q)",
                       command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
 
# keyboard shortcuts
root.bind("<Control-l>", lambda event: clear_all_tabs())
root.bind("<Control-q>", lambda event: root.quit())
 
# settings menu 
settings_menu = tk.Menu(menubar, tearoff=False)
precision_menu = tk.Menu(settings_menu, tearoff=False)
for i in range(11):
    label = f"{i} decimal place{'s' if i != 1 else ''}"
    precision_menu.add_radiobutton(label=label,
                                    variable=precision_var, value=i)
settings_menu.add_cascade(label="Decimal Precision", menu=precision_menu)
menubar.add_cascade(label="Settings", menu=settings_menu)
 
# help menu
help_menu = tk.Menu(menubar, tearoff=False)
 
def show_help():
    """Opens a popup window with instructions."""
    win = tk.Toplevel(root)
    win.title("How to Use")
    win.geometry("420x380")
    win.configure(bg=COLOUR_BG)
    win.resizable(False, False)
 
    tk.Label(win, text="📖  How to Use",
             font=FONT_TITLE, fg=COLOUR_LIGHT_TXT,
             bg=COLOUR_DARK, padx=20, pady=12).pack(fill=tk.X)
 
    help_text = (
        "1.  Click a tab at the top (Speed, Temp, Length…)\n\n"
        "2.  Choose the unit you're converting FROM\n"
        "    using the first dropdown menu.\n\n"
        "3.  Type your number in the Value box.\n"
        "    The result updates automatically as you type!\n\n"
        "4.  Choose the unit you're converting TO\n"
        "    using the second dropdown.\n\n"
        "5.  Click Swap to reverse the direction.\n\n"
        "TOOLBAR:\n"
        "  • Decimal places — controls how many decimals to show.\n"
        "  • 🗑 Clear All   — resets every tab at once.\n\n"
        "KEYBOARD:\n"
        "  • Enter   — trigger conversion.\n"
        "  • Ctrl+L  — clear all tabs.\n"
        "  • Ctrl+Q  — quit the app.\n"
    )
 
    text_box = tk.Text(win, font=FONT_NORMAL, bg=COLOUR_BG,
                        relief=tk.FLAT, padx=20, pady=14,
                        wrap=tk.WORD)
    text_box.pack(fill=tk.BOTH, expand=True)
    text_box.insert(tk.END, help_text)
    text_box.config(state=tk.DISABLED)   # make it read-only
 
    tk.Button(win, text="Close", command=win.destroy,
               font=FONT_LABEL, bg=COLOUR_BTN_BLUE, fg="white",
               relief=tk.FLAT, padx=14, pady=6,
               cursor="hand2").pack(pady=10)
 
def show_about():
    """Opens a simple About popup."""
    import tkinter.messagebox as mb
    mb.showinfo(
        "About",
        "Universal Unit Converter  v1.0\n\n"
        "9 conversion categories:\n"
        "Speed • Temperature • Length\n"
        "Weight • Volume • Area\n"
        "Fuel Economy • Angle • Force\n\n"
        "Built with Python 3 and Tkinter."
    )
 
help_menu.add_command(label="How to Use", command=show_help)
help_menu.add_separator()
help_menu.add_command(label="About",      command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

# status bar
status_var = tk.StringVar(value="  Ready — select a tab and enter a value")
tk.Label(root, textvariable=status_var,
         font=("Segoe UI", 8), bg=COLOUR_DARK,
         fg="#808B96", anchor="w", padx=12, pady=4).pack(
    fill=tk.X, side=tk.BOTTOM)
 
# update status bar when the user switches tabs
TAB_NAMES = ["Speed", "Temperature", "Length", "Weight",
             "Volume", "Area", "Fuel Economy", "Angle", "Force"]
 
def on_tab_change(event):
    try:
        index = notebook.index(notebook.select())
        status_var.set(
            f"  {TAB_NAMES[index]} Converter "
            f"— type a value and press Enter or click Convert")
    except Exception:
        pass
 
notebook.bind("<<NotebookTabChanged>>", on_tab_change)
 
# now to actually start the program
root.mainloop()