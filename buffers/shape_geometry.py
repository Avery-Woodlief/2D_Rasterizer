from typing import Any
from skimage.morphology import footprints
from helpers.shape_calculation_helpers import *
from time import perf_counter


def circle(world : np.ndarray, center : tuple[int, int], radius : int, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:
    """
        with strict_radius being False, the radius is extended by 0.5.
    """

    mask = footprints.disk(radius, strict_radius=False).astype(bool)
    region, clipped_mask = clipping_helper(world, mask, radius=radius, center=center)
    if (region is not None) and (clipped_mask is not None):
        color = kw.get("color", [0, 0, 0, 255])
        region[clipped_mask] = color
        return None
    return region, clipped_mask
#Clipping - done

def diamond(world : np.ndarray, center : tuple[int, int], radius : int, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:
    mask = footprints.diamond(radius).astype(bool)
    region, clipped_mask = clipping_helper(world, mask, radius=radius, center=center)
    if (region is not None) and (clipped_mask is not None):
        color = kw.get("color", [0, 0, 0, 255])
        region[clipped_mask] = color
        return None
    return region, clipped_mask
#Clipping - done

def ellipse(world : np.ndarray, topleft : tuple[int, int], width : int, height : int, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:
    mask = footprints.ellipse(width//2, height//2).astype(bool)
    region, clipped_mask = clipping_helper(world, mask, topleft=topleft, width=width, height=height)
    if (region is not None) and (clipped_mask is not None):
        color = kw.get("color", [0, 0, 0, 255])
        region[clipped_mask] = color
        return None
    return region, clipped_mask
#Clipping - done

def octagon(world : np.ndarray, topleft : tuple[int, int], m : int, n : int, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:
    mask = footprints.octagon(m, n).astype(bool)
    width = (m + (2*n))
    height = (m + (2*n))
    region, clipped_mask = clipping_helper(world, mask, topleft=topleft, width=width, height=height)
    if (region is not None) and (clipped_mask is not None):
        color = kw.get("color", [0, 0, 0, 255])
        region[clipped_mask] = color
        return None
    return region, clipped_mask
#Clipping - done

def star(world : np.ndarray, topleft : tuple[int, int], a : int, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:
    mask = footprints.star(a).astype(bool)
    width = ((2*a) + 1 + (2*(a//2)))
    height = ((2*a) + 1 + (2*(a//2)))
    region, clipped_mask = clipping_helper(world, mask, topleft=topleft, width=width, height=height)
    if (region is not None) and (clipped_mask is not None):
        color = kw.get("color", [0, 0, 0, 255])
        region[clipped_mask] = color
        return None
    return region, clipped_mask
#Clipping - done

def rectangle(world : np.ndarray, topleft : tuple[int, int], shape : tuple[int, int], **kw) -> tuple[np.ndarray | None, np.ndarray | None]:
    mask = footprints.footprint_rectangle(shape)


    height, width = shape
    region, clipped_mask = clipping_helper(world, mask, topleft=topleft, width=width, height=height)



    color = kw.get("color", [0, 0, 0, 255])
    if (region is not None) and (clipped_mask is not None):
        region[:] = color
    return region, clipped_mask
#Clipping - done

from cython_code.triangle_mask import build_triangle_mask
def triangle(world : np.ndarray, height : int, base: int, apex_pos : tuple[int, int], x_offset: int = 0, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | None:

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
    region, clipped_mask = clipping_helper(world, mask, apex_pos=apex_pos, base=base, height=height, x_offset=x_offset)
    color = kw.get("color", [0, 0, 0, 255])
    if (region is not None) and (clipped_mask is not None):
        region[clipped_mask] = color
        return None
    return region, clipped_mask
#Clipping - done


def mirror_shape_axis(shape_buffer : np.ndarray, axis : int = 0) -> np.ndarray | None:
    if axis > len(shape_buffer.shape):
        return None
        #raise np.exceptions.AxisError(f"axis {axis} is out of bounds for array of dimension {len(shape_buffer.shape)}")
    return np.flip(shape_buffer, axis=axis)

def mirror_shape(shape_buffer : np.ndarray) -> tuple | Any:
    return footprints.mirror_footprint(shape_buffer)