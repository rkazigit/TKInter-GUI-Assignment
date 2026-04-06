# TKInter-GUI-Assignment
This is my TKinter GUI Assignment. I built a Unit Converter.

⚠️ 
Please note that this app uses Tkinter and must be run **locally** on your computer/IDE.
GitHub Codespaces and other web-based IDEs do **not** support graphical windows (I learned that the hard way).
⚠️

## How to Run

### Step 1: Download the files
- Go to the GitHub repository page
- Click the green **Code** button
- Click **Download ZIP**
- Find the downloaded ZIP file (usually in your Downloads folder)
- Right-click it and select **Extract All** 
 
### Step 2: Open in VS Code
- Open VS Code
- Click **File → Open Folder**
- Select the extracted folder
- You should see `converter.py` in the file explorer on the left
 
### Step 3: Install Pillow (one time only)
Open the VS Code terminal (View → Terminal) and type:
```
pip install Pillow
```
Wait for it to finish. This installs the library that draws the coloured icons.
If `pip` doesn't work, try:
```
pip3 install Pillow
```
 
### Step 4: Run the app
Press the ▶ Run button at the top right of VS Code and the converter window will open on your screen.

## Some features/functionality
 
| Feature | How to use it |
|---|---|
| Feature | How to use it |
| :--- | :--- |
| 1. **9 category tabs** | click each tab (Speed, Temperature, Length, Weight, Volume, Area, Fuel Economy, Angle, Force) and confirm each one opens a different converter. |
| 2. **Live conversion** | type a number digit by digit and watch the result update after every keystroke without pressing anything. |
| 3. **Combobox dropdowns** | change either the From or To dropdown while a number is typed → result updates immediately. |
| 4. **Swap button** | click Swap to reverse the units and recalculate (e.g. km/h → mph becomes mph → km/h). |
| 5. **Decimal places spinner** | click the up/down arrows in the toolbar to change precision (0-10 decimal places); result updates instantly. |
| 6. **Error: non-numeric input** | type `hello` → red error message appears. Delete it and type a number → error disappears. |
| 7. **Error: empty input** | clear the value box → result quietly resets to "-" with no error shown. |
| 8. **Error: fuel economy zero** | Fuel tab, set From to `mpg (US)`, type `0` → specific red error about mpg being greater than 0. |
| 9. **Error: temperature below absolute zero** | Temp tab, convert -300°C → red error about absolute zero. |
| 10. **Conversion history** | do 3 conversions on one tab → all 3 appear in the history panel, newest first. Do 6 → only the last 5 are kept. |
| 11. **Clear All** | click Clear All in the toolbar (or press Ctrl+L) → every tab's input and result resets at once. |
| 12. **Hover effects** | hover over the Convert, Swap, and Clear All buttons → each one changes colour. Move away → returns to normal. |
| 13. **Tab icons** | each tab header shows a different coloured icon (requires Pillow to be installed). |
| 14. **Help How to Use** | click Help in the menu bar → How to Use popup opens with instructions, closes with the Close button. |
| 15. **Settings Decimal Precision** | same precision control as the toolbar spinner, but accessible through the menu bar. |
