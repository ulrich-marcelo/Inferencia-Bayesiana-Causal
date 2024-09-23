# -*- coding: utf-8 -*-
import math
import numpy as np
from Gaussiana import *

BETA = 1.0 # El desvío estándar del desempeño: N(desempeño | mu=habilidad, sd=BETA).

class Evento(object):
    #
    # Constructor
    def __init__(self, equipos):
        # Ejemplo:
        # equipos = [ [priorA, priorB], [priorC]  ]
        # donde el el orden indica qué equipo ganó.
        self.equipos = equipos
    #
    # Representación
    def __repr__(self):
        return f'{self.equipos}'
    #
    @property
    def desempeño_individuos(self):
        # Genera todos los desempeños sumando ruido a las habilidades
        res = []
        ruido = Gaussian(0,BETA)
        for equipo in self.equipos:
            res.append([]) # Contenedor de equipo
            for habilidad in equipo:
                # ...
        raise NotImplementedError("Implementar el método desempeño_individuos")
    #
    @property
    def desempeño_equipos(self):
        # Suma de los desempeños individuales
        res = []
        for equipo in self.desempeño_individuos:
            # ta = \sum_i pi
            # ...
        raise NotImplementedError("Implementar el método desempeño_equipos")
    #
    @property
    def diferencia_equipos(self):
        ta, tb = self.desempeño_equipos
        # d = ta - tb
        raise NotImplementedError("Implementar el método desempeño_equipos")
    #
    @property
    def marginal_diferencia(self):
        # P(diferencia, resultado) = P(diferencia) > 0
        raise NotImplementedError("Implementar el método marginal_diferencia")
    #
    @property
    def likelihood_diferencia(self):
        # Likelihood = P(diferencia, resultado) / P(diferencia)
        raise NotImplementedError("Implementar el método likelihood_diferencia")
    #
    @property
    def likelihood_equipos(self):
        # I(d = ta - tb) Diferencia entre los desempeños de los equipos
        ta, tb = self.desempeño_equipos
        d = self.likelihood_diferencia
        # ta = tb + d; tb = ta - d
        raise NotImplementedError("Implementar el método likelihood_equipos")
    #
    @property
    def likelihood_individuos(self):
        evento = self
        #
        desempeño_individuos = evento.desempeño_individuos
        desempeño_equipos = evento.desempeño_equipos
        likelihood_equipos = evento.likelihood_equipos
        #
        res = []
        for e in range(len(evento.equipos)):
            res.append([])
            for i in range(len(evento.equipos[e])):
                # te = p1 + p2 + p3
                #        <=>
                # p1 = te - (p2 + p3)
                te = likelihood_equipos[e]
                equipo_sin_i = desempeño_equipos[e].exclude(self.equipos[e][i])
                # ...
        raise NotImplementedError("Implementar el método likelihood_individuos")
    #
    @property
    def posterior(self):
        likelihood = self.likelihood_individuos
        prior = self.equipos
        #
        res = []
        for e in range(len(prior)):
            res.append([])
            for i in range(len(prior[e])):
            # ...
        raise NotImplementedError("Implementar el método posterior")

priorA = Gaussian(3,1)
priorB = Gaussian(2,1)
priorC = Gaussian(6,1)
Equipo1, Equipo2 = Evento([ [priorA, priorB], [priorC]]).posterior
#print(Equipo1)
#[N(mu=3.439, sigma=0.938), N(mu=2.439, sigma=0.938)]
#print(Equipo2)
#[N(mu=5.561, sigma=0.938)]

