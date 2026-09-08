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
#draw_circle(framebuffer, (0, 200), 200, colors["bright-purple"])
#draw_diamond(framebuffer, (0, 0), 200, colors["bright-blue"])
#draw_star(framebuffer, (0, 0), 30, colors["white"])
#draw_rectangle(framebuffer, (0, 20), (20000, 10), colors["bright-green"])
#draw_ellipse(framebuffer, (0, 80), 900, 20, colors["transparent-purple"])

#draw_rectangle(framebuffer, (0, 400), (2, 500), colors["bright-green"])
#draw_octagon(framebuffer, (0, 50), 15, 15, colors["bright-red"])
#draw_cross(framebuffer, (50, 50), 100, colors["white"])
#test_custom_circle(framebuffer, colors["bright-green"], (200, 200), 200)
#test_custom_triangle(framebuffer, colors["bright-green"], 90, 350, (90, 90), 0)
draw_triangle(framebuffer, colors["bright-green"], 15, 80, (-10, 50), 50)


io.imsave("media/test_image_blank.png", framebuffer)

