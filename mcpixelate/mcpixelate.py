from PIL import Image
import numpy as np
import pandas as pd

from mcpixelate.constants import COLORS
from mcpixelate import utils


class PixelImage:
    def __init__(self, image_file_path, width_blocks, ul_x=0, ul_y=0):
        '''
        Class containing data and methods for turning any image into an array of Minecraft blocks.
        This class is useful for creating murals in game, as it gives coordinates of where each block should be.

        Parameters
        ----------
        image_file_path: file path to image to be pixelated
        width_blocks: width of pixelated image in blocks (height is calculated to maintain aspect ratio)
        ul_x = x coordinate of upper left corner of where the pixelated image will be built in Minecraft
        ul_y = y coordinate of upper left corner of where the pixelated image will be built in Minecraft
        '''

        self.ul_x = ul_x
        self.ul_y = ul_y
        self.width_blocks = width_blocks

        # processing the image and obtaining the native resolution
        self.original_image = Image.open(image_file_path)
        self.orig_resolution = self.original_image.size

        # calculating modified resolution based on width_blocks
        self.scale_factor = width_blocks / self.orig_resolution[0]
        self.modified_resolution = (self.width_blocks, int(
            np.floor(self.orig_resolution[1] * self.scale_factor)))

        # creating the pixelated version of the image
        self.pixelated = self.original_image.resize(
            self.modified_resolution)
        self.pixelated_scaled = self.pixelated.resize(
            self.orig_resolution, Image.NEAREST)

        # call get_rgbs to obtain the original RGB values for each pixel from the pixelated image
        self.rgbs = utils.get_rgbs(self.pixelated)

        # match each pixel to the closest Minecraft color
        matching = utils.match_image(self.rgbs)
        self.minecraft_blocks = matching[0]
        self.minecraft_rgbs = matching[1]

        # dictionary for storing counts of each Minecraft block needed
        self.blocks_needed = {
            "white_conc": 0,
            "orange_conc": 0,
            "magenta_conc": 0,
            "lightblue_conc": 0,
            "yellow_conc": 0,
            "lime_conc": 0,
            "pink_conc": 0,
            "gray_conc": 0,
            "lightgray_conc": 0,
            "cyan_conc": 0,
            "purple_conc": 0,
            "blue_conc": 0,
            "brown_conc": 0,
            "green_conc": 0,
            "red_conc": 0,
            "black_conc": 0,
            "white_terr": 0,
            "orange_terr": 0,
            "magenta_terr": 0,
            "lightblue_terr": 0,
            "yellow_terr": 0,
            "lime_terr": 0,
            "pink_terr": 0,
            "gray_terr": 0,
            "lightgray_terr": 0,
            "cyan_terr": 0,
            "purple_terr": 0,
            "blue_terr": 0,
            "brown_terr": 0,
            "green_terr": 0,
            "red_terr": 0
        }

        # adding blocks to dictionary
        for i in self.minecraft_blocks:
            for j in i:
                self.blocks_needed[j] += 1

    def display_blocks_needed(self):
        '''
        Method for displaying how many of each type of block are needed to create the image in-game
        '''

        total = 0

        for i in self.blocks_needed.keys():
            if self.blocks_needed[i] > 0:
                print("{}: {}".format(i, self.blocks_needed[i]))
                total += self.blocks_needed[i]

        print("")
        print("Total: {}".format(total))

    def save_image(self, fname):
        '''
        Method saving the Minecraft-colored pixelated image

        Parameters
        ----------
        fname: file name/path for saving the image
        '''
        img = Image.fromarray(np.array(self.minecraft_rgbs, dtype=np.uint8)).resize(
            self.original_image.size)
        img.save(fname)

    def csv_coords(self, fname):
        '''
        Method for saving color and coordinates of each block to a .csv file for reference when building in-game

        Parameters
        ----------
        fname: file name/path for saving the .csv file
        '''

        x_coords = []
        y_coords = []
        blocks = []
        for rownum in range(len(self.minecraft_blocks)):
            for i, value in enumerate(self.minecraft_blocks[rownum]):
                x_coords.append(self.ul_x + i)
                y_coords.append(self.ul_y - rownum)
                blocks.append(value)
        pd.DataFrame(data={"X": x_coords, "Y": y_coords,
                           "Block": blocks}).to_csv(fname, index=False)
