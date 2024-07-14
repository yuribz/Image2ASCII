import sys

import numpy as np
from PIL import Image

# Step between channel value-to-pixel threshold
PIXEL_STEP = 12

# The numpy array axis for storing the actual pixel values
PIXEL_AXIS = 2

# The size of the output image
OUTPUT_SIZE = (256, 128)

def main(argv):
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
    inp = argv[1]
    out = argv[2]

    im = Image.open(inp).convert(mode = "RGB")

    char_threshold = {
        0:      ' ',
        12:     '.',
        24:     ',',
        36:     '-',
        48:     '_',
        60:     ':',
        72:     ';',
        84:     '~',
        96:     '=',
        108:    '+',
        120:    '*',
        132:    'Z',
        144:    '%',
        156:    '&',
        168:    '8',
        180:    'B',
        192:    '@',
        204:    'W',
        216:    'M',
        228:    'X',
        240:    '$',
        252:    '#'
    }

    def pix_avg(pix):
        avg = np.mean(pix)
        return np.array([avg, avg, avg]).astype(np.uint8)

    def to_grayscale(img_arr):
        return np.apply_along_axis(pix_avg, PIXEL_AXIS, img_arr)

    def pix_to_asc(pix):
        val = (pix[0] // PIXEL_STEP) * PIXEL_STEP
        return char_threshold[val]

    def to_ascii(img_arr):
        return np.apply_along_axis(pix_to_asc, PIXEL_AXIS, img_arr)

    newim = Image.fromarray(to_grayscale(np.asarray(im))).resize(OUTPUT_SIZE)

    print(
        np.asarray(newim)[60, 60]
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

    print(
        np.asarray(Image.open(sys.argv[1]).convert(mode = "RGB"))[180, 180]
        )

    main(sys.argv)
