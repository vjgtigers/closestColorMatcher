from itertools import combinations
import itertools
import math

from extraFuncts import enable_vt_mode, rgb_background_block

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

allMaxMatchAttempt = (138, 53, 61)

finalColorMatch = rgb(210, 130, 137)

current = [0,0,0]

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


def oneColorCalc(values):
    val = values[0]
    color = RGB_colors[val]
    #for i in range(10):
    #    percent = (10-i)*10
    return Colors(f"{val}-100%", color)

def twoColorCalc(values):
    val1 = values[0]
    val2 = values[1]
    color1 = RGB_colors[val1]
    color2 = RGB_colors[val2]
    colors = []

    for i in range(10):
        color1percent = (10-i)

        for j in range(10):
            color2percent = (10-j)
            #print(color1percent,color2percent)
            R = math.floor((color1[0]*color1percent+color2[0]*color2percent)/(color1percent+color2percent))
            G = math.floor((color1[1]*color1percent+color2[1]*color2percent)/(color1percent+color2percent))
            B = math.floor((color1[2]*color1percent+color2[2]*color2percent)/(color1percent+color2percent))
            rgbColor = (R, G, B)
            colors.append(Colors(f"({val1}-{color1percent*10}%, {val2}-{color2percent*10}%)", rgbColor))

    return colors

def threeColorCalc(values):
    val1 = values[0]
    val2 = values[1]
    val3 = values[2]
    color1 = RGB_colors[val1]
    color2 = RGB_colors[val2]
    color3 = RGB_colors[val3]
    colors = []

    for i in range(10):
        color1percent = (10-i)

        for j in range(10):
            color2percent = (10-j)

            for k in range(10):
                color3percent = (10-k)

                R = math.floor((color1[0]*color1percent+color2[0]*color2percent+color3[0]*color3percent)/(color1percent+color2percent+color3percent))
                G = math.floor((color1[1]*color1percent+color2[1]*color2percent+color3[1]*color3percent)/(color1percent+color2percent+color3percent))
                B = math.floor((color1[2]*color1percent+color2[2]*color2percent+color3[2]*color3percent)/(color1percent+color2percent+color3percent))
                rgbColors = (R, G, B)

                colors.append(Colors(f"({val1}-{color1percent * 10}%, {val2}-{color2percent * 10}%, {val3}-{color3percent * 10}%)", rgbColors))

    return colors
# Press the green button in the gutter to run the script.


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


    print(RGB_colors["wineberry"][0])
    for key, value in RGB_colors.items():
        print(key, value)
        for i in range(3):
            current[i] = current[i] + value[i]*10


print(current)
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
allColors.extend([oneColorCalc(i) for i in all_sets1])
for i in all_sets2:
    allColors.extend(twoColorCalc(i))

for i in all_sets3:
    allColors.extend(threeColorCalc(i))

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
baseline = threeColorCalc(all_sets3[0])
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
