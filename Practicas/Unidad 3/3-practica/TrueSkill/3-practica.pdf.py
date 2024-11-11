# -*- coding: utf-8 -*-
from Gaussiana import *

s1 = Gaussian(); s2 = Gaussian(); s3 = Gaussian(); s4 = Gaussian()
o = Gaussian(0, 1) # ruido

p1 = s1 + o; p2 = s2 + o; p3 = s3 + o; p4 = s4 + o

ta = p1 + p2; tb = p3 + p4

d = ta - tb
d_approx = d > 0

lh_d = d_approx / d

lh_ta = lh_d + tb

lh_p1 = lh_ta - p2

lh_s1 = lh_p1 - o

posterior_s1 = s1 * lh_s1

#

s1 = ttt.Gaussian(); s2 = ttt.Gaussian(); s3 = ttt.Gaussian(); s4 = ttt.Gaussian()
o = ttt.Gaussian(0, 1) # ruido
p1 = s1 + o; p2 = s2 + o; p3 = s3 + o; p4 = s4 + o
ta = p1 + p2; tb = p3 + p4
d = ta - tb
lf_d = ttt.approx(d, margin=0, tie=False)/d
lh_ta = lh_d + tb
lh_p1 = lh_ta - p2
lh_s1 = lh_p1 - o
posterior_s1_ttt = s1 * lh_s1

assert posterior_s1_ttt.isapprox(posterior_s1)



import numpy as np
from matplotlib import pyplot as plt
x_grid = np.arange(-6,6,0.01)
plt.plot(x_grid, norm(*Gaussian(2,1)).pdf(x_grid) * (x_grid>0)  )
plt.plot(x_grid, norm(*(Gaussian(2,1) > 0)).pdf(x_grid)  )
plt.show()
### N(mu=2.055, sigma=0.942)

