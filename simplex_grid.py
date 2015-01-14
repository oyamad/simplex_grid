"""
Filename: simplex_grid.py

Author: Daisuke Oyama

Thie module provides a function that constructs a grid for a simplex as
well as one that determines the index of a point in the simplex.

"""
import numpy as np
import scipy.misc
from numba import jit


@jit
def simplex_grid(m, n):
    r"""
    Construct an array consisting of the integer points in the
    (m-1)-dimensional simplex
    :math:`\{x \mid x_0 + \cdots + x_{m-1} = n\}`,
    or equivalently, the m-part compositions of n, which are listed in
    lexicographic order. The total number of the points (hence the
    length of the output array) is L = (n+m-1)!/(n!*(m-1)!) (i.e.,
    (n+m-1) choose (m-1)).

    Parameters
    ----------
    m : scalar(int)
        Dimension of each point. Must be a positive integer.

    n : scalar(int)
        Number which the coordinates of each point sum to. Must be a
        nonnegative integer.

    Returns
    -------
    out : ndarray(int, ndim=2)
        Array of shape (L, m) containing the integer points in the
        simplex, aligned in lexicographic order.

    Notes
    -----
    A grid of the (m-1)-dimensional *unit* simplex with n subdivisions
    along each dimension can be obtained by `simplex_grid(m, n) / n`.

    Examples
    --------
    >>> simplex_grid(3, 4)
    array([[0, 0, 4],
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

    >>> from __future__ import division  # Omit for Python 3.x
    >>> simplex_grid(3, 4) / 4
    array([[ 0.  ,  0.  ,  1.  ],
           [ 0.  ,  0.25,  0.75],
           [ 0.  ,  0.5 ,  0.5 ],
           [ 0.  ,  0.75,  0.25],
           [ 0.  ,  1.  ,  0.  ],
           [ 0.25,  0.  ,  0.75],
           [ 0.25,  0.25,  0.5 ],
           [ 0.25,  0.5 ,  0.25],
           [ 0.25,  0.75,  0.  ],
           [ 0.5 ,  0.  ,  0.5 ],
           [ 0.5 ,  0.25,  0.25],
           [ 0.5 ,  0.5 ,  0.  ],
           [ 0.75,  0.  ,  0.25],
           [ 0.75,  0.25,  0.  ],
           [ 1.  ,  0.  ,  0.  ]])

    References
    ----------
    A. Nijenhuis and H. S. Wilf, Combinatorial Algorithms, Chapter 5,
    Academic Press, 1978.

    """
    L = num_compositions(m, n)
    out = np.empty((L, m), dtype=int)

    x = np.zeros(m, dtype=int)
    x[m-1] = n

    for j in range(m):
        out[0, j] = x[j]

    h = m

    for i in range(1, L):
        h -= 1

        val = x[h]
        x[h] = 0
        x[m-1] = val - 1
        x[h-1] += 1

        for j in range(m):
            out[i, j] = x[j]

        if val != 1:
            h = m

    return out


def simplex_index(x, m, n):
    r"""
    Return the index of the point x in the lexicographic order of the
    integer points of the (m-1)-dimensional simplex
    :math:`\{x \mid x_0 + \cdots + x_{m-1} = n\}`.

    Parameters
    ----------
    x : array_like(int, ndim=1)
        Integer point in the simplex, i.e., an array of m nonnegative
        itegers that sum to n.

    m : scalar(int)
        Dimension of each point. Must be a positive integer.

    n : scalar(int)
        Number which the coordinates of each point sum to. Must be a
        nonnegative integer.

    Returns
    -------
    idx : scalar(int)
        Index of x.

    """
    if m == 1:
        return 0

    decumsum = np.cumsum(x[-1:0:-1])[::-1]
    idx = num_compositions(m, n) - 1
    for i in range(m-1):
        if decumsum[i] == 0:
            break
        idx -= num_compositions(m-i, decumsum[i]-1)
    return idx


def simplex_index_rec(x, m, n):
    """
    Recursive version of `simplex_index`.

    """
    if m == 1:
        return 0

    # idx0: index of the first point whose 0th coordinate = x[0]
    if x[0] == 0:
        n_next = n
        idx0 = 0
    else:
        n_next = n - x[0]
        idx0 = num_compositions(m, n) - num_compositions(m, n_next)

    return idx0 + simplex_index_rec(x[1:], m-1, n_next)


def num_compositions(m, n):
    """
    The total number of m-part compositions of n, which is equal to
    (n+m-1) choose (m-1).

    Parameters
    ----------
    m : scalar(int)
        Number of parts of composition.

    n : scalar(int)
        Integer to decompose.

    Returns
    -------
    scalar(int)
        Total number of m-part compositions of n.

    """
    # github.com/scipy/scipy/blob/v0.15.0/scipy/special/basic.py#L1139
    return scipy.misc.comb(n+m-1, m-1, exact=True)
