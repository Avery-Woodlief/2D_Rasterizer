import numpy as np
from skimage.morphology import footprints

def draw_circle(main_buffer : np.ndarray, center : tuple[int, int], radius : int, color : tuple[int, int, int, int]) -> None:
    """
        with strict_radius being False, the radius is extended by 0.5.
    """
    """mask = footprints.disk(radius, strict_radius=False).astype(bool)
    x, y = center
    region = main_buffer[
        y-radius:y + radius + 1,
        x-radius:x + radius + 1
    ]

    region[mask] = color"""
    mask = footprints.disk(radius, strict_radius=False).astype(bool)

    x, y = center
    #TODO: handle appropriate clipping for all shapes with a universal method

    h, w = main_buffer.shape[:2]

    # Desired bounds
    x1 = x - radius
    x2 = x + radius + 1
    y1 = y - radius
    y2 = y + radius + 1

    # Clip to framebuffer
    bx1 = max(0, x1)
    bx2 = min(w, x2)
    by1 = max(0, y1)
    by2 = min(h, y2)

    # Corresponding section of the mask
    mx1 = bx1 - x1
    mx2 = mx1 + (bx2 - bx1)
    my1 = by1 - y1
    my2 = my1 + (by2 - by1)

    region = main_buffer[by1:by2, bx1:bx2]
    clipped_mask = mask[my1:my2, mx1:mx2]

    region[clipped_mask] = color

def draw_diamond(main_buffer : np.ndarray, center : tuple[int, int], radius : int, color : tuple[int, int, int, int]) -> None:
    mask = footprints.diamond(radius).astype(bool)
    x, y = center
    region = main_buffer[
        y-radius:y + radius + 1,
        x-radius:x + radius + 1
    ]

    region[mask] = color

def draw_ellipse(main_buffer : np.ndarray, topleft : tuple[int, int], width : int, height : int, color : tuple[int, int, int, int]) -> None:
    mask = footprints.ellipse(width, height).astype(bool)

    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]

    region[mask] = color

def draw_octagon(main_buffer : np.ndarray, topleft : tuple[int, int], m : int, n : int, color : tuple[int, int, int, int]) -> None:
    mask = footprints.octagon(m, n).astype(bool)

    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color


def draw_star(main_buffer : np.ndarray, topleft : tuple[int, int], a : int, color: tuple[int, int, int, int]) -> None:
    mask = footprints.star(a).astype(bool)

    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color

def draw_rectangle(main_buffer : np.ndarray, topleft : tuple[int, int], shape : tuple[int, int], color: tuple[int, int, int, int]) -> None:
    mask = footprints.footprint_rectangle(shape).astype(bool)
    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color


def cross_footprint(size: int) -> np.ndarray:
    mask = np.zeros((size, size), dtype=bool)

    center = size // 2

    mask[center, :] = True
    mask[:, center] = True

    return mask
def draw_cross(main_buffer : np.ndarray, topleft : tuple[int, int], size : int, color: tuple[int, int, int, int]) -> None:
    mask = cross_footprint(size).astype(bool)
    x, y = topleft
    mask_height, mask_width = mask.shape

    region = main_buffer[
        y:y + mask_height,
        x:x + mask_width
    ]
    region[mask] = color

def test_custom_circle(main_buffer, color, center, radius):
    test_footprint = []#[[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    c_x, c_y = center
    for y in range(2*radius + 1):
        test_footprint.append([])
        for x in range(2*radius + 1):
            if ((x - c_x)**2 + (y-c_y)**2) <= ((radius**2) + .5):
                test_footprint[y].append(1)
            else:
                test_footprint[y].append(0)
    test_footprint = np.array(test_footprint)
    mask = test_footprint.astype(bool)
    mask_height, mask_width = mask.shape
    region = main_buffer[c_y - radius:c_y + radius + 1,c_x - radius:c_x+radius + 1]
    region[mask] = color

def test_custom_triangle(main_buffer, color, height, base, apex_pos, x_offset = 0):
    Ax, Ay = apex_pos
    mask = footprints.footprint_rectangle((height, base)).astype(bool)

    m1 = height/Ax
    try:
        m3 = (-height)/(base - Ax)

    except ZeroDivisionError:
        m3 = np.inf
    Y1 = lambda x: -height + Ay + m1*x
    Y2 = Ay - height
    Y3 = lambda x: Ay + m3 * (x - Ax)
    for y in range(Ay - height, Ay + 1):
        for x in range(base):
            if (0 <= x <= Ax):
                if (y > Y1(x)):
                    mask[Ay - y, x] = 0
            elif (Ax < x <= base):
                if (y > Y3(x)):
                    mask[Ay - y, x] = 0
    region = main_buffer[
        Y2: Ay,
        x_offset: base + x_offset
    ]
    #mask[:] = footprints.mirror_footprint(mask[:])
    mask = np.flip(mask, axis=0)
    region[mask.astype(bool)] = color
    import json
    from utils.file_operations import find_file
    colors = json.load(find_file(folder_name = "color",file_name = "color_dictionary.json").open("r"))

    draw_circle(main_buffer, (Ax + x_offset, Ay), 2, colors["bright-purple"])
    draw_circle(main_buffer, (x_offset, Y2), 2, colors["bright-purple"])
    draw_circle(main_buffer, (base + x_offset, Y2), 2, colors["bright-purple"])


