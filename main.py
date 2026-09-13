from buffers.drawing import Drawing
from helpers.polyfile_reader import read_polyfile

calls = read_polyfile("generated_palete.poly")
HEIGHT, WIDTH = calls[0]["size"]
drawing = Drawing(HEIGHT, WIDTH)
calls = calls[1:]
for call in calls:
    getattr(drawing, "poly")(**call.get("poly"))

from skimage.morphology import disk

image = drawing.clean_image(disk(0))
drawing.imsave("generated_palete", image)