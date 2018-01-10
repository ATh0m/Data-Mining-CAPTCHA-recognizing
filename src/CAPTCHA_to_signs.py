
import numpy as np
from save_images import NewSign
from scipy import misc


class DFS:

    """class finding bitmaps of separated
     signs in passed image"""

    def __init__(self, img):
        self.img = misc.imread(img)
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        self.array = np.zeros((self.rows, self.cols))
        self.bin_array()
        self.visited = np.zeros((self.rows+1, self.cols+1))
        self.pixels = None
        self.id = 1

    def black_or_white(self, A):

        """convert a single array
        to black-or-white byte"""

        return np.sign(765 - np.sum(A))

    def bin_array(self):

        """convert rgb array to
        binary black-or-white array
        black: 1, white: 0"""

        for x in range(self.rows):
            for y in range(self.cols):
                self.array[x, y] = \
                    np.array(self.black_or_white(self.img[x, y]))

    def neighbours(self, point):

        """define Moore's neighbours
        in (point_x, point_y"""

        point_x, point_y = point[0], point[1]

        if point_x == 0 and point_y == 0:
            return (0, 1), (1, 1), (1, 0)
        if point_x == self.rows-1 and point_y == \
            self.cols-1:
            return (point_x-1, point_y), \
                   (point_x-1, point_y-1), \
                   (point_x, point_y-1)
        if point_x == self.rows-1 and point_y == 0:
            return (point_x-1, 0), (point_x-1, 1), \
                   (point_x, 1)
        if point_x == 0 and point_y == self.cols-1:
            return (0, point_y-1), (1, point_y-1), \
                   (1, point_y)
        if point_x == 0:
            return (0, point_y - 1), (1, point_y-1), \
                   (1, point_y), (1, point_y+1), (0, point_y+1)
        if point_y == 0:
            return (point_x-1, 0), (point_x-1, 1), \
                   (point_x, 1), (point_x+1, 1), (point_x+1, 0)
        if point_x == self.rows-1:
            return (point_x-1, point_y), (point_x-1, point_y-1), \
                   (point_x, point_y-1), (point_x-1, point_y+1), \
                   (point_x, point_y+1)
        if point_y == self.cols-1:
            return (point_x, point_y-1), (point_x-1, point_y-1), \
                   (point_x-1, point_y), (point_x+1, point_y-1), \
                   (point_x+1, point_y)

        return (point_x-1, point_y-1), (point_x-1, point_y), \
               (point_x-1, point_y+1), (point_x, point_y+1), \
               (point_x+1, point_y+1), (point_x+1, point_y), \
               (point_x+1, point_y-1), (point_x, point_y-1)

    def dfs(self, point):

        """dfs on plane with Moore's
        neighbourhood"""

        self.visited[point[0], point[1]] = 1
        for neighbour in self.neighbours(point):

            if self.array[neighbour[0], neighbour[1]] == 1\
                    and self.visited[neighbour[0],
                                     neighbour[1]] == 0:
                self.pixels.append(list(neighbour))
                self.dfs(neighbour)

    def dfs_all(self):

        """start dfs on all black pixels"""
        signs = []
        for point_y in range(self.cols):
            for point_x in range(self.rows):

                # start dfs only on black pixel

                if self.visited[point_x, point_y] == 0 and \
                                self.array[point_x, point_y] == 1:

                    self.pixels = [[point_x, point_y]]
                    self.dfs((point_x, point_y))
                    new_sign = NewSign(np.array(self.pixels))
                    signs.append(new_sign)
                    self.id += 1
        return signs


if __name__ == "__main__":
    dfs = DFS('2A2X.png')
    dfs.dfs_all()


