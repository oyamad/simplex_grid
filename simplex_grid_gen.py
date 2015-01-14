"""
Filename: simplex_grid_gen.py

Author: Daisuke Oyama

Generator version of simple_grid.py.

"""
import numpy as np
from simplex_grid import simplex_index, num_compositions


class SimplexGrid(object):
    r"""
    Generate the integer points in the (m-1)-dimensional simplex
    :math:`\{x \mid x_0 + \cdots + x_{m-1} = n\}`,
    or equivalently, the m-part compositions of n, in lexicographic
    order.

    Parameters
    ----------
    m : scalar(int)
        Dimension of each point. Must be a positive integer.

    n : scalar(int)
        Number which the coordinates of each point sum to. Must be a
        nonnegative integer.

    Attributes
    ----------
    m, n : See Parameters

    size : scalar(int)
        Number of grid points, equal to (n+m-1)!/(n!*(m-1)!).

    Examples
    --------
    >>> simplexgrid = SimplexGrid(3, 4)
    >>> simplexgrid.size
    15
    >>> for x in simplexgrid.generate():
    ...     print x
    ...
    [0 0 4]
    [0 1 3]
    [0 2 2]
    [0 3 1]
    [0 4 0]
    [1 0 3]
    [1 1 2]
    [1 2 1]
    [1 3 0]
    [2 0 2]
    [2 1 1]
    [2 2 0]
    [3 0 1]
    [3 1 0]
    [4 0 0]
    >>> simplexgrid[2]
    array([0, 2, 2])
    >>> simplexgrid[14]
    array([4, 0, 0])
    >>> simplexgrid.get_index([0, 4, 0])
    4

    References
    ----------
    A. Nijenhuis and H. S. Wilf, Combinatorial Algorithms, Chapter 5,
    Academic Press, 1978.

    """
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.size = num_compositions(m, n)

    def generate(self):
        """
        Generate the grid points of the simplex in lexicographic order.

        Returns
        -------
        generator of ndarrays (int, ndim=1)
            Grid points of the simplex.

        """
        m, n = self.m, self.n

        x = np.zeros(m, dtype=int)
        x[m-1] = n

        h = m

        while True:
            yield x

            h -= 1
            if h == 0:
                return

            val = x[h]
            x[h] = 0
            x[m-1] = val - 1
            x[h-1] += 1
            if val != 1:
                h = m

    def __getitem__(self, idx):
        if not (0 <= idx < self.size):
            raise IndexError('index out of range')

        gen = self.generate()
        for i in range(idx):
            _ = gen.next()
        return gen.next()

    def get_index(self, x):
        r"""
        Return the index of the point x in the lexicographic order of
        the integer points in the simplex.

        Parameters
        ----------
        x : array_like(int, ndim=1)
            Integer point in the simplex.

        Returns
        -------
        idx : scalar(int)
            Index of x.

        """
        return simplex_index(x, self.m, self.n)
