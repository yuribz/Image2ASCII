import sys, math

import numpy as np
from PIL import Image, UnidentifiedImageError
from pathlib import Path

# Step between channel value-to-pixel threshold
PIXEL_STEP = 12

# Numpy axes that refer to different parts of the image matrix
COLUMN_AXIS     = 0
ROW_AXIS        = 1
PIXEL_AXIS      = 2


# The size of the output image
OUTPUT_WIDTH = 256

def main(argv : list[str]):
    """
    Converts provided PNG image to an ASCII art text file.

    All images are converted to grayscale by taking an average of
    the RGB channels of every pixel. The image is then rescaled to
    specified width (height determined from original image ratio), 
    and converted to ASCII using the threshold for every specified character,
    acting as a screen tone.

    The output width can be specified with an optinal -w parameter

    @params: argv is the system arguments. The expected provided
    arguments are <the path of the input image> and the
    <the path of the output text file>.
    @throws SystemExit when the provided input file is not a PNG,
    or if the number of arguments is invalid.
    """


    def parse_arguments(argv : list[str]):
        """
        Parses the command line arguments and returns a dictionary
        with the parsed arguments.
        """
        argv : list[str] = list(argv)[1:]

        arg_dict = {}

        # Check first argument: input image

        arg_dict["inp"] = argv[0]
        argv.pop(0)

        # Check for tagged arguments

        # -w tag is used to specify width of the output image
        try:
            w_index = argv.index("-w")
            if argv[w_index + 1].isnumeric():
                arg_dict["width"] = int(argv[w_index + 1])
                argv = argv[:w_index] + argv[w_index + 2:]
            else:
                raise TypeError
        except TypeError:
            print("-w tag must be followed by a numeric argument to specify width.")
            sys.exit(1)
        except ValueError:
            pass

        # Check for the output file destination
        try:
            out : str = argv[0]
        except IndexError:
            out : str = Path(arg_dict["inp"]).stem + ".txt"
        finally:
            arg_dict["out"] = out

        return arg_dict
    
    arg_dict : dict = parse_arguments(argv=argv)

    # Input location, output destination
    inp = arg_dict["inp"]
    out = arg_dict["out"]
    
    # Try to open the input image.
    try:
        im : Image = Image.open(inp).convert(mode = "RGB")
    except FileNotFoundError:
        print("The input image was not found!")
        sys.exit(1)
    except UnidentifiedImageError:
        print("The input file is not an image supported by PIL!")
        print("See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html for supported formats.")
        sys.exit(1)
    
    # Width of the output image, as well as its ratio
    width = arg_dict.get("width", OUTPUT_WIDTH)

    # Flip the ratio, otherwise the image looks stretched
    ratio : int = int(math.ceil(im.size[0] / im.size[1])) 
    
    # Give the user an indication that something is being done
    print(f"Converting {inp} to {out}...")

    # The association between pixel values and characters to be used to represent it.
    # The threshold serves as the lower bound, i.e. pixels with values 0 to 11 will 
    # use the space character, then 12 to 23 will use a period, etc.
    char_threshold : dict[int:str] = {
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
        """
        Takes in a pixel as an np.array of size 3 and returns
        another array with every channel being the mean of the
        pixel values of the input array. The output array is
        typed to contain unsigned 8-bit integers.
        """
        avg = np.mean(pix)
        return np.array([avg, avg, avg]).astype(np.uint8)

    def to_grayscale(img_arr):
        """
        Applies the pixel mean function to every pixel in the
        provided image array.
        """
        return np.apply_along_axis(pix_avg, PIXEL_AXIS, img_arr)

    def pix_to_asc(pix):
        """
        Converts the provided pixel to a corresponding ASCII characters,
        using a table of characters defined as char_threshold.
        """
        val = (pix[0] // PIXEL_STEP) * PIXEL_STEP
        return char_threshold[val]

    def to_ascii(img_arr):
        """
        Applies the pixel-to-character conversion function to every pixel in the array.
        """
        return np.apply_along_axis(pix_to_asc, PIXEL_AXIS, img_arr)

    # Converts the image to an np.array, grayscales it, converts it back to an image and resizes it.
    newim : Image = Image.fromarray(to_grayscale(np.asarray(im))).resize((width, int(width * ratio)))

    # Convers the new image to an array and convers pixels to ASCII characters.
    ascii = to_ascii(np.asarray(newim))

    def join_rows(row):
        """
        Joins characters in every row into a single continuous string.
        """
        return str.join("", row)

    def join_cols(col):
        """
        Joins strings representing rows into a single string, divided with a new line character.
        """
        return str.join("\n", col)
    

    # Join the output image into a single output string.
    output = join_cols(
        np.apply_along_axis(
            join_rows, 
            ROW_AXIS, 
            ascii)
        )
    
    # Write the string to a file.
    with open(out, "w") as f: f.write(output)
    
    print("Success!")
    sys.exit(0)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python im2ascii <input file> <optional: output file> <optional -w tag followed by desired output image width")
        sys.exit(1)

    main(sys.argv)
