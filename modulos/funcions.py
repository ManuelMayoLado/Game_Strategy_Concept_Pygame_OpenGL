# -*- coding: utf-8 -*-

#### FUNCIONS ####
##################

from OpenGL.GL import *
from OpenGL.GLU import *
import math

from constantes import *

def pos(n, num_cadros_ancho_fase):
    return [n % num_cadros_ancho_fase, n / num_cadros_ancho_fase]

def num(p, num_cadros_ancho_fase):
    return p[0]+p[1]*num_cadros_ancho_fase

#### OPENGL ####

def init_gl():
    glViewport(MARCO_LATERAL/2,MARCO_VERTICAL/2,ANCHO_VENTANA-MARCO_LATERAL,ALTO_VENTANA-MARCO_VERTICAL)
    glClearColor(0,0,0,0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#    glEnable(GL_LINE_SMOOTH)
#    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

def limpiar_ventana_gl(ancho_gl,alto_gl):
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,ancho_gl,0,alto_gl)
    glTranslatef(0-pos_camara[0],0-pos_camara[1],0)
    glMatrixMode(GL_MODELVIEW)

def debuxar_linha(vertices):
    glLoadIdentity()
    glBegin(GL_LINES)
    for v in vertices:
        glVertex2f(v[0],v[1])
    glEnd()
    
def debuxar_hex(radio,pos):
    glLoadIdentity()
    glTranslatef(pos[0],pos[1],0)
    glColor4f(0, 0.5, 1.0, 0.8)
    glBegin(GL_POLYGON)
    for i in range(6):
        ang = i/6.0*2*math.pi
        glVertex2d(math.sin(ang)*radio,math.cos(ang)*radio)
    glEnd()
    #
    glColor4f(0, 0, 0, 0.3)
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        ang = i/6.0*2*math.pi
        glVertex2d(math.sin(ang)*radio,math.cos(ang)*radio)
    glEnd()

def debuxar_fila(radio, pos, n):
    for i in xrange(n):
        posx = pos[0] + math.sqrt(3) * radio * i
        debuxar_hex(radio, [posx, pos[1]])

def debuxar_grella(radio, pos, columnas, filas):
    for fila in xrange(filas):
        posx = pos[0] + (fila % 2) * radio * math.sqrt(3) / 2.0
        posy = pos[1] + 1.5 * radio * fila
        debuxar_fila(radio, [posx, posy], columnas)

def debuxar_rect_gl(vertices,pos=False):
    glLoadIdentity()
    if pos:
        glTranslatef(pos[0], pos[1], 0)
    glBegin(GL_QUADS)
    for v in range(0,len(vertices),4):
        glTexCoord2f(0,0)
        glVertex2f(vertices[v][0],vertices[v][1])
        glTexCoord2f(1,0)
        glVertex2f(vertices[v+1][0],vertices[v+1][1])
        glTexCoord2f(1,1)
        glVertex2f(vertices[v+2][0],vertices[v+2][1])
        glTexCoord2f(0,1)
        glVertex2f(vertices[v+3][0],vertices[v+3][1])
    glEnd()

def cargar_imagen_textura(imagen):
    texturaSurface = pygame.image.load(imagen).convert_alpha()
    texturaData = pygame.image.tostring(texturaSurface, "RGBA", True)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texturaSurface.get_width(), texturaSurface.get_height(), 0,
                           GL_RGBA, GL_UNSIGNED_BYTE, texturaData)

def crear_lista(id_lista,vertices,forma):
    glNewList(id_lista, GL_COMPILE) ### INICIO LISTA
    glLoadIdentity()
    if forma=="liña":
        debuxar_linha(vertices)
    elif forma=="rectangulo":
        debuxar_rect_gl(vertices)
    glEndList() ############################### FIN LISTA
