from itertools import combinations
import itertools
import math
import argparse
from extraFuncts import enable_vt_mode, rgb_background_block, validateColorList
import json


parser = argparse.ArgumentParser(prog="Closest Color Matcher", description="Program to get closest matching color from provided options", epilog="Created by Vaughn Gugger")
parser.add_argument("path", help="Path to file containing RGB colors for calculations, please either modify or see colorOptions.json for file formatting")
parser.add_argument("matchColor", help="RGB color value you want to match in '[34, 233, 87]' style format")
parser.add_argument("-s", "--steps", type=int, default=10, help="Number of steps to calculate colors with. Ex, 1=just 100%%, 2= 100%% and 50%%, 10= 100,90,80...%%")
parser.add_argument("-o", "-output", type=str, default="colorCalcSave.txt", help="File path to save output to")
parser.add_argument("--displayResults", action="store_true", help="Display program output to console as well")
args = parser.parse_args()
#color values used in colorOptions.json are pulled from https://www.lipnpour.com/products/create-your-lip-product
#finalColorMatch = rgb(210, 130, 137)


#load in json file of colors
RGB_colors = {}
colorsFile = open(args.path, "r")
colors = json.load(colorsFile)
for key, value in colors.items():
    RGB_colors[key] = tuple((value[0], value[1], value[2]))


#get and validate color to match
colorList = json.loads(args.matchColor)
validateColorList(colorList)
finalColorMatch = tuple((colorList[0], colorList[1], colorList[2]))


print("Import complete")

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



#create all combinations
baseColorOptions = []
baseColorOptions.extend(combinations(RGB_colors.keys(), 1))
baseColorOptions.extend(combinations(RGB_colors.keys(), 2))
baseColorOptions.extend(combinations(RGB_colors.keys(), 3))

#preform all the real calculations
allColors = []
allColors.extend([multiColorCalc(i) for i in baseColorOptions])



#reorganize
allColorsTemp = []
for i in allColors:
    if isinstance(i, list):
        for j in i:
            allColorsTemp.append(j)
    else:
        allColorsTemp.append(i)
allColors = allColorsTemp




allClose = []
lowestColor = 999
lowestColorName = None

print("-"*100)
for i in allColors:
    distance = i.getDistanceFrom(finalColorMatch)
    if distance<lowestColor:
        lowestColor = distance
        lowestColorName=i
    if distance <= 5:
        allClose.append(i)

for i in allClose:
    rgb_background_block(i.color[0], i.color[1], i.color[2], 20, 1, end=False)
    print(f"Distance: {i.getDistanceFrom(finalColorMatch)}", i)
print("-"*100)
rgb_background_block(lowestColorName.color[0], lowestColorName.color[1], lowestColorName.color[2], 20, 1, end=False)
print(f"Distance: {lowestColorName.getDistanceFrom(finalColorMatch)}", lowestColorName)
#twoColorCalc(all_sets2[0])


print("NEW funciton testing")
print("-"*100)
#baseline = multiColorCalc(all_sets3[0])
#test = multiColorCalc(all_sets3[0])
#print(baseline[0], test[0])
#
#print(len(baseline), len(test))
#for i in range(len(baseline)):
#    if baseline[i].color == test[i].color and baseline[i].name == test[i].name: continue
#    else:
#        print("FAILED")
#        exit(4)
#print(baseline[0])
#print(test[0])
#if baseline == test:
#    print('Equals')
#rgb_background_block(20, 160, 150, width=30, height=8)
