import numpy as np
from scipy import misc

class NewSign:
    def __init__(self, pixels):
        self.pixels = pixels
        self.north, self.south, self.west, self.east = \
            self.find_borders()
        self.width = self.east - self.west
        self.height = self.south - self.north
        self.normalized = self.normalize_image()
        self.bitmap = self.make_bitmap()

    def find_borders(self):

        """find extremal values of
        coefficients"""

        return np.min(self.pixels, axis=0)[0], \
               np.max(self.pixels, axis=0)[0], \
               np.min(self.pixels, axis=0)[1], \
               np.max(self.pixels, axis=0)[1]

    def normalize_image(self):

        """normalize image as if it starts from [0, 0]"""

        return self.pixels - np.full((self.pixels.shape[0], 2),
                                    [self.north, self.west])

    def make_bitmap(self):

        """save a bitmap of separated sign"""

        bitmap = np.full((16, 16), 1.)
        for pixel in self.normalized:
            if pixel[0] < 16 and pixel[1] < 16:
                bitmap[pixel[0], pixel[1]] = 0.

        return bitmap

    def show(self):
        misc.imshow(self.bitmap)

    def save(self, id):
        misc.imsave(id + '.png', self.bitmap)
