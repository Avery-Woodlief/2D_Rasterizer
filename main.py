import json
from skimage import io
from utils.file_operations import find_file
import numpy as np
from buffers.shape_geometry import clean_image
from buffers.drawing import framebuffer


name = "realistic_polygon_face_2"

io.imsave(
    f"media/{name}_raw.png",
    framebuffer
)

from skimage.morphology import footprints

io.imsave(
    f"media/{name}_cleaned_rect_3x3.png",
    clean_image(framebuffer, footprints.footprint_rectangle((3, 3)))
)

io.imsave(
    f"media/{name}_cleaned_disk_5.png",
    clean_image(framebuffer, footprints.disk(5))
)


io.imsave(
    f"media/{name}_cleaned_disk_1.png",
    clean_image(framebuffer, footprints.disk(1))
)

io.imsave(
    f"media/{name}_cleaned_disk_0.png",
    clean_image(framebuffer, footprints.disk(0))
)