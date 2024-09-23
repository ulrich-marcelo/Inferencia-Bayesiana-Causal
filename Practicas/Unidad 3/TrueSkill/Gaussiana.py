# -*- coding: utf-8 -*-
"""
   TrueskillThroughTime.py
   ~~~~~~~~~~~~~~~~~~~~~~~~~~
   :copyright: (c) 2019-2024 by Gustavo Landfried.
   :license: BSD, see LICENSE for more details.
"""

import math
from scipy.stats import norm
from scipy.stats import truncnorm
from matplotlib import pyplot as plt
import numpy as np

inf = math.inf
sqrt2 = math.sqrt(2)
sqrt2pi = math.sqrt(2 * math.pi)

__all__ = ['MU', 'SIGMA', 'Gaussian', 'N01', 'N00', 'Ninf', 'Nms']

MU = 0.0
SIGMA = 6
PI = SIGMA**-2
TAU = PI * MU


def mu_sigma(tau_, pi_):
    if pi_ > 0.0:
        sigma = math.sqrt(1/pi_)
        mu = tau_ / pi_
    if pi_ == 0.0:
        sigma = inf
        mu = 0.0
    return mu, sigma


class Gaussian(object):
    #
    # Constructor
    def __init__(self, mu=MU, sigma=SIGMA):
        assert sigma >= 0, "sigma tiene que ser positivo!!"
        self.mu, self.sigma = mu, sigma
    #
    # Iterador

    def __iter__(self):
        return iter((self.mu, self.sigma))
    #
    # Print

    def __repr__(self):
        return 'N(mu={:.3f}, sigma={:.3f})'.format(self.mu, self.sigma)
    #
    # tau = mu/sigma^2

    @property
    def tau(self):
        if self.sigma == 0:
            return inf
        else:
            return self.mu / self.sigma**2
    #
    # pi = 1/sigma^2

    @property
    def pi(self):
        if self.sigma == 0:
            return inf
        else:
            return self.sigma**-2
    #
    # N > 0

    def __gt__(self, threshold):
        # Gaussiana truncada: N > 0.
        truncated_norm = truncnorm(
            (threshold - self.mu) / self.sigma, 
            inf, loc=self.mu, scale=self.sigma)
        # Devolver la Gaussiana con misma media y desvío
        return Gaussian(truncated_norm.mean(), truncated_norm.std())
    # N >= 0

    def __ge__(self, threshold):
        return self.__gt__(threshold)
    #
    # N + M

    def __add__(self, M):
        if self.sigma > 0




        raise NotImplementedError("Implementar el método N + M")
    #
    # N - M

    def __sub__(self, M):
        raise NotImplementedError("Implementar el método N - M")
    #
    # N * M

    def __mul__(self, M):
        if M.pi == 0:
            return self
        elif self.pi == 0:
            return M
        elif self.sigma > 0 and M.sigma > 0:
            new_mu = self.tau + M.tau
            new_sigma = (self.pi + M.pi)**(-1/2)
            return Gaussian(new_mu,new_sigma)

    def __rmul__(self, other):
        return self.__mul__(other)
    #
    # N / M

    def __truediv__(self, M):
        raise NotImplementedError("Implementar el método N / M")
    #
    # Forget

    def forget(self, gamma, t):
        return Gaussian(self.mu, math.sqrt(self.sigma**2 + t*gamma**2))
    #
    # Delta

    def delta(self, M):
        return abs(self.mu - M.mu), abs(self.sigma - M.sigma)
    #
    # Inverso de la suma: f^{-1}(N+M)

    def exclude(self, M):
        return Gaussian(self.mu - M.mu, math.sqrt(self.sigma**2 - M.sigma**2))
    #
    # IsApprox

    def isapprox(self, M, tol=1e-4):
        cond1 = abs(self.mu - M.mu)
        return (cond1 < tol) and (abs(self.sigma - M.sigma) < tol)


N21 = Gaussian(2, 1)
N01 = Gaussian(0, 1)
Ninf = Gaussian(0, inf)
Nms = Gaussian(MU, SIGMA)
print(N01)
print(N01 > 0)

# x_grid = np.linspace(-5, 7.5, 1000)

# plt.plot(x_grid, norm(*N01).pdf(x_grid) * (x_grid > 0))
# plt.plot(x_grid, norm(*(N01 > 0)).pdf(x_grid))
# plt.legend(["Truncada original", "Aproximacion a la truncada"])
# plt.show()

print((N01 > 0).pi)
