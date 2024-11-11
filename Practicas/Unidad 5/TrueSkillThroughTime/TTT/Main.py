# -*- coding: utf-8 -*-
from Historia import *

eventos = [ [["a"],["b"]],
            [["b"],["a"]] ]

h = Historia(eventos)
for i in range(7):
    h.forward_propagation()
    h.backward_propagation()
    print(h.posteriors())