import numpy as np
cimport numpy as cnp

def build_triangle_mask(tuple apex_pos, cnp.ndarray[cnp.uint8_t, ndim=2] mask, int base, int height, double m1, double m3):
    cdef int Ax = apex_pos[0]
    cdef int Ay = apex_pos[1]

    cdef int x
    cdef int y
    cdef int mask_y

    cdef double Y1
    cdef double Y3

    for y in range(Ay - height, Ay):

        mask_y = Ay - y - 1

        for x in range(base):

            if x <= Ax:

                Y1 = -height + Ay + m1 * x

                if y > Y1:
                    mask[mask_y, x] = 0

            else:

                Y3 = Ay + m3 * (x - Ax)

                if y > Y3:
                    mask[mask_y, x] = 0

    return mask