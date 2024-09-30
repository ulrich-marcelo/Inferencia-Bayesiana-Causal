from Gaussiana import Gaussian
from functools import reduce
a = [Gaussian(0, 1), Gaussian(2, 1)]

print(reduce(lambda x, y: x + y, a))


