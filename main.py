# -*- coding: utf-8 -*-

from __future__ import division

import math
import pyglet
from pyglet.gl import *
from pyglet.window import key
from modulos.funcions import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES
FPS = 30
pos_camara = [0,0]
_fase_cargada = False
manter_letra = 10
	
#VENTANA
resolucion = [640,480]
aspectro_pantalla = resolucion[0]/float(resolucion[1])
DIF_ASP = 1.333

config = Config(double_buffer=True)
window = pyglet.window.Window(width=resolucion[0], 	height=resolucion[1],
								caption="Main", config=config, resizable=True)
								
window.set_minimum_size(320, 240)
							
#TAMANHO GL
ALTO_PANTALLA_GL = 100
ANCHO_PANTALLA_GL = int(ALTO_PANTALLA_GL * DIF_ASP)

#MARCO
MARCO_LATERAL,MARCO_VERTICAL = calcular_marco(resolucion,ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL,DIF_ASP)

#VARIABLES 2
VELOCIDADE_DESPLAZAMENTO = ALTO_PANTALLA_GL / 50
ZOOM = ALTO_PANTALLA_GL / 20
presionadas = []

#FASE
ALTO_FASE = 100
ANCHO_FASE = ALTO_FASE * DIF_ASP

#CALCULO DE HEXAGONOS
columnas = 5
filas = 5

radio_columnas = (ANCHO_FASE/float(columnas+1))*0.50
radio_filas = (ALTO_FASE/float(filas+1))*0.65

radio = min(radio_columnas,radio_filas)

ancho_hex_total = columnas*(radio*math.sqrt(3))+abs(columnas%2-1)*radio*0.75
alto_hex_total = filas*radio*1.5+radio/2

dif_alto_hex = (ALTO_FASE-alto_hex_total)
dif_ancho_hex = (ANCHO_FASE-ancho_hex_total)

centro0 = [dif_ancho_hex/2+radio*math.sqrt(3)/2,dif_alto_hex/2+radio]

#VARIABLES 3	
posicion_mouse_rel = False
posicion_mouse_abs = False

ID_LISTA_GRELLA = 1
tamanho_da_letra = 10
crear_lista_grella(ID_LISTA_GRELLA,radio,centro0,columnas,filas,tamanho_da_letra,True)

init_gl(0,0,ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL)

@window.event
def on_resize(width, height):
	global resolucion
	resolucion = [width,height]

@window.event
def on_draw():
	#window.clear()
	limpiar_ventana_gl(ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL,[0,0])
	glColor4f(0,0,0,1)
	debuxar_rect_gl([[0,0],[ANCHO_FASE,0],[ANCHO_FASE,ALTO_FASE],[0,ALTO_FASE]])
	glCallList(ID_LISTA_GRELLA)
	glColor4f(1,1,1,1)
	if posicion_mouse_rel:
		debuxar_hex_con_pxpy(radio,centro0,columnas,filas,
					posicion_mouse_rel[0],posicion_mouse_rel[1])
		
@window.event
def on_mouse_motion(x, y, dx, dy):
	global posicion_mouse_rel
	global posicion_mouse_abs
	posicion_mouse_abs = [x,y]
	posicion_mouse_rel = [x*(ANCHO_PANTALLA_GL/float(resolucion[0])),
							y*(ALTO_PANTALLA_GL/float(resolucion[1]))]
	window.invalid = False

@window.event
def on_mouse_leave(x, y):
	global posicion_mouse_rel
	global posicion_mouse_abs
	posicion_mouse_rel = False
	posicion_mouse_abs = False
	window.invalid = False

@window.event
def on_mouse_press(x, y, button, modifiers):
	window.invalid = False
	pass

@window.event
def on_mouse_release(x, y, button, modifiers):
	window.invalid = False
	pass

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	window.invalid = False
	pass

def update(dt):
	if posicion_mouse_rel:
		m_x = posicion_mouse_rel[0]
		m_y = posicion_mouse_rel[1]

if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1.0/60)
	pyglet.app.run()