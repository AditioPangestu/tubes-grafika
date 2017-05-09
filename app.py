from __future__ import print_function
import pygame
from pygame.locals import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *

kumpulanGedung3D = []
textures = []

#Kelas untuk menyimpan gambar dari file ke memori
class Gambar:
    def __init__(self, image = None, x = 0, y = 0):
        self.image = image
        self.x = x
        self.y = y

#Kelas untuk menyimpan data gedung versi 3 dimensi
class gedung3D:
    def __init__(self, vertices = [], edges = [], surfaces = [], selatan = None, utara = None, barat = None, timur = None, atas = None):
        self.vertices = vertices
        self.edges = edges
        self.surfaces = surfaces
        self.selatan = selatan
        self.utara = utara
        self.barat = barat
        self.timur = timur
        self.atas = atas

    def print3D(self):
        counter = 1
        for surface in self.surfaces:
            # siapin gambarnya
            if counter == 2:
                drawImage(self.atas)
            elif counter == 3:
                drawImage(self.utara)
            elif counter == 4:
                drawImage(self.barat)
            elif counter == 5:
                drawImage(self.selatan)
            elif counter == 6:
                drawImage(self.timur)
            # tempel ke koordinat
            glBegin(GL_QUADS)
            TexCoord = [(0.0,0.0),(1.0,0.0),(1.0,1.0),(0.0,1.0)]
            index = 0
            for vertex in surface:
                glTexCoord2fv(TexCoord[index])
                index += 1
                glVertex3fv(self.vertices[vertex])
            counter += 1
            glEnd()
        # gambar rusuk kubus (?)
"""
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()
"""
def loadImage(filename = ''):
    image = pygame.image.load('resources/' + filename)
    ix = image.get_width()
    iy = image.get_height()
    return Gambar(pygame.image.tostring(image, "RGBA", 1), ix, iy)

def drawImage(image = None):
    texture = 0
    glBindTexture(GL_TEXTURE_2D, texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, image.x, image.y, 0, GL_RGBA, GL_UNSIGNED_BYTE, image.image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

#Menyimpan kumpulan titik pada memory
def loadFile(namafile = ''):
    global kumpulanGedung3D

    f = open(namafile, "r")
    mode = 1 # lagi load vertex atau edge atau surface atau image
    newMode = True
    rowRemaining = 1
    print('Loading', end = '')
    for line in f:
        print('.', end = '')
        line = line.split('\n')[0]
        if newMode:
            rowRemaining = int(line)
            if mode == 1:
                vertices = []
                edges = []
                surfaces = []
            selatan = None
            utara = None
            barat = None
            timur = None
            atas = None
            newMode = False
        else :
            if mode == 1:
                temp = []
                for word in line.split():
                    temp.append(float(word) / 20)
                vertices.append(tuple(temp))
            elif mode == 2:
                temp = []
                for word in line.split():
                    temp.append(int(word))
                edges.append(temp)
            elif mode == 3:
                temp = []
                for word in line.split():
                    temp.append(int(word))
                surfaces.append(temp)
            elif mode == 4:
                if rowRemaining == 5:
                    selatan = loadImage(str(line))
                elif rowRemaining == 4:
                    utara = loadImage(str(line))
                elif rowRemaining == 3:
                    barat = loadImage(str(line))
                elif rowRemaining == 2:
                    timur = loadImage(str(line))
                elif rowRemaining == 1:
                    atas = loadImage(str(line))
            rowRemaining -= 1
            if (rowRemaining < 1):
                mode += 1
                newMode = True
            if mode > 4: # new building
                mode = 1
                kumpulanGedung3D.append(gedung3D(vertices, edges, surfaces, selatan, utara, barat, timur, atas))

def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    # initialize texture mapping
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

def main():
    # load file
    loadFile("resources/gedung3d.txt")
    # init pygame
    display = (800, 600)
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    InitGL(display[0],display[1])
    glTranslatef(-20, -25, -75)
    # infinite loop until quit
    while True:
        # keyboard / mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.5, 0, 0)
                elif event.key == pygame.K_RIGHT:
                    glTranslatef(-0.5, 0, 0)
                elif event.key == pygame.K_UP:
                    glTranslatef(0, -1, 0)
                elif event.key == pygame.K_DOWN:
                    glTranslatef(0, 1, 0)
                elif event.key == pygame.K_a:
                    glRotatef(5, 0, -1, 0)
                elif event.key == pygame.K_d:
                    glRotatef(5, 0, 1, 0)
                elif event.key == pygame.K_w:
                    glRotatef(5, -1, 0, 0)
                elif event.key == pygame.K_s:
                    glRotatef(5, 1, 0, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)
                elif event.button == 5:
                    glTranslatef(0, 0, -1.0)
        # redraw
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for gedung in kumpulanGedung3D:
            gedung.print3D()
        pygame.display.flip()
        pygame.time.wait(100)

# main program
main()
