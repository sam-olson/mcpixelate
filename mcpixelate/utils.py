from PIL import Image
import numpy as np
import pandas as pd

from mcpixelate.constants import COLORS


def get_rgbs(image):
    '''
    Function for obtaining RGB values from an image and storing them in a 2D array

    Parameters
    ----------
    image: a PIL Image object of the image to be analyzed

    Returns
    --------
    2D array of RGBs
    '''

    width = image.size[0]
    height = image.size[1]

    # convert to RGB values
    image = image.convert("RGB")
    rgbs = []

    # extract RGB data for each pixel
    for j in range(height):
        row = []
        for i in range(width):
            row.append(image.getpixel((i, j)))
        rgbs.append(row)

    return rgbs


def match_color(color, color_choices):
    '''
    Function for finding closest matching Minecraft color

    Parameters
    ----------
    color: color to be matched (must be a tuple)
    color_choices: a dictionary of colors to compare against (i.e. Minecraft terracotta and concrete RGB values)

    Returns
    -------
    Name of Minecraft block closest to given color
    '''

    minimum = [None, 1000000]

    # iterate through each color...
    for i in color_choices.keys():
        rgb = color_choices[i]
        diff = 0

        # calculate "distance" of color of interest to current color
        for a, b in zip(color, rgb):
            diff += (b - a)**2

        # if the color difference is lower than current minimum, update
        if diff < minimum[1]:
            minimum = [i, diff]

    # return the color name
    return minimum[0]

def match_image(rgbs):
    '''
    Function for finding all Minecraft color matches in a given image

    Parameters
    ----------
    rgbs: 2D array of RGB values (usually the output of get_rgbs)

    Returns
    -------
    2D array of match names and match RGBs
    '''

    all_matches = []
    all_matches_rgb = []

    width = len(rgbs[0])
    height = len(rgbs)

    # loop through each RGB value
    for j in range(height):
        row = []
        row_rgb = []
        for i in range(width):

            # find closest match
            mtch = match_color(rgbs[j][i], COLORS)

            # add data to array
            row.append(mtch)
            row_rgb.append(COLORS[mtch])

        all_matches.append(row)
        all_matches_rgb.append(row_rgb)
    return [all_matches, all_matches_rgb]

