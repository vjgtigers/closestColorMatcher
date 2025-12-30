from itertools import combinations
import argparse
from extraFuncts import enable_vt_mode, rgb_background_block, validateColorList, Colors, multiColorCalc
import json


parser = argparse.ArgumentParser(prog="Closest Color Matcher", description="Program to get closest matching color from provided options", epilog="Created by Vaughn Gugger")
parser.add_argument("path", help="Path to file containing RGB colors for calculations, please either modify or see colorOptions.json for file formatting")
parser.add_argument("matchColor", help="RGB color value you want to match in '[34, 233, 87]' style format")
parser.add_argument("-s", "--steps", type=int, default=10, help="Number of steps to calculate colors with. Ex, 1=just 100%%, 2= 100%% and 50%%, 10= 100,90,80...%%")
parser.add_argument("-o", "--output", type=str, help="File path to save output to")
parser.add_argument("--displayResults", action="store_true", help="Display program output to console as well")
parser.add_argument("--altOptionsMax", type=int, default=5, help="Other than the best value, display other options within this distance from color")

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
allColors.extend([multiColorCalc(i, RGB_colors, args.steps) for i in baseColorOptions])


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

for i in allColors:
    distance = i.getDistanceFrom(finalColorMatch)
    if distance<lowestColor:
        lowestColor = distance
        lowestColorName=i
    if distance <= args.altOptionsMax:
        allClose.append(i)

allClose = sorted(allClose, key=lambda x: x.getDistanceFrom(finalColorMatch), reverse=True)

if args.displayResults == True and args.altOptionsMax>0:
    print("-"*100)
    for i in allClose:
        rgb_background_block(i.color[0], i.color[1], i.color[2], 20, 1, end=False)
        print(f"Distance: {i.getDistanceFrom(finalColorMatch)}", i)
    print("-"*100)
    rgb_background_block(lowestColorName.color[0], lowestColorName.color[1], lowestColorName.color[2], 20, 1, end=False)
    print(f"Distance: {lowestColorName.getDistanceFrom(finalColorMatch)}", lowestColorName)
    print("-"*100)
elif args.displayResults:
    print(f"Distance: {lowestColorName.getDistanceFrom(finalColorMatch)}", lowestColorName)


if args.output is not None:
    if args.output == args.path:
        print("Output file can not be the same as color options file")
        exit()
    with open(args.output, "w") as f:
        f.write(f"Distance: {lowestColorName.getDistanceFrom(finalColorMatch)}, {lowestColorName} \n")
        f.write("-"*50 + "\n")

        allClose.reverse()
        for i in allClose:
            f.write(f"Distance: {i.getDistanceFrom(finalColorMatch)}, {i} \n")

    print(f"Output saved to '{args.output}'")

