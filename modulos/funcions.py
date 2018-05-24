# -*- coding: utf-8 -*-

from __future__ import division

from pyglet.gl import *
from pyglet import font

import math

arial = font.load('Arial', 14, bold=True, italic=False)

def pos(n, num_cadros_ancho_fase):
    return [n % num_cadros_ancho_fase, n / num_cadros_ancho_fase]

def num(p, num_cadros_ancho_fase):
    return p[0]+p[1]*num_cadros_ancho_fase
    
def simplificar_fraccion(dividendo, divisor):
        for i in range(dividendo,2,-1):
            if dividendo%i == 0 and divisor%i == 0:
                return dividendo/float(i), divisor/float(i)
        return None
    
def calcular_marco(resolucion,ancho_gl,alto_gl,dif_asp):
    ancho_esperable = resolucion[1] * dif_asp
    marco_lateral = int(resolucion[0] - ancho_esperable)
    if marco_lateral < 0:
        alto_esperable = resolucion[0] / dif_asp
        marco_vertical = int(resolucion[1] - alto_esperable)
        marco_lateral = 0
    else:
        marco_vertical = 0
    return marco_lateral, marco_vertical

#### OPENGL ####

def init_gl(marco_lateral,marco_vertical,ancho,alto):
    glClearColor(0,0,0,0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

def limpiar_ventana_gl(ancho_gl,alto_gl,pos_camara):
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

def debuxar_hex(radio, centro, cor, cor_linha=False):
    glLoadIdentity()
    glTranslatef(centro[0],centro[1],0)
    glColor4f(*cor)
    glBegin(GL_POLYGON)
    for i in range(6):
        ang = i/6.0*2*math.pi
        glVertex2d(math.sin(ang)*radio,math.cos(ang)*radio)
    glEnd()
    if not cor_linha:
        glColor4f(0, 0, 0, 0.5)
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

def vicinhas(x, y, z, n=1):
    return ((x + dx, y + dy, z - dx - dy)
            for dx in xrange(-n, n+1)
            for dy in xrange(max(-n, -dx-n), min(n, -dx + n) + 1)
            if (dx, dy) != (0, 0))

def debuxar_grella(radio, centro0, columnas, filas, tamanho_letra, numeros=False, px=None, py=None):
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
            if numeros:
                label = pyglet.text.Label(str(int(x)), font_name='Times New Roman',
                                font_size=radio/3,
                                x=0, y=0, width=radio/2, height=radio/2,
                                anchor_x='center', anchor_y='center', dpi=240)
                label.draw()
                #drawText(radio/5.5, 0, str(x), tamanho_letra, cor_text)
                #drawText(-radio/1.5, 0, str(y), tamanho_letra, cor_text)
                #drawText(-radio/4, -radio/1.5, str(z), tamanho_letra, cor_text)
            
def debuxar_hex_con_pxpy(radio,centro0,columnas,filas,px,py):
    cor = 0.9, 0.4, 0.4, 0.2
    columna,fila = pixeles_a_columna_fila(radio, centro0, px, py)
    if (0 <= columna < columnas) and (0 <= fila < filas):
        centro = columna_fila_a_pixeles(radio, centro0, columna, fila)
        debuxar_hex(radio, centro, cor,[1.0,0.1,0.1,1])
        x,y,z = columna_fila_a_xyz(columna,fila)
        return {"Columna":columna,"Fila":fila}, {"X":x,"Y":y,"Z":z}
    else:
        return False
     
def debuxar_cadrado_gl(pos,tamanho=50,cor=[1,1,1,1]):
	glLoadIdentity()
	glTranslatef(pos[0], pos[1], 0)
	glColor4f(*cor)
	glBegin(GL_QUADS)
	glVertex2f(-tamanho/2,-tamanho/2)
	glVertex2f(tamanho/2,-tamanho/2)
	glVertex2f(tamanho/2,tamanho/2)
	glVertex2f(-tamanho/2,tamanho/2)
	glEnd()

def debuxar_rect_gl(vertices,pos=False):
    glLoadIdentity()
    if pos:
        glTranslatef(pos[0], pos[1], 0)
    glBegin(GL_QUADS)
    for v in range(0,len(vertices),4):
        glVertex2f(vertices[v][0],vertices[v][1])
        glVertex2f(vertices[v+1][0],vertices[v+1][1])
        glVertex2f(vertices[v+2][0],vertices[v+2][1])
        glVertex2f(vertices[v+3][0],vertices[v+3][1])
    glEnd()
	
#LISTAS
    
def crear_lista_grella(id_lista,radio,centro0,columnas,filas,tamanho_letra,numeros):
    glNewList(id_lista, GL_COMPILE)
    glLoadIdentity()
    debuxar_grella(radio, centro0, columnas, filas, tamanho_letra,numeros,px=None, py=None)
    glEndList()
