import json
from skimage import io
from utils.file_operations import find_file
import numpy as np
from buffers.shape_geometry import *
from skimage.morphology import footprints#, area_opening

WIDTH = 512
HEIGHT = 512

framebuffer = np.zeros(
    (HEIGHT, WIDTH, 4),
    dtype=np.uint8
)

# background
polygon(
    framebuffer,
    [(0, 0), (511, 0), (511, 511), (0, 511)],
    color=(230, 220, 210, 255)
)

# face / jaw
polygon(
    framebuffer,
    [
        (160, 110),
        (220, 75),
        (292, 75),
        (352, 110),
        (385, 190),
        (372, 310),
        (330, 395),
        (256, 440),
        (182, 395),
        (140, 310),
        (127, 190)
    ],
    color=(224, 176, 138, 255)
)

# hair
polygon(
    framebuffer,
    [
        (145, 185),
        (145, 125),
        (175, 75),
        (225, 50),
        (295, 52),
        (345, 80),
        (375, 135),
        (370, 190),
        (345, 145),
        (310, 125),
        (275, 135),
        (245, 115),
        (210, 135),
        (175, 125)
    ],
    color=(62, 42, 32, 255)
)

# left eyebrow
polygon(
    framebuffer,
    [
        (165, 195),
        (215, 184),
        (224, 194),
        (173, 205)
    ],
    color=(75, 48, 35, 255)
)

# right eyebrow
polygon(
    framebuffer,
    [
        (288, 194),
        (297, 184),
        (347, 195),
        (339, 205)
    ],
    color=(75, 48, 35, 255)
)

# left eye white
polygon(
    framebuffer,
    [
        (168, 222),
        (188, 211),
        (216, 214),
        (230, 226),
        (214, 237),
        (188, 238)
    ],
    color=(245, 245, 240, 255)
)

# right eye white
polygon(
    framebuffer,
    [
        (282, 226),
        (296, 214),
        (324, 211),
        (344, 222),
        (324, 238),
        (298, 237)
    ],
    color=(245, 245, 240, 255)
)

# left iris
polygon(
    framebuffer,
    [
        (192, 216),
        (205, 215),
        (215, 225),
        (208, 236),
        (194, 235),
        (186, 225)
    ],
    color=(70, 105, 115, 255)
)

# right iris
polygon(
    framebuffer,
    [
        (307, 215),
        (320, 216),
        (328, 225),
        (320, 235),
        (306, 236),
        (298, 225)
    ],
    color=(70, 105, 115, 255)
)

# pupils
polygon(
    framebuffer,
    [
        (198, 219),
        (208, 220),
        (211, 228),
        (204, 234),
        (195, 230)
    ],
    color=(20, 20, 20, 255)
)

polygon(
    framebuffer,
    [
        (311, 220),
        (321, 219),
        (326, 230),
        (317, 234),
        (308, 228)
    ],
    color=(20, 20, 20, 255)
)

# nose
polygon(
    framebuffer,
    [
        (252, 225),
        (240, 300),
        (254, 316),
        (275, 307),
        (264, 298)
    ],
    color=(190, 137, 105, 255)
)

# nose highlight
polygon(
    framebuffer,
    [
        (255, 235),
        (253, 294),
        (262, 302),
        (266, 296)
    ],
    color=(235, 190, 151, 255)
)

# left ear
polygon(
    framebuffer,
    [
        (127, 205),
        (108, 218),
        (112, 278),
        (135, 295),
        (145, 270),
        (141, 220)
    ],
    color=(211, 158, 122, 255)
)

# right ear
polygon(
    framebuffer,
    [
        (385, 205),
        (404, 218),
        (400, 278),
        (377, 295),
        (367, 270),
        (371, 220)
    ],
    color=(211, 158, 122, 255)
)

# upper lip
polygon(
    framebuffer,
    [
        (205, 345),
        (238, 334),
        (256, 340),
        (274, 334),
        (307, 345),
        (274, 351),
        (256, 349),
        (238, 351)
    ],
    color=(137, 73, 70, 255)
)

# lower lip
polygon(
    framebuffer,
    [
        (205, 345),
        (238, 351),
        (256, 349),
        (274, 351),
        (307, 345),
        (278, 368),
        (256, 373),
        (234, 368)
    ],
    color=(175, 98, 92, 255)
)

# left cheek shadow
polygon(
    framebuffer,
    [
        (144, 260),
        (174, 280),
        (185, 340),
        (165, 375),
        (142, 315)
    ],
    color=(205, 151, 116, 255)
)

# right cheek shadow
polygon(
    framebuffer,
    [
        (368, 260),
        (338, 280),
        (327, 340),
        (347, 375),
        (370, 315)
    ],
    color=(205, 151, 116, 255)
)

# neck
polygon(
    framebuffer,
    [
        (210, 400),
        (302, 400),
        (320, 511),
        (192, 511)
    ],
    color=(205, 151, 115, 255)
)

# shirt / shoulders
polygon(
    framebuffer,
    [
        (192, 445),
        (115, 475),
        (65, 511),
        (447, 511),
        (397, 475),
        (320, 445),
        (290, 485),
        (256, 500),
        (222, 485)
    ],
    color=(55, 76, 105, 255)
)
io.imsave("media/creepy_polygon_face.png", framebuffer)
