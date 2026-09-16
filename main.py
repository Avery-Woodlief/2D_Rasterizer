def color_palette():
    from buffers.drawing import Drawing
    from helpers.polyfile_reader import read_polyfile

    calls = read_polyfile("generated_palete.poly")
    HEIGHT, WIDTH = calls[0]["size"]
    drawing = Drawing(HEIGHT, WIDTH)
    calls = calls[1:]
    for call in calls:
        getattr(drawing, "poly")(**call.get("poly"))

    from skimage.morphology import disk

    image = drawing.clean_image(disk(0))
    drawing.imsave("generated_palete", image)

import numpy as np
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

def clip_general(buffer : np.ndarray, mask:np.ndarray, topleft : tuple[int, int]):
    buffer_h, buffer_w = buffer.shape
    mask_h, mask_w = mask.shape
    x, y = topleft # in terms of buffer coordinate system

    bx1 = x
    bx2 = x + mask_w
    by1 = y
    by2 = y + mask_h

    mx1 = 0
    mx2 = mask_w
    my1 = 0
    my2 = mask_h
    clipped = False

    if x + mask_w > buffer_w:
        #print("right")
        i = (x + mask_w) - buffer_w
        bx2 -= i
        mx2 -= i
        clipped = True

    if y + mask_h > buffer_h:
        #print("bottom")
        i = (y + mask_h) - buffer_h
        by2 -= i
        my2 -= i
        clipped = True

    if clipped:
        buffer[by1:by2,bx1:bx2] = mask[my1:my2,mx1:mx2]
    else:
        buffer[by1:by2,bx1:bx2] = mask


def count_ones(mask : np.ndarray) -> int:
    ones = 0
    for row in mask:
        ones += list(row).count(1)
    return ones

def clipping(n : int, m : int):

    from random import randint
    from skimage.morphology import disk
    from helpers.color_sampling import clip
    from utils.file_operations import find_file, overwrite_file


    height = 256
    width = 512
    radius = 16
    mask = disk(radius)

    capture = []

    c = 0
    tot = m

    for __ in range(m):
        file_ = np.zeros((height, width), dtype=bool)
        for _ in range(n):
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            mask_buffer = np.zeros((height, width), dtype=bool)
            #clip_circle_mask(mask_buffer, mask, radius, (x, y), width, height)
            clip_general(mask_buffer, mask, (x, y))
            file_ |= mask_buffer.astype(bool)

        hits = count_ones(file_)
        misses = (height*width) - hits
        capture_clip_general = f"Captured {(hits / (misses + hits)) * 100:.2f}% - clip_general"

        a = (hits / (misses + hits))

        file_ = np.zeros((height, width), dtype=bool)
        for _ in range(n):
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            mask_buffer = np.zeros((height, width), dtype=bool)
            clip_circle_mask(mask_buffer, mask, radius, (x, y), width, height)
            #clip_general(mask_buffer, mask, (x, y))
            file_ |= mask_buffer.astype(bool)

        hits = count_ones(file_)
        misses = (height*width) - hits
        capture_clip_circle_mask = f"Captured {(hits / (misses + hits)) * 100:.2f}% - clip_circle_mask"

        b = (hits / (misses + hits))

        if b > a:
            c += 1

        capture.append([capture_clip_general, capture_clip_circle_mask])
    capture.append([f"clip_circle_mask won {(c/tot) * 100}% of the time"])
    overwrite_file(find_file(filename="pretty_buffer_example.txt"), capture)


if __name__ == "__main__":
    clipping(50, 20)