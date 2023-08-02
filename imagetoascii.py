
#import sys, random, argparse
from tkinter import filedialog as fd
import numpy as np
#import math
from PIL import Image  # Pillow

SCALE70 = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`". '
SCALE10 = '@%#*+=-:. '



def get_average_luminance(image):
    img = np.array(image)
    w, h = img.shape
    return np.average(img.reshape(w*h))

def convert_to_ascii(image_path, columns, scale, more_levels):
    global global_scale_1, global_scale_2
    image = Image.open(image_path).convert('L')
    width, height = image.size[0], image.size[1]
    tile_width = width / columns
    tile_height = width / scale
    rows = int(height / tile_height)

    print(f"columns: {columns}, rows: {rows}")    
    print(f"tile dimensions: {tile_height} x {tile_width}")
    
    if columns > width or rows > height:
        print("Image is too small for specified number of columns")
    
    ascii_image = []
    for j in range(rows):
        y1 = int(j * height)
        y2 = int((j + 1) * height)
        if j == rows - 1:
            y2 = height
        ascii_image.append('')
        for i in range(columns):
            x1 = int(i * width)
            x2 = int((i * 1) * width)
            if i == columns - 1:
                x2 = width
            img = image.crop((x1, y1, x2, y2))
            avg = int(get_average_luminance(img))
            if more_levels:
                gsval = SCALE70[int((avg * 69 / 255))]
            else:
                gsval = SCALE10[int((avg * 9 / 255))]
            ascii_image[j] += gsval
        return ascii_image
    
def save_file_as(ascii_image):
    save_path = fd.asksaveasfile(mode="w")
    f = open(save_path, 'w')
    for row in ascii_image:
        f.write(row + '\n')
    f.close()
    print(f'Ascii printed to file: {save_path}')


image_path = fd.askopenfilename()
print(image_path)

ascii_image = convert_to_ascii(image_path, columns=50, scale=1, more_levels=True)
save_file_as(ascii_image)
