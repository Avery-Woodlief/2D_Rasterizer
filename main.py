from buffers.drawing import Drawing
from helpers.polyfile_reader import read_polyfile

drawing = Drawing(60, 60)
calls = read_polyfile("image.poly")
for call in calls:
    getattr(drawing, "poly")(**call.get("poly"))

drawing.imsave("test", drawing.framebuffer)