# must be run from root dir
import colorsys
from pathlib import Path
from PIL import Image
import numpy as np
#np.set_printoptions(threshold=np.inf)
from skimage import io
from random import randint
from utils.file_operations import find_file, ROOT, overwrite_file, resolve_path

def clip(mask_buffer : np.ndarray, mask : np.ndarray, width:int, height:int, x : int, y : int):
    h, w = mask.shape

    #x = randint(0, width - 1)
    #y = randint(0, height - 1)

    radius = (h+w) // 4

    # Unclipped disk bounds in image coordinates
    x1 = x - radius
    x2 = x1 + w

    y1 = y - radius
    y2 = y1 + h

    # Clip against image
    cx1 = max(0, x1)
    cx2 = min(width, x2)

    cy1 = max(0, y1)
    cy2 = min(height, y2)

    # Corresponding portion of the mask
    mx1 = cx1 - x1
    mx2 = mx1 + (cx2 - cx1)

    my1 = cy1 - y1
    my2 = my1 + (cy2 - cy1)

    mask_buffer[
        cy1:cy2,
        cx1:cx2
    ] = mask[
        my1:my2,
        mx1:mx2
    ]


def clip_circle_mask(mask_buffer : np.ndarray, circle_mask : np.ndarray, radius : int, center : tuple[int, int], width:int, height:int):
    mask_center_x, mask_center_y = center # in terms of the mask_buffer coordinate system

    mask_height, mask_width = circle_mask.shape

    x_lower_bound_global = 0
    x_upper_bound_global = width - 1
    y_lower_bound_global = 0
    y_upper_bound_global = height - 1

    global_x1 = mask_center_x - radius
    global_x2 = mask_center_x + radius + 1
    global_y1 = mask_center_y - radius
    global_y2 = mask_center_y + radius + 1

    mask_x1 = 0
    mask_x2 = mask_width
    mask_y1 = 0
    mask_y2 = mask_height
    clipped = False

    if mask_center_x - radius < x_lower_bound_global:
        #print("left side clip")
        i = x_lower_bound_global - (mask_center_x - radius)
        mask_x1 += i
        global_x1 += i
        clipped = True


    if mask_center_x + radius > x_upper_bound_global:
        #print("right side clip")
        i = (mask_center_x + radius) - x_upper_bound_global
        mask_x2 -= i
        global_x2 -= i
        clipped = True

    if mask_center_y - radius < y_lower_bound_global:
        #print("top side clip")
        i = y_lower_bound_global - (mask_center_y - radius)
        mask_y1 += i
        global_y1 += i
        clipped = True

    if mask_center_y + radius > y_upper_bound_global:
        #print("bottom side clip")
        i = (mask_center_y + radius) - y_upper_bound_global
        mask_y2 -= i
        global_y2 -= i
        clipped = True

    if clipped:
        mask_buffer[global_y1:global_y2,global_x1:global_x2] = circle_mask[mask_y1:mask_y2,mask_x1:mask_x2]
    else:
        mask_buffer[global_y1:global_y2,global_x1:global_x2] = circle_mask


def sample_colors(image : np.ndarray,mask: np.ndarray, radius) -> np.ndarray:



    height, width = image.shape[:2]

    mask_buffer = np.zeros((height, width), dtype=bool)
    #clip(mask_buffer, mask, width, height)
    x = randint(0, width - 1)
    y = randint(0, height - 1)
    clip_circle_mask(mask_buffer, mask, radius, (x, y), width, height)

    pixels = image[mask_buffer]

    if len(pixels) == 0:
        return np.empty((0, image.shape[-1]), dtype=image.dtype)

    return pixels



def create_palette_image_instructions(colors: list[list[int] | tuple[int, ...]]):
    count = len(colors)
    x_spacing = 0
    y_spacing = 0
    w=50
    h=50
    rows=count % w
    palete_width = (w + x_spacing) * (count//rows)
    palete_height = (h + y_spacing) * (count//rows)

    def hue(color):
        r, g, b = color[:3]

        h, s, v = colorsys.rgb_to_hsv(
            r / 255,
            g / 255,
            b / 255
        )

        return h
    def dom_RGBchannel_freqs() -> dict:
        freqs = {"red" : 0, "green" : 0, "blue" : 0}
        for color in colors:
            red = color[0]
            green = color[1]
            blue = color[2]
            c_max = max([red, green, blue])
            if red == c_max:
                freqs["red"] += 1
            if green == c_max:
                freqs["green"] += 1
            if blue == c_max:
                freqs["blue"] += 1
        return freqs
    def rect_poly_line(layer, topleft, w, h, color, x_offset=0,y_offset=0) -> str:
        x, y = topleft
        r,g,b,a = color
        return f"P|{layer}|{r},{g},{b},{a}|{x + x_offset},{y+y_offset};{x+x_offset+w},{y+y_offset};{x+x_offset+w},{y+y_offset+h};{x+x_offset},{y+y_offset+h}"
    """
    data = dom_RGBchannel_freqs()
    #print(data)
    max_channel = max(data.keys(), key=lambda x: data[x])
    #print(max_channel, data[max_channel])
    if max_channel == "red":
        colors = sorted(colors, key=lambda color:color[0])
    elif max_channel == "green":
        colors = sorted(colors, key=lambda color:color[1])
    elif max_channel == "blue":
        colors = sorted(colors, key=lambda color:color[2])"""
    colors = sorted(colors, key=lambda x:hue(x))
    instructions = [f"{palete_height}x{palete_width}"]
    row = 0
    col = 0

    for color in colors:

        if (((w + x_spacing)*col) + w) > palete_width:
            row += 1
            col = 0
            instructions.append(rect_poly_line(layer=0,w=w,h=h, topleft=((w + x_spacing)*col, (h + y_spacing)*(row)), color=tuple(color)))
        else:
            instructions.append(rect_poly_line(layer=0,w=w,h=h, topleft=((w + x_spacing)*col, (h + y_spacing)*(row)), color=tuple(color)))
            col += 1

    return instructions


def create_color_palette_image_raw(filename : str, output_name : str, n_samples :int, radius=1):
    from skimage.morphology import disk

    image_path = find_file(foldername="media", filename=filename)
    #image = io.imread(image_path)
    #image = io.imread(image_path)
    image = np.asarray(
        Image.open(image_path).convert("RGBA")
    )
    collected_colors = []
    for _ in range(n_samples):
        colors = sample_colors(image, disk(radius, strict_radius=True), radius=radius)
        count = len(colors)
        for color in colors:
            r, g, b, a = tuple(color)
            already_gotten = False
            for collected_color in collected_colors:
                r2, g2, b2, a2 = tuple(collected_color)
                if r == r2 and g == g2 and b == b2 and a == a2:
                    already_gotten = True
            if not (already_gotten):
                collected_colors.append(color)
    rel, abs_=resolve_path(foldername="objects", filename="generated_palete.poly")
    overwrite_file(abs_, create_palette_image_instructions(collected_colors))
    from buffers.drawing import Drawing
    from helpers.polyfile_reader import read_polyfile

    calls = read_polyfile("generated_palete.poly")
    HEIGHT, WIDTH = calls[0]["size"]
    drawing = Drawing(HEIGHT, WIDTH)
    calls = calls[1:]
    for call in calls:
        getattr(drawing, "poly")(**call.get("poly"))

    image = drawing.clean_image(disk(0))

    drawing.imsave(resolve_path(foldername="media", filename=f"{output_name}.png")[0], image)


def create_color_palette_image_avg(filename : str, output_name : str, n_samples :int, radius=1):
    from skimage.morphology import disk

    image_path = find_file(foldername="media", filename=filename)
    #image = io.imread(image_path)
    #image = io.imread(image_path)
    image = np.asarray(
        Image.open(image_path).convert("RGBA")
    )
    color_averages = []
    for _ in range(n_samples):
        average_red=0
        average_green=0
        average_blue=0
        average_alpha=0
        colors = sample_colors(image, disk(radius, strict_radius=True), radius=radius)
        count = len(colors)
        for color in colors:
            r, g, b, a = tuple(map(int, color))
            average_red += r
            average_green += g
            average_blue += b
            average_alpha += a
        average_red /=count
        average_green /=count
        average_blue /=count
        average_alpha /=count
        average_color_from_sample = list(map(int, [average_red, average_green, average_blue, average_alpha]))
        #print(average_color_from_sample)
        if not (average_color_from_sample in color_averages):
            color_averages.append(average_color_from_sample)
    rel, abs_=resolve_path(foldername="objects", filename="generated_palete.poly")
    overwrite_file(abs_, create_palette_image_instructions(color_averages))
    from buffers.drawing import Drawing
    from helpers.polyfile_reader import read_polyfile

    calls = read_polyfile("generated_palete.poly")
    HEIGHT, WIDTH = calls[0]["size"]
    drawing = Drawing(HEIGHT, WIDTH)
    calls = calls[1:]
    for call in calls:
        getattr(drawing, "poly")(**call.get("poly"))

    image = drawing.clean_image(disk(0))

    drawing.imsave(resolve_path(foldername="media", filename=f"{output_name}.png")[0], image)
"""
if __name__ == "__main__":
    N=10
    from skimage.morphology import disk
    def count_ones(mask : np.ndarray) -> int:
        ones = 0
        for row in mask:
            ones += list(row).count(1)
        return ones
    pixel_count = 447*447
    create_color_palette_image("images.jpeg", f"stone_palette", n_samples=(pixel_count//count_ones(disk(5)) + 1), radius=5)
"""

if __name__ == "__main__":
    height = 128
    width = 128
    mask = disk(1)
    mask_buffer = np.zeros((height, width), dtype=bool)
    clip(mask_buffer, mask, width, height)