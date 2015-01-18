"""
Filename: test_simplex_grid.py
Author: Daisuke Oyama

Tests for simplex_grid.py

"""
import numpy as np
from numpy.testing import assert_array_equal
from nose.tools import eq_

from simplex_grid import (simplex_grid, simplex_index, simplex_index_rec,
    num_compositions)


class TestSimplexGrid:
    def setUp(self):
        self.simplex_grid_3_4 = np.array([[0, 0, 4],
                                          [0, 1, 3],
                                          [0, 2, 2],
                                          [0, 3, 1],
                                          [0, 4, 0],
                                          [1, 0, 3],
                                          [1, 1, 2],
                                          [1, 2, 1],
                                          [1, 3, 0],
                                          [2, 0, 2],
                                          [2, 1, 1],
                                          [2, 2, 0],
                                          [3, 0, 1],
                                          [3, 1, 0],
                                          [4, 0, 0]])

    def test_simplex_grid(self):
        out = simplex_grid(3, 4)
        assert_array_equal(out, self.simplex_grid_3_4)

        assert_array_equal(simplex_grid(1, 1), [[1]])

    def test_simplex_index(self):
        points = [[0, 0, 4], [1, 1, 2], [4, 0, 0]]
        for point in points:
            idx = simplex_index(point, 3, 4)
            assert_array_equal(self.simplex_grid_3_4[idx], point)

        eq_(simplex_index([1], 1, 1), 0)

    def test_simplex_index_rec(self):
        points = [[0, 0, 4], [1, 1, 2], [4, 0, 0]]
        for point in points:
            idx = simplex_index_rec(point, 3, 4)
            assert_array_equal(self.simplex_grid_3_4[idx], point)

        eq_(simplex_index_rec([1], 1, 1), 0)

    def test_num_compositions(self):
        num = num_compositions(3, 4)
        eq_(num, len(self.simplex_grid_3_4))


if __name__ == '__main__':
    import sys
    import nose

    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)
