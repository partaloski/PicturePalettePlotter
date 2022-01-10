import operator
import os.path
import time

import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
hexa_vals = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']


class Pixel:
    def __init__(self, pixel):
        self.r, self.g, self.b = pixel[0:3]
        self.pixel = pixel
        self.appearances = 1
        self.rgbhex = '#' + self.to_hex(self.r) + self.to_hex(self.g) + self.to_hex(self.b)

    def to_hex(self, value):
        value = int(value)
        part1 = int(value / 16)
        part2 = int(value % 16)
        return hexa_vals[part1] + hexa_vals[part2]

    def get_value(self):
        return str(self.rgbhex)

    def get_value_alt(self):
        return str(self.r)+","+str(self.g)+","+str(self.b)

    def increment(self):
        self.appearances += 1

    def get_appearances(self):
        return self.appearances

def main():
    path = input("Input the path of the picture here, please: ")
    mode = input("If you want the barplot to show hexadecimal colours, enter anything, else, just press Enter : ")
    if os.path.isfile(path) == False:
        print("The path you entered isn't a valid file.\nThe program will quit in 5.")
        time.sleep(5)
        return
    image = Image.open(path,'r')
    pixels = list(image.getdata())
    image.close()
    pixels_dict = dict()
    pixels_list = list()
    for pixel in pixels:
        p = Pixel(pixel)
        if p.get_value() not in pixels_dict.keys():
            pixels_dict.__setitem__(p.get_value(), p)
            pixels_list.append(p)
        elif p.get_value() in pixels_dict.keys():
            pixels_dict.get(p.get_value()).increment()

    sorted_by_occurences = sorted(pixels_list, key=operator.attrgetter("appearances"))
    sorted_by_occurences.reverse()
    pixels_all = [[x.get_value(), x.get_appearances(), x.get_value_alt()] for x in sorted_by_occurences]

    dataFrame = pd.DataFrame(pixels_all)
    dataFrame.columns = ["Color", "Count", "RGB"]
    dataFrame.to_csv('data.csv')

    value_count = int(input('How many of the top colors do you want to be shown?'))
    if value_count <= 0:
        print("Value cannot be smaller than 0.\nProgram shutting down in 5 seconds")
        time.sleep(5)
        return

    df = dataFrame

    col = df['Color'].head(value_count)
    cou = df['Count'].head(value_count)
    rgb = df['RGB'].head(value_count)

    # Figure Size
    fig, ax = plt.subplots(figsize=(value_count, 20))


    if len(mode.strip()) == 0:
        # Horizontal Bar For RGB Values
        for rgb_val, color, count in zip(rgb, col, cou):
            ax.barh(rgb_val, count, color=color)
    else:
        # Horizontal Bar For HEX Values
        for color, count in zip(col, cou):
            ax.barh(color, count, color=color)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(b=True, color='#777777',
            linestyle='-.', linewidth=0.5,
            alpha=0.2)

    # Show top values
    ax.invert_yaxis()

    plt.savefig('image.png')

    print('The program is now complete, exiting in 5 seconds')

if __name__ == '__main__':
    main()
    time.sleep(5)