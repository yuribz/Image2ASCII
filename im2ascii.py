import os, sys

import numpy as np
from PIL import Image, ImageFilter


"""
Converts provided PNG image to an ASCII art text file.

All images are converted to grayscale by taking an average of
the RGB channels of every pixel. The image is then rescaled to
256 x 128 pixels, and converted to ASCII using the threshold
for every specified character, acting as a screen tone.

@params: argv is the system arguments. The expected provided
arguments are <the path of the input image> and the
<the path of the output text file>.
@throws SystemExit when the provided input file is not a PNG,
or if the number of arguments is invalid.
"""
def main(argv):
    inp = argv[1]
    out = argv[2]

    im = Image.open(inp)

    if im.format != "PNG":
        print("Only PNG images are supported currently.")
        sys.exit(1)


    char_threshold = {
        0: ".",
        50: ":",
        100: "O",
        150: "Z",
        200: "8",
        250: "#"
    }

    def pix_avg(pix):
        if pix[3] == 0:
            return pix
        else:
            avg = np.mean(pix[:3])
            return np.array([avg, avg, avg, pix[3]])

    def to_grayscale(img_arr):
        return np.apply_along_axis(pix_avg, 2, img_arr)

    def pix_to_asc(pix):
        val = (pix[0] // 50) * 50
        return char_threshold[val]

    def to_ascii(img_arr):
        return np.apply_along_axis(pix_to_asc, 2, img_arr)

    newim = Image.fromarray(
    to_grayscale(
        np.asarray(im)
        )
    )

    newim = newim.resize(
        (256, 128)
    )

    ascii = to_ascii(np.asarray(newim))

    shape = ascii.shape

    with open(out, "w") as f:
        for i in range(shape[0]):
            for j in range(shape[1]):
                f.write(ascii[i, j])
            if i != shape[0] - 1:
                f.write("\n")
    
    sys.exit(0)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python im2ascii <input file> <output file>")
        sys.exit(1)

    main(sys.argv)
