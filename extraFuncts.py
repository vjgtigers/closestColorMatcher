import itertools
import math
import os

def enable_vt_mode():
    """Enable ANSI / Virtual Terminal Processing on Windows (no-op on POSIX)."""
    if os.name != "nt":
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        mode = ctypes.c_uint()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        return bool(kernel32.SetConsoleMode(handle, new_mode))
    except Exception:
        return False


def rgb_background_block(r, g, b, width=20, height=6, char=" ", end=True):
    """#rgb_background_block(20, 160, 150, width=30, height=8)
    Print a rectangular block filled with background RGB color.
      - r,g,b: 0..255
      - width,height: block size in characters
      - char: the character to fill each cell with (space works well)
    Uses 24-bit background: ESC[48;2;R;G;Bm
    """
    esc = "\x1b["
    bg = f"{esc}48;2;{r};{g};{b}m"
    reset = f"{esc}0m"
    row = bg + (char * width) + reset
    # print rows; keep simple and portable
    for _ in range(height):
        if end:
            print(row)
        else:
            print(row, end=" ")
def validateColorList(colorList):
    if not isinstance(colorList, list):
        print("Incorrectly formated input for matchColor, fix and try again")
        exit()
    if len(colorList) != 3:
        print("Incorrect number of elements, fix and try again")
        exit()
    if not all(isinstance(x, int) for x in colorList):
        print("All values must be int, fix and try again")
        exit()
    if not all(0 <= x <= 255 for x in colorList):
        print("All values must be in range 0 <= x <= 255, fix and try again")
        exit()




#class def
class Colors:
    def __init__(self, colorName, colorTuple):
        self.name = colorName
        self.color = colorTuple

    def getDistancesFrom(self, colorMatch):
        sub = tuple(x - y for x, y in zip(colorMatch, self.color))
        return sub

    def getDistanceFrom(self, colorMatch):
        distances = self.getDistancesFrom(colorMatch)
        val = 0
        for i in distances:
            val+= abs(i)
        return val


    def __str__(self):
        return f"Name: {self.name}; Color: {self.color}"


def multiColorCalc(values, RGB_colors, steps = 10):

    if not values: raise ValueError("values can not be empty")

    #shortcut for if len is one
    if len(values) == 1:
        val = values[0]
        color = RGB_colors[val]
        return Colors(f"{val}-100%", color)

    #anything greater than one

    color_tuples = [RGB_colors[v] for v in values]
    names = values

    colors_out = []
    weight_range = range(steps, 0, -1)

    for weights in itertools.product(weight_range, repeat=len(values)):
        total_weight = sum(weights)

        R = math.floor(sum(c[0] * w for c, w in zip(color_tuples, weights)) / total_weight)
        G = math.floor(sum(c[1] * w for c, w in zip(color_tuples, weights)) / total_weight)
        B = math.floor(sum(c[2] * w for c, w in zip(color_tuples, weights)) / total_weight)
        rgb_value = (R, G, B)

        parts = []
        for name, w in zip(names, weights):
            percent = int(w * 100 / steps)
            parts.append(f"{name}-{percent}%")
        label = f"({', '.join(parts)})"

        colors_out.append(Colors(label, rgb_value))

    return colors_out
