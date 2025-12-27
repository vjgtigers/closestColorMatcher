
import os
import sys

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


def rgb_background_block(r, g, b, width=20, height=6, char=" "):
    """
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
        print(row)
