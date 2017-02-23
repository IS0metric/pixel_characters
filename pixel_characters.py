from PIL import Image
import random
import math


"""
Returns a random RGB colour
"""
def get_colour():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r,g,b)


"""
Constructs a colour map
  Takes a list of encountered characters and constructs a dictionary with each
  character being assigned a unique colour value
"""
def assign_colours(characters):
    colour_map = {}
    used_colours = []
    for char in characters:
        if char == " " or char == "\n":
            colour = (255,255,255)
        else:
            colour = get_colour()
            while colour in used_colours:
                colour = get_colour()
        colour_map[char] = colour
    return colour_map


"""
Decides an appropriate image size based on the number of lines and the maximum
length of the lines
"""
def scale(width, height):
    factor = 0
    columns = 1
    while factor < 1:
        columns = columns * 2
        width = width * 2
        height = int(math.ceil(float(height) / 2))
        factor = float(width) / float(height)
    return (width, height, columns)


"""
Reads in a specified file and outputs a list containing each line, a list of
all encountered characters and the maximum line length
"""
def read_file(filename):
    column_width = 0
    all_lines = []
    encountered_characters = []
    f = open(filename, "r")
    line = f.readline()
    while line != '':
        line += "  "
        if len(line) > column_width:
            column_width = len(line)
        for char in line:
            if char not in encountered_characters:
                encountered_characters += [char]
        all_lines += [line]
        line = f.readline()
    f.close()
    return (all_lines, encountered_characters, column_width)


"""
Builds and saves the image
"""
def create_image(colour_map, column_width, full_height, all_lines, output):
    (width, height, columns) = scale(column_width, full_height)
    image = Image.new("RGB", (width, height), "white")
    pixels = image.load()
    current_column = 0
    for y in range(len(all_lines)):
        for x in range(len(all_lines[y])):
            x_pix = x + (column_width * current_column)
            if y != 0:
                y_pix = y % height
            else:
                y_pix = 0
            char = all_lines[y][x]
            pixels[x_pix, y_pix] = colour_map[char]
        if y_pix == height - 1:
            current_column += 1
    image.save(output+".bmp")


"""
Takes user input for the filename and output file to build the image
"""
def run_main():
    filename = raw_input("Enter a file to read in: ")
    output = raw_input("Enter a filename to output to: ")
    (all_lines, encountered_characters, column_width) = read_file(filename)
    full_height = len(all_lines)
    colour_map = assign_colours(encountered_characters)
    create_image(colour_map, column_width, full_height, all_lines, output)


if __name__ == "__main__":
    run_main()
