# -*- coding: utf-8 -*-

import pygame

def simplificar_fraccion(dividendo, divisor):
		for i in range(dividendo,2,-1):
			if dividendo%i == 0 and divisor%i == 0:
					return dividendo/float(i), divisor/float(i)
		return None


ASPECTRO = RESOLUCION[0]/float(RESOLUCION[1])
ASPECTRO_P =  simplificar_fraccion(*RESOLUCION)

DIF_ASP = 1.3333

DIMENSIONS_GL = 100
DIMENSIONS_GL_ESTANDAR = DIMENSIONS_GL*DIF_ASP

ANCHO_PANTALLA_GL_PRO = DIMENSIONS_GL*ASPECTRO
ALTO_PANTALLA_GL_PRO = DIMENSIONS_GL

MARCO_LATERAL = int(ANCHO_VENTANA - ((DIMENSIONS_GL_ESTANDAR*ANCHO_VENTANA)/float(ANCHO_PANTALLA_GL_PRO)))

if MARCO_LATERAL < 0:
	MARCO_VERTICAL = int(abs(MARCO_LATERAL)/float(DIF_ASP))
else:
	MARCO_VERTICAL = 0

MARCO_LATERAL = max(0,MARCO_LATERAL)
MARCO_VERTICAL = max(0,MARCO_VERTICAL)

ANCHO_PANTALLA_GL = DIMENSIONS_GL_ESTANDAR
ALTO_PANTALLA_GL = DIMENSIONS_GL
	

COLOR_LIMPIADO = [1,1,1,1]

#CAMBIARAN DESPOIS:

pos_camara = [0,0]

lista_cadros_colision = []
lista_vertices_cadros_colision = []
vertices_cadricula = []

ANCHO_FASE = 500
ALTO_FASE = 600