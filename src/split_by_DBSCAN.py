import numpy as np
from scipy import misc
from sklearn.cluster import DBSCAN
from math import sqrt
from save_images import NewSign
from operator import itemgetter


class DBScan:

    """class finding bitmaps of separated
     signs in passed image"""

    def __init__(self, img, min_samples=7):
        self.img = misc.imread(img)
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        self.array = np.zeros((self.rows, self.cols))
        self.bin_array()
        self.visited = np.zeros((self.rows+1, self.cols+1))
        self.id = 1
        self.min_samples = min_samples

    def black_or_white(self, A):

        """converts a single array
        to black-or-white byte"""

        if np.sum(A) > 400:
            return 0
        else:
            return 1

    def bin_array(self):

        """converts rgb array to
        binary black-or-white array
        black: 1, white: 0"""

        for x in range(self.rows):
            for y in range(self.cols):
                self.array[x, y] = \
                    np.array(self.black_or_white(self.img[x, y]))

    def bin_to_index(self):

        """converts 0-1 array to 1D
        array with indexes of ones
        [row, column] in 2D 0-1 array"""

        return np.array(list(zip(*np.where(self.array == 1))))

    def dbscan(self):

        """performs a dbscan clustering"""

        array_of_indexes = self.bin_to_index()
        sorted_signs = []

        # dbscan here

        db = DBSCAN(eps=sqrt(2), min_samples=self.min_samples)
        db.fit(array_of_indexes)

        n_unique_labels = np.unique(db.labels_).size

        for label in range(n_unique_labels):
            indexes = (db.labels_ == label)

            if np.count_nonzero(indexes) > 100:
                sorted_signs.append(
                    min(array_of_indexes[indexes].tolist(),
                        key=itemgetter(1)) + [label])

        # set the correct order of signs
        # sort by min value of col index

        sorted_signs.sort(key=itemgetter(1))

        signs = []
        for k in sorted_signs:
            indexes = (db.labels_ == k[2])

            new_sign = NewSign(array_of_indexes[indexes], 32)
            #new_sign.save(str(self.id))
            signs.append(new_sign)
            self.id += 1

        return signs


if __name__ == "__main__":
    dbscan = DBScan('2b83r8.png')
    dbscan.dbscan()


