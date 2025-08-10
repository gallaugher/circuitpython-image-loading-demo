# wrap-text-demo.py
import board, busio, time, displayio, pwmio, terminalio, fourwire
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import wrap_text_to_pixels
import adafruit_ili9341
import adafruit_imageload

# Check Memory Function:
import gc

def mem(label=""):
    gc.collect()
    print(f"{label} free: {gc.mem_free()} bytes")

mem("Boot")

# --- Display Setup ---
displayio.release_displays()

# SPI bus for display
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

# Display control pins
tft_cs = board.GP20
tft_dc = board.GP21
tft_reset = board.GP15

# Display bus
display_bus = fourwire.FourWire(
   spi,
   command=tft_dc,
   chip_select=tft_cs,
   reset=tft_reset
)

# Initialize display in landscape mode
display = adafruit_ili9341.ILI9341(
   display_bus,
   width=320,
   height=240,
   rotation=0,  # Landscape mode
   backlight_pin=None # Board has a backlight but we'll handle it w/pwm so we can dim.
)

# PWM backlight - note we ignore the backlight pin.
# to change backlight, set: backlight.duty_cycle = to range 0-65535
backlight = pwmio.PWMOut(board.GP22, frequency=5000, duty_cycle=65535)

group = displayio.Group()
display.root_group = group

label_font = bitmap_font.load_font("/fonts/Collegiate-50.bdf")

# # Read from "disk"
# mem("Before load")
# bitmap = displayio.OnDiskBitmap("/images/Whale Shark.bmp")
# mem("After load")
# # Create a TileGrid to hold the bitmap
# tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
# # Add the TileGrid to the Group
# group.append(tile_grid)

# Load image into RAM
mem("Before load")
ws_bitmap, ws_palette = adafruit_imageload.load("/images/Whale Shark.bmp")
mem("After load")
# Create a TileGrid to hold the bitmap
ws_tile_grid = displayio.TileGrid(ws_bitmap, pixel_shader=ws_palette)

# Center vertically
ws_tile_grid.y = (display.height-ws_bitmap.height) //2

# Add the TileGrid to the Group
group.append(ws_tile_grid)

ws_label = Label(
   label_font,
   text="Whale Shark",
   background_tight=True,
   anchor_point=(0.5, 1),
   anchored_position=(display.width//2, display.height-1),
   color=(255, 255, 255)
)
group.append(ws_label)

# Load image into RAM
mem("Before load")
cf_bitmap, cf_palette = adafruit_imageload.load("/images/Cuddlefish.bmp")
mem("After load")
# Create a TileGrid to hold the bitmap
cf_tile_grid = displayio.TileGrid(cf_bitmap, pixel_shader=cf_palette)

cf_label = Label(
   label_font,
   text="Cuttlefish",
   background_tight=False,
   anchor_point=(0.5, 1),
   anchored_position=(display.width//2, display.height-1-30),
   padding_top=-25,
   padding_bottom=5,
   padding_right=5,
   padding_left=5,
   background_color=(0, 0, 0),
   color=(255, 255, 255)
)

# Add the cf_tile_grid to the Group
group.append(cf_tile_grid)
group.append(cf_label)

while True:
   ws_tile_grid.hidden = False
   cf_tile_grid.hidden = True
   ws_label.hidden = False
   cf_label.hidden = True
   time.sleep(3)
   ws_tile_grid.hidden = True
   cf_tile_grid.hidden = False
   ws_label.hidden = True
   cf_label.hidden = False
   time.sleep(3)