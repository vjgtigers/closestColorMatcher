from itertools import combinations
import itertools
import math
import argparse
from extraFuncts import enable_vt_mode, rgb_background_block
import json
import re

parser = argparse.ArgumentParser(prog="Closest Color Matcher", description="Program to get closest matching color from provided options", epilog="Created by Vaughn Gugger")
parser.add_argument("path", help="Path to file containing RGB colors for calculations, please either modify or see colorOptions.json for file formatting")
parser.add_argument("matchColor", help="RGB color value you want to match in '(34, 233, 87)' style format")
parser.add_argument("-s", "--steps", type=int, default=10, help="Number of steps to calculate colors with. Ex, 1=just 100%%, 2= 100%% and 50%%, 10= 100,90,80...%%")
parser.add_argument("-o", "-output", type=str, default="colorCalcSave.txt", help="File path to save output to")
args = parser.parse_args()
#color values used in colorOptions.json are pulled from https://www.lipnpour.com/products/create-your-lip-product

def rgb(r,g,b):
    return (r,g,b)

#these colors are pulled from https://www.lipnpour.com/products/create-your-lip-product
RGB_colors = {
    "wineberry" : rgb(127, 41, 45),
    "red-red" : rgb(180, 65, 63),
    "blackberry" : rgb(107, 54, 77),
    "magenta" : rgb(204, 30, 126),
    "ruby red": rgb(185, 10, 77),
    "coral":rgb(209, 70, 118),
    "crimson":rgb(212, 67, 72),
    "flame":rgb(214, 55, 8),
    "paprika":rgb(202, 41, 36),
    "peach":rgb(235, 178, 129),
    "russet":rgb(155, 74, 60),
    "tangerine":rgb(234, 76, 10),
    "black":rgb(0, 0, 0),
    "blueberry":rgb(8, 98, 155),
    "brown":rgb(94, 63, 36),
    "sapphire":rgb(39, 40, 150),
    "mahogany":rgb(98, 51, 40),
    "marigold":rgb(234, 192, 8),
    "cocoa":rgb(106, 79, 71),
    "ochre":rgb(170, 122, 9),
    "white":rgb(255, 255, 255),
}
with open("colorOptions.json", "w") as f:
    text = json.dumps(RGB_colors, indent=4)
    pattern = r"\[\s+((?:-?\d+(?:\s*,\s*)?)+)\s+]"
    text = re.sub(pattern, lambda m: "[" + " ".join(m.group(1).split()) + "]", text)
    f.write(text)

print("happenig now!")
with open("colorOptions.json", "r") as f:
    colors = json.load(f)
    print(colors)
    print(colors["white"])
    RGB_values_new = {}
    for key, value in colors.items():
        RGB_values_new[key] = tuple((value[0], value[1], value[2]))
    print("*"*100)
    print(RGB_values_new)
finalColorMatch = rgb(210, 130, 137)
print("--")
print(RGB_colors)
print("---")
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


def multiColorCalc(values, steps = 10):

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


if __name__ == '__main__':
    ok = enable_vt_mode()
    if not ok:
        print("Warning: couldn't enable ANSI VT mode. Try using Windows Terminal or a modern console.")




all_sets1 = []
all_sets2 = []
all_sets3 = []
all_sets1.extend(combinations(RGB_colors.keys(), 1))
all_sets2.extend(combinations(RGB_colors.keys(), 2))
all_sets3.extend(combinations(RGB_colors.keys(), 3))




print(all_sets1)
allColors = []
#for i in all_sets1:
#    allColors.append(oneColorCalc(i))
allColors.extend([multiColorCalc(i) for i in all_sets1])
for i in all_sets2:
    allColors.extend(multiColorCalc(i))

for i in all_sets3:
    allColors.extend(multiColorCalc(i))

lowestColor = 999
lowestColorName = None

allClose = []

print("-"*100)
for i in allColors:
    distance = i.getDistanceFrom(finalColorMatch)
    if distance<lowestColor:
        lowestColor = distance
        lowestColorName=i
    if distance <= 5:
        allClose.append(i)

for i in allClose:
    print(i, i.getDistanceFrom(finalColorMatch), end=" ")
    rgb_background_block(i.color[0], i.color[1], i.color[2], 20, 1)
print("-"*100)
print(lowestColorName, lowestColorName.getDistanceFrom(finalColorMatch), end=" ")
rgb_background_block(lowestColorName.color[0], lowestColorName.color[1], lowestColorName.color[2], 10, 1)
#twoColorCalc(all_sets2[0])


print("NEW funciton testing")
print("-"*100)
baseline = multiColorCalc(all_sets3[0])
test = multiColorCalc(all_sets3[0])
print(baseline[0], test[0])

print(len(baseline), len(test))
for i in range(len(baseline)):
    if baseline[i].color == test[i].color and baseline[i].name == test[i].name: continue
    else:
        print("FAILED")
        exit(4)
print(baseline[0])
print(test[0])
if baseline == test:
    print('Equals')
rgb_background_block(20, 160, 150, width=30, height=8)
