import numpy as np
from skimage.morphology import footprints

def draw_circle(main_buffer, center, radius, color):
    mask = footprints.disk(radius).astype(bool)
    x, y = center
    region = main_buffer[
        y-radius:y + radius + 1,
        x-radius:x + radius + 1
    ]

    region[mask] = color

def draw_diamond(main_buffer, center, radius, color):
    mask = footprints.diamond(radius).astype(bool)
    x, y = center
    region = main_buffer[
        y-radius:y + radius + 1,
        x-radius:x + radius + 1
    ]

    region[mask] = color

def draw_ellipse(main_buffer, topleft, width, height, color):
    mask = footprints.ellipse(width, height).astype(bool)

    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]

    region[mask] = color

def draw_octagon(main_buffer, topleft, m, n, color):
    mask = footprints.octagon(m, n).astype(bool)

    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color


def draw_star(main_buffer, topleft, a, color):
    mask = footprints.star(a).astype(bool)

    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color

def draw_rectangle(main_buffer, topleft, shape, color):
    mask = footprints.footprint_rectangle(shape).astype(bool)
    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color


def cross_footprint(size: int):
    mask = np.zeros((size, size), dtype=bool)

    center = size // 2

    mask[center, :] = True
    mask[:, center] = True

    return mask
def draw_cross(main_buffer, topleft, size, color):
    mask = cross_footprint(size).astype(bool)
    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color