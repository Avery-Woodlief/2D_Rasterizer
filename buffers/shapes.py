import numpy as np
from skimage.morphology import footprints


def compute_clipped_bounds(main_buffer : np.ndarray, **kw) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    buffer_height, buffer_width = main_buffer.shape[:2]
    radius = kw.get("radius", None)
    center = kw.get("center", None)
    topleft = kw.get("topleft", None)
    width = kw.get("width", None)
    height = kw.get("height", None)
    apex_pos = kw.get("apex_pos", None)
    base = kw.get("base", None)
    x_offset = kw.get("x_offset", None)

    x1 = x2 = y1 = y2 = 0

    if (radius is not None) and (center is not None) and isinstance(center, tuple) and isinstance(radius, int):
        x, y = center
        x1 = x - radius
        x2 = x + radius + 1
        y1 = y - radius
        y2 = y + radius + 1
    elif (topleft is not None) and (width is not None) and (height is not None) and isinstance(topleft, tuple) and isinstance(width, int) and isinstance(height, int):
        x, y = topleft
        x1 = x
        x2 = x + width
        y1 = y
        y2 = y + height
    elif (apex_pos is not None) and (base is not None) and (height is not None) and (x_offset is not None) and isinstance(apex_pos, tuple) and isinstance(base, int) and isinstance(height, int) and isinstance(x_offset, int):
        Ax, Ay = apex_pos
        x1 = x_offset
        x2 = x_offset + base
        y1 = Ay - height
        y2 = Ay
    buffer_x1 = max(0, x1)
    buffer_x2 = min(buffer_width, x2)
    buffer_y1 = max(0, y1)
    buffer_y2 = min(buffer_height, y2)
    mask_x1 = buffer_x1 - x1
    mask_x2 = mask_x1 + (buffer_x2 - buffer_x1)
    mask_y1 = buffer_y1 - y1
    mask_y2 = mask_y1 + (buffer_y2 - buffer_y1)

    return (buffer_x1, buffer_x2, buffer_y1, buffer_y2), (mask_x1, mask_x2, mask_y1, mask_y2)

def clipping_helper(main_buffer : np.ndarray, mask : np.ndarray, color : tuple[int, int, int, int], **kw) -> None:
    radius = kw.get("radius", None)
    center = kw.get("center", None)
    topleft = kw.get("topleft", None)
    width = kw.get("width", None)
    height = kw.get("height", None)
    apex_pos = kw.get("apex_pos", None)
    base = kw.get("base", None)
    x_offset = kw.get("x_offset", None)

    buffer_bounds = None
    mask_bounds = None

    if (radius is not None) and (center is not None) and isinstance(radius, int) and isinstance(center, tuple):
        buffer_bounds, mask_bounds = compute_clipped_bounds(main_buffer, center=center, radius=radius)
    elif (width is not None) and (height is not None) and (topleft is not None) and isinstance(width, int) and isinstance(height, int) and isinstance(topleft, tuple):
        buffer_bounds, mask_bounds = compute_clipped_bounds(main_buffer, topleft=topleft, width=width, height=height)
    elif (apex_pos is not None) and (base is not None) and (height is not None) and (x_offset is not None) and isinstance(apex_pos, tuple) and isinstance(base, int) and isinstance(height, int) and isinstance(x_offset, int):
        buffer_bounds, mask_bounds = compute_clipped_bounds(main_buffer, apex_pos=apex_pos, base=base, height=height, x_offset=x_offset)

    if (buffer_bounds is not None) and (mask_bounds is not None):
        bx1, bx2, by1, by2 = buffer_bounds
        mx1, mx2, my1, my2 = mask_bounds
        region = main_buffer[by1:by2, bx1:bx2]
        clipped_mask = mask[my1:my2, mx1:mx2]
        region[clipped_mask.astype(bool)] = color
    return

def draw_circle(main_buffer : np.ndarray, center : tuple[int, int], radius : int, color : tuple[int, int, int, int]) -> None:
    """
        with strict_radius being False, the radius is extended by 0.5.
    """
    mask = footprints.disk(radius, strict_radius=False).astype(bool)
    clipping_helper(main_buffer, mask, color, radius=radius, center=center)
#Clipping - done

def draw_diamond(main_buffer : np.ndarray, center : tuple[int, int], radius : int, color : tuple[int, int, int, int]) -> None:
    mask = footprints.diamond(radius).astype(bool)
    clipping_helper(main_buffer, mask, color, radius=radius, center=center)
#Clipping - done

def draw_ellipse(main_buffer : np.ndarray, topleft : tuple[int, int], width : int, height : int, color : tuple[int, int, int, int]) -> None:
    mask = footprints.ellipse(width//2, height//2).astype(bool)
    clipping_helper(main_buffer, mask, color, topleft=topleft, width=width, height=height)
#Clipping - done

def draw_octagon(main_buffer : np.ndarray, topleft : tuple[int, int], m : int, n : int, color : tuple[int, int, int, int]) -> None:
    mask = footprints.octagon(m, n).astype(bool)
    width = (m + (2*n))
    height = (m + (2*n))
    clipping_helper(main_buffer, mask, color, topleft=topleft, width=width, height=height)
#Clipping - done

def draw_star(main_buffer : np.ndarray, topleft : tuple[int, int], a : int, color: tuple[int, int, int, int]) -> None:
    mask = footprints.star(a).astype(bool)
    width = ((2*a) + 1 + (2*(a//2)))
    height = ((2*a) + 1 + (2*(a//2)))
    clipping_helper(main_buffer, mask, color, topleft=topleft, width=width, height=height)
#Clipping - done

def draw_rectangle(main_buffer : np.ndarray, topleft : tuple[int, int], shape : tuple[int, int], color: tuple[int, int, int, int]) -> None:
    mask = footprints.footprint_rectangle(shape).astype(bool)
    height, width = shape
    clipping_helper(main_buffer, mask, color, topleft=topleft, width=width, height=height)
#Clipping - done

from cython_code.triangle_mask import build_triangle_mask
def draw_triangle(main_buffer, color, height, base, apex_pos, x_offset = 0):

    Ax, Ay = apex_pos

    mask = footprints.footprint_rectangle((height, base)).astype(np.uint8)

    try:
        m1 = height / Ax
    except ZeroDivisionError:
        m1 = np.inf

    try:
        m3 = (-height) / (base - Ax)
    except ZeroDivisionError:
        m3 = np.inf


    build_triangle_mask(apex_pos, mask, base, height, m1, m3)

    mask = np.flip(mask, axis=0)
    clipping_helper(main_buffer, mask, color, apex_pos=apex_pos, base=base, height=height, x_offset=x_offset)

    """
    # Desired framebuffer bounds
    x1 = x_offset
    x2 = x_offset + base

    y1 = Ay - height
    y2 = Ay

    buffer_height, buffer_width = main_buffer.shape[:2]

    # Clip framebuffer bounds
    buffer_x1 = max(0, x1)
    buffer_x2 = min(buffer_width, x2)

    buffer_y1 = max(0, y1)
    buffer_y2 = min(buffer_height, y2)

    # Matching mask bounds
    mask_x1 = buffer_x1 - x1
    mask_x2 = mask_x1 + (buffer_x2 - buffer_x1)

    mask_y1 = buffer_y1 - y1
    mask_y2 = mask_y1 + (buffer_y2 - buffer_y1)

    region = main_buffer[
        buffer_y1:buffer_y2,
        buffer_x1:buffer_x2
    ]

    clipped_mask = mask[
        mask_y1:mask_y2,
        mask_x1:mask_x2
    ]

    region[clipped_mask.astype(bool)] = color
    
    bx1, bx2, by1, by2 = buffer_bounds
    mx1, mx2, my1, my2 = mask_bounds
    region = main_buffer[by1:by2, bx1:bx2]
    clipped_mask = mask[my1:my2, mx1:mx2]
    region[clipped_mask] = color
    
    """
#Clipping - done