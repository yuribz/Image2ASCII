import os, sys

import numpy as np
from PIL import Image, ImageFilter


im = Image.open("awesome.png")

def pix_avg(pix):
    if pix[3] == 0:
        return pix
    else:
        avg = np.mean(pix[:3])
        return np.array([avg, avg, avg, pix[3]])

def to_grayscale(img_arr):
    return np.apply_along_axis(pix_avg, 2, img_arr)

newim = Image.fromarray(
    to_grayscale(
        np.asarray(im)
        )
    )

newim = newim.resize(
    (256, 128)
)

char_threshold = {
    0: ".",
    50: ":",
    100: "O",
    150: "Z",
    200: "8",
    250: "#"
}

def pix_to_asc(pix):
    val = (pix[0] // 50) * 50
    return char_threshold[val]

def to_ascii(img_arr):
    return np.apply_along_axis(pix_to_asc, 2, img_arr)
    
ascii = to_ascii(np.asarray(newim))

shape = ascii.shape

if os.path.exists("output.txt"):
    os.remove("output.txt")

with open("output.txt", "w") as f:
    for i in range(shape[0]):
        for j in range(shape[1]):
            f.write(ascii[i, j])
        if i != shape[0] - 1:
            f.write("\n")