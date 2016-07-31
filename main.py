# -*- coding: utf-8 -*-

###LIBRERIAS NECESARIAS###
#pygame
#pyOpenGL

from __future__ import division

from modulos.funcions import *

from pygame.locals import *

import ctypes
import os
import sys

if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
    ctypes.windll.user32.SetProcessDPIAware()

#VARIABLES

camara_libre = True
mostrar_cadricula = True

_fase_cargada = False

#INICIAR PYGAME

pygame.init()

#VENTANA

ventana = pygame.display.set_mode([ANCHO_VENTANA,ALTO_VENTANA],OPENGL|DOUBLEBUF|HWSURFACE)

pygame.display.set_caption("Xogo_Estratexia")

#------------------------------------------------------------------------
#FUNCION MAIN
#------------------------------------------------------------------------

_ON = True

def main():

    global _ON
    global _fase_cargada
    global camara_libre
    global mostrar_cadricula
    global ANCHO_PANTALLA_GL
    global ALTO_PANTALLA_GL

    # esteban cambiou esto
    ANCHO_PANTALLA_GL = 390
    ALTO_PANTALLA_GL = ANCHO_PANTALLA_GL / DIF_ASP
    global pos_camara
    pos_camara[:] = [4.5, 0]
    #INICIAR OPENGL
    pos_mouse_gl = False
	
    radio = 20

    init_gl()

    #BUCLE XOGO
    #-----------------

    while _ON:

        reloj = pygame.time.Clock()

        #### CARGA DE FASE ####

        if not _fase_cargada:

            #LISTAS DE OPENGL
            
            ID_LISTA_GRELLA = glGenLists(1)
            crear_lista_grella(ID_LISTA_GRELLA,radio,[1.7 * radio, 2 * radio],10,8)
            
            _fase_cargada = True

        #LIMPIAR VENTANA

        limpiar_ventana_gl(ANCHO_PANTALLA_GL,ALTO_PANTALLA_GL)

        #glBindTexture(GL_TEXTURE_2D,0)

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
        
        glColor4f(0, 0.5, 1, 0.8)
        #debuxar_hex(100,[ANCHO_FASE/2,ALTO_FASE/2])
        #debuxar_fila(20,[ANCHO_FASE/2,ALTO_FASE/2], 5)
        
        #if pos_mouse_gl:
        #    debuxar_grella(radio, [1.7 * radio, 2 * radio], 10, 8, *pos_mouse_gl)
        #else:
        #    debuxar_grella(radio, [1.7 * radio, 2 * radio], 10, 8)
        
        glCallList(ID_LISTA_GRELLA)
        
        if pos_mouse_gl:
             debuxar_hex_con_pxpy(radio,[1.7 * radio, 2 * radio],10,8,pos_mouse_gl[0],pos_mouse_gl[1])
        
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

        for evento in pygame.event.get():

            #MOUSE
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4:
                    if not ANCHO_PANTALLA_GL == ANCHO_FASE/2:
                        ANCHO_PANTALLA_GL -= 4
                        ANCHO_PANTALLA_GL = max(ANCHO_FASE/2,ANCHO_PANTALLA_GL)
                        pos_camara[0] += 2
                        pos_camara[1] += 2
                elif evento.button == 5:
                    if not ANCHO_PANTALLA_GL == ANCHO_FASE:
                        ANCHO_PANTALLA_GL += 4
                        ANCHO_PANTALLA_GL = min(ANCHO_FASE,ANCHO_PANTALLA_GL)
                        pos_camara[0] -= 2
                        pos_camara[1] -= 2
                if evento.button in [4,5]:
                    ALTO_PANTALLA_GL = ANCHO_PANTALLA_GL / DIF_ASP

            #TECLADO
            if evento.type == pygame.KEYDOWN:

                #CAMARA_LIBRE
                if evento.key == K_c:
                    if camara_libre:
                        camara_libre=False
                    else:
                        camara_libre=True

                #MOSTRAR_CADRICULA
                if evento.key == K_v:
                    if mostrar_cadricula:
                        mostrar_cadricula = False
                    else:
                        mostrar_cadricula = True

                #ESC - CERRAR  XOGO
                if evento.key == K_ESCAPE:
                    _ON = False

            #QUIT
            if evento.type == pygame.QUIT:
                _ON = False

        if not _ON:
            pygame.display.quit()
            break

        #CAMARA
        
        if tecla_pulsada[K_RIGHT]:
            pos_camara[0] += 1
        if tecla_pulsada[K_LEFT]:
            pos_camara[0] -= 1
        if tecla_pulsada[K_UP]:
            pos_camara[1] += 1
        if tecla_pulsada[K_DOWN]:
            pos_camara[1] -= 1
        pos_camara[0] = max(0,pos_camara[0])
        pos_camara[0] = min(ANCHO_FASE-ANCHO_PANTALLA_GL,pos_camara[0])
        
        pos_camara[1] = max(0,pos_camara[1])
        pos_camara[1] = min(ALTO_FASE-ALTO_PANTALLA_GL,pos_camara[1])
            
        #pos_camara[0] = pos_camara[0]-(ANCHO_PANTALLA_GL/2)
        #pos_camara[1] = pos_camara[1]-(ALTO_PANTALLA_GL/2)

        #pos_camara[0] = max(pos_camara[0], 0)
        #pos_camara[0] = min(pos_camara[0], ANCHO_FASE-ANCHO_PANTALLA_GL)

        #pos_camara[1] = max(pos_camara[1], 0)
        #pos_camara[1] = min(pos_camara[1], ALTO_FASE-ALTO_PANTALLA_GL)

        pygame.display.flip()

        reloj.tick(FPS)

if __name__ == '__main__':
    main()
