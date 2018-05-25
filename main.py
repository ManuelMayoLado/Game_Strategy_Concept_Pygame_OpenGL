# -*- coding: utf-8 -*-

###LIBRERIAS NECESARIAS###
#pygame
#pyOpenGL

from __future__ import division

from modulos.funcions import *

import pygame

from pygame.locals import *

import ctypes
import os
import sys
import math

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

FPS = 30
pos_camara = [0,0]
_fase_cargada = False

manter_letra = 10

#INICIAR PYGAME

pygame.init()

#VENTANA

RESOLUCION_PANTALLA = [pygame.display.Info().current_w,pygame.display.Info().current_h]
ASPECTRO_REAL = RESOLUCION_PANTALLA[0]/float(RESOLUCION_PANTALLA[1])
DIF_ASP = ASPECTRO_REAL
#DIF_ASP = 1.3333

RESOLUCION = RESOLUCION_PANTALLA[:]
RESOLUCION[0] = int(RESOLUCION[0]/2)
RESOLUCION[1] = int(RESOLUCION[1]/2)
ANCHO_VENTANA, ALTO_VENTANA = RESOLUCION

#TAMANHO GL
ALTO_PANTALLA_GL = 100
ANCHO_PANTALLA_GL = ALTO_PANTALLA_GL * DIF_ASP

MARCO_LATERAL,MARCO_VERTICAL = calcular_marco(RESOLUCION,ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL,DIF_ASP)

#variables 2

VELOCIDADE_DESPLAZAMENTO = ALTO_PANTALLA_GL / 50
ZOOM = ALTO_PANTALLA_GL / 20

#FASE

ALTO_FASE = 100
ANCHO_FASE = ALTO_FASE * DIF_ASP

ventana = pygame.display.set_mode([ANCHO_VENTANA,ALTO_VENTANA],OPENGL|DOUBLEBUF|HWSURFACE|RESIZABLE)
pygame.display.set_caption("Xogo_Estratexia")

#------------------------------------------------------------------------
#FUNCION MAIN
#------------------------------------------------------------------------

_ON = True

presionadas = []

def main():

    global _ON
    global _fase_cargada
    global ANCHO_PANTALLA_GL
    global ALTO_PANTALLA_GL
    global ANCHO_VENTANA
    global ALTO_VENTANA
    global MARCO_LATERAL
    global MARCO_VERTICAL
    global pos_camara
    global manter_letra
    global presionadas
    
    #Variables 3
    
    hex_mouse_deb = False
    pos_mouse_gl = False
    numeros_hex = False
    
    #NUMERO DE HEXAGONOS
    ###############################################
    n_hex_columna = 10
    n_hex_fila = 15
    ###############################################
    
    n_hex_columna = max(1,n_hex_columna)
    n_hex_fila = max(1,n_hex_fila)
    
    radio = ((ALTO_FASE/float(n_hex_columna+1))*0.75)
        
    if not n_hex_fila:
        n_hex_fila = (ANCHO_FASE/(radio*math.sqrt(3)))
        n_hex_fila = int(round(n_hex_fila-0.5))
        calcular_hex_fila = True
    else:
        calcular_hex_fila = False
        
    ancho_hex_total = n_hex_fila*(radio*math.sqrt(3))+abs(n_hex_columna%2-1)*radio*0.75
    alto_hex_total = n_hex_columna*radio*1.5+radio/2
        
    while alto_hex_total >= ALTO_FASE:
        radio -= 0.1
        if calcular_hex_fila:
            n_hex_fila = (ANCHO_FASE/(radio*math.sqrt(3)))
            n_hex_fila = int(round(n_hex_fila-0.5))
        alto_hex_total = n_hex_columna*radio*1.5+radio/2
        ancho_hex_total = n_hex_fila*(radio*math.sqrt(3))+abs(n_hex_columna%2-1)*radio*0.75
            
    while ancho_hex_total >= ANCHO_FASE:
        if calcular_hex_fila:
            n_hex_fila -= 1
        else:
            radio -= 0.1
        alto_hex_total = n_hex_columna*radio*1.5+radio/2
        ancho_hex_total = n_hex_fila*(radio*math.sqrt(3))+abs(n_hex_columna%2-1)*radio*0.75
            
    ancho_hex_total = n_hex_fila*(radio*math.sqrt(3))+abs(n_hex_columna%2-1)*radio*0.75
    alto_hex_total = n_hex_columna*radio*1.5+radio/2
        
    dif_alto_hex = (ALTO_FASE-alto_hex_total)
    dif_ancho_hex = (ANCHO_FASE-ancho_hex_total)
    
    print("Number of Hexs:", n_hex_fila*n_hex_columna)
    
    
    centro0 = [dif_ancho_hex/2+radio*math.sqrt(3)/2,dif_alto_hex/2+radio]
    
    #print "ANCHO FASE:",ANCHO_FASE
    #print "ALTO FASE:",ALTO_FASE
    #print "RADIO:",radio
    #print "N HEX COLUMN:",n_hex_columna
    #print "N HEX ROW:",n_hex_fila
    #print "HEX NUMBER:",n_hex_columna*n_hex_fila

    init_gl(MARCO_LATERAL,MARCO_VERTICAL,ANCHO_VENTANA,ALTO_VENTANA)

    #BUCLE XOGO
    #-----------------

    while _ON:

        reloj = pygame.time.Clock()

        #### CARGA DE FASE ####

        if not _fase_cargada:

            #LISTAS DE OPENGL
            
            ID_LISTA_GRELLA = glGenLists(1)
            tamanho_da_letra = radio * max(1,((ANCHO_FASE/ANCHO_PANTALLA_GL)*3)) + max(0,ANCHO_VENTANA/600)
            crear_lista_grella(ID_LISTA_GRELLA,radio,centro0,n_hex_fila,n_hex_columna,tamanho_da_letra,numeros_hex)
            
            _fase_cargada = True

        #LIMPIAR VENTANA

        limpiar_ventana_gl(ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL,pos_camara)

        ############################################
        #DEBUXADO
        ############################################

        #DEBUXAR FONDO
        glColor4f(1, 1, 1, 1)
        glLoadIdentity()
        glBegin(GL_QUADS)
        glVertex2f(pos_camara[0],pos_camara[1])
        glVertex2f(ANCHO_PANTALLA_GL+pos_camara[0],pos_camara[1])
        glVertex2f(ANCHO_PANTALLA_GL+pos_camara[0],ALTO_PANTALLA_GL+pos_camara[1])
        glVertex2f(pos_camara[0],ALTO_PANTALLA_GL+pos_camara[1])
        glEnd()
        
        #FASE
        v_f = [[0,0],[ANCHO_FASE,0],[ANCHO_FASE,ALTO_FASE],[0,ALTO_FASE]]
        glColor4f(0.5, 0.5, 1, 0.5)
        debuxar_rect_gl(v_f,pos=False)
        
        glCallList(ID_LISTA_GRELLA)
        if pos_mouse_gl:
             hex_mouse_deb = debuxar_hex_con_pxpy(radio,centro0,n_hex_fila,n_hex_columna,pos_mouse_gl[0],pos_mouse_gl[1])
        
        
        ############################################
        #EVENTOS
        ############################################

        ###### TECLAS PULSADAS ######

        tecla_pulsada = pygame.key.get_pressed()

        ####### MOUSE ########

        pos_mouse = pygame.mouse.get_pos()

        if (MARCO_LATERAL/2 <= pos_mouse[0] <= ANCHO_VENTANA-MARCO_LATERAL/2
            and MARCO_VERTICAL / 2 <= pos_mouse[1] <= ALTO_VENTANA - MARCO_VERTICAL / 2):
            pos_mouse_gl = [
                (pos_mouse[0]-MARCO_LATERAL/2)*ANCHO_PANTALLA_GL/(ANCHO_VENTANA-MARCO_LATERAL)+pos_camara[0],
                ALTO_PANTALLA_GL-(
                    (pos_mouse[1]-MARCO_VERTICAL/2)*ALTO_PANTALLA_GL/(ALTO_VENTANA-MARCO_VERTICAL))+pos_camara[1]]
        else:
            pos_mouse_gl = False

        #EVENTOS

        for x, y, z in presionadas:
            debuxar_hex_con_pxpy(radio,centro0,n_hex_fila,n_hex_columna, *columna_fila_a_pixeles(radio, centro0, *xyz_a_columna_fila(x, y, z)))

        for evento in pygame.event.get():

            #MOUSE
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if pos_mouse_gl and hex_mouse_deb:
                        print(hex_mouse_deb)
                        presionadas[:] = vicinhas(*list(hex_mouse_deb[1][x] for x in 'XYZ') + [3])
                if evento.button == 4:
                    if not ANCHO_PANTALLA_GL == ANCHO_FASE/2:
                        ANCHO_PANTALLA_GL -= ZOOM
                        ANCHO_PANTALLA_GL = max(ANCHO_FASE/2,ANCHO_PANTALLA_GL)
                        pos_camara[0] += ZOOM/2
                        pos_camara[1] += ZOOM/2
                elif evento.button == 5:
                    if not ANCHO_PANTALLA_GL == ANCHO_FASE:
                        ANCHO_PANTALLA_GL += ZOOM
                        ANCHO_PANTALLA_GL = min(ANCHO_FASE,ANCHO_PANTALLA_GL)
                        pos_camara[0] -= ZOOM/2
                        pos_camara[1] -= ZOOM/2
                if evento.button in [4,5]:
                    ALTO_PANTALLA_GL = ANCHO_PANTALLA_GL / DIF_ASP
                    if not manter_letra:
                        if radio * max(1,((ANCHO_FASE/ANCHO_PANTALLA_GL)/1.5)) != tamanho_da_letra:
                            _fase_cargada = False
                            manter_letra = 10
                        else:
                            manter_letra = 10
                    else:
                        manter_letra -= 1

            #TECLADO
            if evento.type == pygame.KEYDOWN:
            
            #N -> NUMEROS HEX
                if evento.key == K_n:
                    if not numeros_hex:
                        numeros_hex = True
                    else:
                        numeros_hex = False
                    _fase_cargada = False

                #ESC - CERRAR  XOGO
                if evento.key == K_ESCAPE:
                    _ON = False
            
            #REDIMENSIONAR       
            if evento.type == VIDEORESIZE:
                ANCHO_VENTANA = max(evento.dict['size'][0],int(RESOLUCION_PANTALLA[0]/3))
                ALTO_VENTANA = max(evento.dict['size'][1],int(RESOLUCION_PANTALLA[1]/3))
                ANCHO_PANTALLA_GL = max(ANCHO_FASE/2,ANCHO_PANTALLA_GL)
                ANCHO_PANTALLA_GL = min(ANCHO_FASE,ANCHO_PANTALLA_GL)
                ALTO_PANTALLA_GL = ANCHO_PANTALLA_GL / DIF_ASP
                ventana = pygame.display.set_mode([ANCHO_VENTANA,ALTO_VENTANA],OPENGL|DOUBLEBUF|RESIZABLE)
                RESOLUCION[0] = ANCHO_VENTANA
                RESOLUCION[1] = ALTO_VENTANA
                MARCO_LATERAL,MARCO_VERTICAL = calcular_marco(RESOLUCION,ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL,DIF_ASP)
                init_gl(MARCO_LATERAL,MARCO_VERTICAL,ANCHO_VENTANA,ALTO_VENTANA)
                _fase_cargada = False

            #QUIT
            if evento.type == pygame.QUIT:
                _ON = False

        if not _ON:
            pygame.display.quit()
            break

        #CAMARA
        
        if tecla_pulsada[K_RIGHT]:
            pos_camara[0] += VELOCIDADE_DESPLAZAMENTO
        if tecla_pulsada[K_LEFT]:
            pos_camara[0] -= VELOCIDADE_DESPLAZAMENTO
        if tecla_pulsada[K_UP]:
            pos_camara[1] += VELOCIDADE_DESPLAZAMENTO
        if tecla_pulsada[K_DOWN]:
            pos_camara[1] -= VELOCIDADE_DESPLAZAMENTO
        pos_camara[0] = max(0,pos_camara[0])
        pos_camara[0] = min(ANCHO_FASE-ANCHO_PANTALLA_GL,pos_camara[0])
        
        pos_camara[1] = max(0,pos_camara[1])
        pos_camara[1] = min(ALTO_FASE-ALTO_PANTALLA_GL,pos_camara[1])

        pygame.display.flip()

        reloj.tick(FPS)

if __name__ == '__main__':
    main()
