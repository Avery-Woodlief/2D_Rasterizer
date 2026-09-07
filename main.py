import json
from skimage import io
from utils.file_operations import find_file
import numpy as np
from buffers.shapes import *
from skimage.morphology import footprints#, area_opening
colors = json.load(find_file(folder_name = "color",file_name = "color_dictionary.json").open("r"))





WIDTH = 900
HEIGHT = 650
TRANSPARENT_COLOR = [0, 0, 0, 0]



framebuffer = np.full(
    (HEIGHT, WIDTH, 4),
    255,
    dtype=np.uint8
)

framebuffer[:] = TRANSPARENT_COLOR
#draw_circle(framebuffer, (400, 200), 200, colors["bright-purple"])
#draw_diamond(framebuffer, (200, 200), 87, colors["bright-blue"])
#draw_ellipse(framebuffer, (80, 80), 90, 20, colors["white"])
#draw_star(framebuffer, (400, 80), 100, colors["white"])
#draw_rectangle(framebuffer, (0, 0), (70, 70), colors["bright-green"])
#draw_rectangle(framebuffer, (0, 400), (2, 500), colors["bright-green"])
#draw_octagon(framebuffer, (0, 0), 10, 10, colors["bright-red"])
#draw_cross(framebuffer, (50, 50), 100, colors["white"])
#test_custom_circle(framebuffer, colors["bright-green"], (200, 200), 200)
test_custom_triangle(framebuffer, colors["bright-green"], 90, 350, (200, 90), 50)

io.imsave("media/test_image_blank.png", framebuffer)

