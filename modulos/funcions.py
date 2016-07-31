# -*- coding: utf-8 -*-

#from __future__ import division

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
    
def drawText(x, y, text, tamanho,cor_background):                                                                                                    
    font = pygame.font.Font(None, int(tamanho))                                          
    textSurface = font.render(text, True, (0,0,0,255), cor_background)                                   
    textData = pygame.image.tostring(textSurface, "RGBA", True)              
    glRasterPos3d(x-textSurface.get_width()/2,y-textSurface.get_height()/2,0)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),         
                GL_RGBA, GL_UNSIGNED_BYTE, textData)

def debuxar_linha(vertices):
    glLoadIdentity()
    glBegin(GL_LINES)
    for v in vertices:
        glVertex2f(v[0],v[1])
    glEnd()

def debuxar_hex(radio, centro, cor,cor_linha=False):
    glLoadIdentity()
    glTranslatef(centro[0],centro[1],0)
    glColor4f(*cor)
    glBegin(GL_POLYGON)
    for i in range(6):
        ang = i/6.0*2*math.pi
        glVertex2d(math.sin(ang)*radio,math.cos(ang)*radio)
    glEnd()
    #
    if not cor_linha:
        glColor4f(0, 0, 0, 0.3)
    else:
        glColor4f(*cor_linha)
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        ang = i/6.0*2*math.pi
        glVertex2d(math.sin(ang)*radio,math.cos(ang)*radio)
    glEnd()

def columna_fila_a_pixeles(radio, centro0, columna, fila):
    return [centro0[0] + math.sqrt(3) * radio * (columna + (fila % 2) / 2.0),
            centro0[1] + 1.5 * radio * fila]

def xyz_a_columna_fila(x, y, z):
    # com cada x a columna aumenta 1
    assert x + y + z == 0
    columna = x + (z - z % 2) / 2
    fila = -z
    return columna, fila
    
def columna_fila_a_xyz(columna,fila):
    z = -fila
    x = columna - (z - z%2)/2
    y = -x -z
    return x,y,z
    
def pixeles_a_xyz(radio, centro0, px, py):
    px -= centro0[0]
    py -= centro0[1]
    px /= float(radio)
    py /= float(radio)
    py = -py
    # sem redondear
    x = (px * math.sqrt(3) - py) / 3
    z = py * 2.0/3
    y = -x - z
    return redondea_xyz(x, y, z)

def pixeles_a_columna_fila(radio, centro0, px, py):
    # q = x, r = z
    px -= centro0[0]
    py -= centro0[1]
    px /= float(radio)
    py /= float(radio)
    py = -py
    # sem redondear
    x = (px * math.sqrt(3) - py) / 3
    z = py * 2.0/3
    y = -x - z
    x, y, z = redondea_xyz(x, y, z)
    return xyz_a_columna_fila(x, y, z)

def redondea_xyz(x, y, z):
    rx = round(x)
    ry = round(y)
    rz = round(z)
    dx = abs(rx - x)
    dy = abs(ry - y)
    dz = abs(rz - z)
    m = max(dx, dy, dz)
    if m == dx:
        rx = -ry - rz
    elif m == dy:
        ry = -rx - rz
    elif m == dz:
        rz = -rx - ry
    return rx, ry, rz

def debuxar_grella(radio, centro0, columnas, filas, px=None, py=None):
    for fila in xrange(filas):
        for columna in xrange(columnas):
            centro = columna_fila_a_pixeles(radio, centro0, columna, fila)
            if None not in [px, py] and (columna, fila) == pixeles_a_columna_fila(radio, centro0, px, py):
                cor = 0.957, 0.643, 0.376, 1.0
                cor_text = 244, 164, 96, 255
            else:
                cor = 0.118, 0.565, 1.000, 1.0
                cor_text = 30, 144, 255, 255
            debuxar_hex(radio, centro, cor)
            x,y,z = columna_fila_a_xyz(columna,fila)
            glColor4f(*cor)
            drawText(radio/2, radio/3, str(x), radio, cor_text)
            drawText(-radio/2+3, radio/3, str(y), radio, cor_text)
            drawText(2, -radio/3, str(z), radio, cor_text)
            
def debuxar_hex_con_pxpy(radio,centro0,columnas,filas,px,py):
    cor = 0.9, 0.4, 0.4, 0.2
    columna,fila = pixeles_a_columna_fila(radio, centro0, px, py)
    if (0 <= columna < columnas) and (0 <= fila < filas):
        centro = columna_fila_a_pixeles(radio, centro0, columna, fila)
        debuxar_hex(radio, centro, cor,[1.0,0.1,0.1,1])
     
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
    
def crear_lista_grella(id_lista,radio,centro0,columnas,filas):
    glNewList(id_lista, GL_COMPILE)
    glLoadIdentity()
    debuxar_grella(radio, centro0, columnas, filas, px=None, py=None)
    glEndList()
