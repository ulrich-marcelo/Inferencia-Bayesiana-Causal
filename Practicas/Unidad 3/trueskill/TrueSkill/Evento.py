# -*- coding: utf-8 -*-
import math
import numpy as np
from copy import copy
from functools import reduce
from Gaussiana import Gaussian, norm

BETA = 1.0  # El desvío estándar del desempeño: N(desempeño |
# mu=habilidad, sd=BETA).


class Evento(object):
    #
    # Constructor
    def __init__(self, equipos):
        # Ejemplo:
        # equipos = [ [priorA, priorB], [priorC]  ]
        # donde el el orden indica qué equipo ganó.
        self.equipos = equipos
        self.desemp_indiv = None
        self.desemp_equip = None
        self.dif_equip = None
        self.marg_dif = None
        self.likeli_dif = None
    #
    # Representación

    def __repr__(self):
        return f'{self.equipos}'
    #

    def desempeño_individuos(self):
        # Genera todos los desempeños sumando ruido a las habilidades
        res = []
        ruido = Gaussian(0, BETA)
        for equipo in self.equipos:
            eq = []
            for habilidad in equipo:  # Contenedor de equipo
                eq.append(habilidad + ruido)
            res.append(eq)
        self.desemp_indiv = res
        return res
    #

    def desempeño_equipos(self):
        # Suma de los desempeños individuales
        res = []
        for equipo in self.desempeño_individuos():
            res.append(reduce(lambda x, y: x + y, equipo))
        self.desemp_equip = res
        return res
    #

    def diferencia_equipos(self):
        ta, tb = self.desempeño_equipos()
        d = ta - tb
        self.dif_equip = d
        return ta - tb
    #

    def marginal_diferencia(self):
        # P(diferencia, resultado) = P(diferencia) > 0
        aprox = self.diferencia_equipos() > 0
        self.marg_dif = aprox
        return aprox
    #

    def likelihood_diferencia(self):
        # Likelihood = P(diferencia, resultado) / P(diferencia)
        self.likeli_dif = self.marginal_diferencia() / self.dif_equip
        return self.likeli_dif
    #

    def likelihood_equipos(self):
        # I(d = ta - tb) Diferencia entre los desempeños de los equipos
        d = self.likelihood_diferencia()
        ta, tb = self.desemp_equip
        # ta = tb + d; tb = ta - d
        return tb + d, ta - d
    #

    def likelihood_individuos(self):
        evento = self
        #
        likelihood_equipos = evento.likelihood_equipos()
        desempeño_individuos = evento.desempeño_individuos()
        #
        res = []
        for e in range(len(evento.equipos)):
            desempeños_jugadores = desempeño_individuos[e]
            likelihood_equipo = []
            for i in range(len(evento.equipos[e])):
                desemp_equipo = copy(desempeños_jugadores)
                desemp_equipo.pop(e)
                desemp_resto = reduce(lambda x, y: x + y, desemp_equipo)
                # te = p1 + p2 + p3
                #        <=>
                # p1 = te - (p2 + p3)
                te = likelihood_equipos[e]
                likelihood_jugador = te - desemp_resto
                likelihood_equipo.append(likelihood_jugador)
            res.append(likelihood_equipo)
        self.likeli_ind = res
        return res
    
    def likelihood_habilidad(self):
        likelihood_desempeños = self.likelihood_individuos()
        ruido = Gaussian(0,BETA)
        res = []
        for e in range(len(self.equipos)):
            habilidades_equipo = []
            for i in range(len(self.equipos[e])):
                habilidad_indiv = likelihood_desempeños[e][i] - ruido
                habilidades_equipo.append(habilidad_indiv)
            res.append(habilidades_equipo)
        return res


    #
    @property
    def posterior(self):
        likelihood = self.likelihood_habilidad()
        prior = self.equipos
        #
        res = []
        for e in range(len(prior)):
            post_equipo = []
            for i in range(len(prior[e])):
                post_equipo.append(likelihood * prior[e][i])
            res.append(post_equipo)
        return res


priorA = Gaussian(3, 1)
priorB = Gaussian(2, 1)
priorC = Gaussian(6, 1)
Equipo1, Equipo2 = Evento([[priorA, priorB], [priorC]]).posterior
#print(Equipo1)
#[N(mu=3.439, sigma=0.938), N(mu=2.439, sigma=0.938)]
#print(Equipo2)
#[N(mu=5.561, sigma=0.938)]

