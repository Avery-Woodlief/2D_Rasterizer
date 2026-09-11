import numpy as np

def compute_clipped_bounds(main_buffer : np.ndarray, **kw) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    buffer_height, buffer_width = main_buffer.shape[:2]
    radius = kw.get("radius", None)
    center = kw.get("center", None)
    topleft = kw.get("topleft", None)
    width = kw.get("width", None)
    height = kw.get("height", None)
    apex_pos = kw.get("apex_pos", None)
    base = kw.get("base", None)

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
    elif (apex_pos is not None) and (base is not None) and (height is not None) and isinstance(apex_pos, tuple) and isinstance(base, int) and isinstance(height, int):
        Ax, Ay = apex_pos
        x1 = 0
        x2 = 0 + base
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

def clipping_helper(main_buffer : np.ndarray, mask : np.ndarray, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:
    radius = kw.get("radius", None)
    center = kw.get("center", None)
    topleft = kw.get("topleft", None)
    width = kw.get("width", None)
    height = kw.get("height", None)
    apex_pos = kw.get("apex_pos", None)
    base = kw.get("base", None)
    #x_offset = kw.get("x_offset", None)

    buffer_bounds = None
    mask_bounds = None
    clipped_mask = None
    region = None

    if (radius is not None) and (center is not None) and isinstance(radius, int) and isinstance(center, tuple):
        buffer_bounds, mask_bounds = compute_clipped_bounds(main_buffer, center=center, radius=radius)

    elif (width is not None) and (height is not None) and (topleft is not None) \
         and isinstance(width, int) and isinstance(height, int) and isinstance(topleft, tuple):
        buffer_bounds, mask_bounds = compute_clipped_bounds(main_buffer, topleft=topleft, width=width, height=height)

    elif (apex_pos is not None) and (base is not None) and (height is not None) \
          and isinstance(apex_pos, tuple) and isinstance(base, int) and isinstance(height, int):
        buffer_bounds, mask_bounds = compute_clipped_bounds(main_buffer, apex_pos=apex_pos, base=base, height=height)

    if (buffer_bounds is not None) and (mask_bounds is not None):
        bx1, bx2, by1, by2 = buffer_bounds
        mx1, mx2, my1, my2 = mask_bounds
        region = main_buffer[by1:by2, bx1:bx2]
        clipped_mask = mask[my1:my2, mx1:mx2]

        if bx1 >= bx2 or by1 >= by2:
            return None, None
        return region, clipped_mask.astype(bool)
    return None