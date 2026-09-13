import numpy as np
from buffers.shape_geometry import polygon
from random import randint
from dataclasses import dataclass
from skimage import io


@dataclass
class Polygon:
    rr: np.ndarray
    cc : np.ndarray
    color: tuple[int, int, int, int]


LAYER_COLORS = [[layer] + [randint(layer, 255) for _ in range(2)] + [255] for layer in range(256)]


class Drawing:
    def __init__(self, height : int, width : int, alpha : bool = True):
        self.width = width
        self.height = height
        self.framebuffer = np.zeros(
            (self.height, self.width, 4 if alpha else 3),
            dtype=np.uint8
        )
        self.layers = {}



    def poly(self, points : list, **kw):
        poly_data = polygon(self.framebuffer, points, **kw)
        dims, color, layer = poly_data
        rr, cc = dims
        self.framebuffer[rr, cc] = LAYER_COLORS[layer]
        if self.layers.get(layer, None) is not None:
            self.layers[layer].append(Polygon(rr=rr, cc=cc, color=color))
        else:
            self.layers[layer] = [Polygon(rr=rr, cc=cc, color=color)]

    def clean_image(self, cleaning_footprint : np.ndarray) -> np.ndarray:
        from skimage.morphology import opening, closing

        HEIGHT, WIDTH = self.framebuffer.shape[:2]
        num_layers = len(self.layers)

        masked_layers = {}

        # --------------------------------------------------
        # Combine polygons belonging to each layer
        # --------------------------------------------------

        for layer in range(num_layers):

            mask = np.zeros(
                self.framebuffer.shape[:2],
                dtype=bool
            )

            for poly in self.layers[layer]:
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

            for poly in self.layers[layer]:

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

    def imsave(self, name : str, buffer_input : np.ndarray) -> None:
        io.imsave(name, buffer_input)