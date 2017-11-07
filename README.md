# simplex_grid
Generate grid points on a simplex

Main part of the code has been included in
[QuantEcon.py](https://github.com/QuantEcon/QuantEcon.py) (version 0.3.7 or above):

```py
>>> import quantecon as qe
>>> qe.simplex_grid(3, 4)
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
>>> qe.simplex_index([1, 1, 2], 3, 4)
6
```
