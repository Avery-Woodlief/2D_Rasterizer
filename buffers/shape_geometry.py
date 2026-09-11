from typing import Any
from skimage.morphology import footprints
from helpers.shape_calculation_helpers import *
from time import perf_counter
import skimage.draw


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
def triangle(world : np.ndarray, points : list, **kw) -> tuple[np.ndarray | None, np.ndarray | None] | int:

    if len(points) != 3:
        raise ValueError(f"Need 3 points for a triangle, got {len(points)}")
    p1 = points[0]
    p2 = points[1]
    x1, y1 = p1
    x2, y2 = p2

    apex_pos = points[2]
    Ax, Ay = apex_pos

    height = abs(Ay - y1)
    base = abs(x2 - x1)
    print(base, height)

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
    region, clipped_mask = clipping_helper(world, mask, apex_pos=apex_pos, base=base, height=height)
    color = kw.get("color", [0, 0, 0, 255])
    if (region is not None) and (clipped_mask is not None):
        region[clipped_mask] = color
        return 1
    return region, clipped_mask
#Clipping - done


from dataclasses import dataclass
from random import randint

@dataclass
class Polygon:
    rr: np.ndarray
    cc : np.ndarray
    color: tuple[int, int, int, int]

layers = {}
LAYER_COLORS = [[layer] + [randint(layer, 255) for _ in range(2)] + [255] for layer in range(256)]

def polygon(buffer : np.ndarray, points : list, **kw):
    layer = kw.get("layer", 0)
    axis0 = [point[1] for point in points]
    axis1 = [point[0] for point in points]

    rr, cc = skimage.draw.polygon(axis0, axis1,shape=buffer.shape[:2])


    buffer[rr, cc] = LAYER_COLORS[layer]
    if layers.get(layer, None) is not None:
        layers[layer].append(Polygon(rr=rr, cc=cc, color=kw.get("color", [0, 0, 0, 255])))
    else:
        layers[layer] = [Polygon(rr=rr, cc=cc, color=kw.get("color", [0, 0, 0, 255]))]


def clean_image(framebuffer:np.ndarray, cleaning_footprint : np.ndarray) -> np.ndarray:
    from skimage.morphology import opening, closing

    HEIGHT, WIDTH = framebuffer.shape[:2]
    num_layers = len(layers)

    masked_layers = {}

    # --------------------------------------------------
    # Combine polygons belonging to each layer
    # --------------------------------------------------

    for layer in range(num_layers):

        mask = np.zeros(
            framebuffer.shape[:2],
            dtype=bool
        )

        for poly in layers[layer]:
            mask[poly.rr, poly.cc] = True

        masked_layers[layer] = mask


    # --------------------------------------------------
    # Clean each complete layer ONCE
    # --------------------------------------------------


    for layer in range(num_layers):

        mask = masked_layers[layer]

        mask = opening(
            mask,
            cleaning_footprint
        )

        mask = closing(
            mask,
            cleaning_footprint
        )

        masked_layers[layer] = mask


    # --------------------------------------------------
    # Final RGBA framebuffer
    # --------------------------------------------------

    final_image = np.zeros(
        (HEIGHT, WIDTH, 4),
        dtype=np.uint8
    )


    # --------------------------------------------------
    # Restore polygon colors, respecting cleaned masks
    # --------------------------------------------------

    for layer in range(num_layers):

        cleaned_mask = masked_layers[layer]

        for poly in layers[layer]:

            # Which original polygon pixels survived cleaning?
            keep = cleaned_mask[
                poly.rr,
                poly.cc
            ]

            rr = poly.rr[keep]
            cc = poly.cc[keep]

            final_image[
                rr,
                cc
            ] = poly.color
    return final_image


def mirror_shape_axis(shape_buffer : np.ndarray, axis : int = 0) -> np.ndarray | None:
    if axis > len(shape_buffer.shape):
        return None
        #raise np.exceptions.AxisError(f"axis {axis} is out of bounds for array of dimension {len(shape_buffer.shape)}")
    return np.flip(shape_buffer, axis=axis)

def mirror_shape(shape_buffer : np.ndarray) -> tuple | Any:
    return footprints.mirror_footprint(shape_buffer)