# -*- coding: utf-8 -*-
from Gaussiana import *
from Habilidad import *
from Evento import *
from collections import defaultdict
import math
from copy import copy

class Historia(object):
    def __init__(self, eventos, priors=defaultdict(lambda: Gaussian(0.0, 3.0)) ):
        self.eventos = eventos
        self.priors = priors
        self.habilidades = [ [[Habilidad() for integrante in equipo] for equipo in evento] for evento in eventos]
    #
    def __repr__(self):
        return f'Historia(Eventos={len(eventos)})'
    #
    def forward_propagation(self):
        h = self
        ultimo_mensaje = copy(h.priors)
        for t in range(len(self.eventos)):
            #PRIORS
            priors_t = []
            for e in range(len(h.eventos)):
                priors_t.append([])
                for i in range(len(h.eventos[t][e])):
                    nombre = h.eventos[t][e][i]
                    priors_t[-1].append(
                        ultimo_mensaje[nombre]*h.habilidades[t][e][i].backward
                    )
            #Evento
            likelihood = Evento(priors_t).likelihood

            for e in range(len(h.eventos[t])):
                for i in range(len(h.eventos[t][e])):
                    nombre = h.eventos[t][e][i]
                    h.habilidades[t][e][i].forward = ultimo_mensaje[nombre]
                    h.habilidades[t][e][i].likelihood = likelihood[e][i]
                    ultimo_mensaje[nombre] = h.habilidades[t][e][i].forward_posterior


    def backward_propagation(self):
        h = self
        ultimo_mensaje = defaultdict(lambda: Gaussian(0.0, math.inf))
        for t in reversed(range(len(self.eventos))):
            #PRIORS
            priors_t = []
            for e in range(len(h.eventos)):
                priors_t.append([])
                for i in range(len(h.eventos[t][e])):
                    nombre = h.eventos[t][e][i]
                    priors_t[-1].append(
                        ultimo_mensaje[nombre]*h.habilidades[t][e][i].forward
                    )
            #Evento
            likelihood = Evento(priors_t).likelihood
            
            for e in range(len(h.eventos[t])):
                for i in range(len(h.eventos[t][e])):
                    nombre = h.eventos[t][e][i]
                    h.habilidades[t][e][i].backward = ultimo_mensaje[nombre]
                    h.habilidades[t][e][i].likelihood = likelihood[e][i]
                    ultimo_mensaje[nombre] = h.habilidades[t][e][i].backward_posterior

    def posteriors(self):
        return [[[habilidad.posterior for habilidad in equipo] for equipo in evento] for evento in self.habilidades]


