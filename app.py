import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#Vertices berupa list of tuple
#Fungsi mengurutkan titik sehingga berlawanan arah jarum jam
def orderVertices(vertices):
    length = len(vertices)
    for index in range(0,length):
        x = vertices[index]
        for index2 in range((index+1),length):
            if not(compareVertex(x,vertices[index2])):
                temp = x
                x = vertices[index2]
                vertices[index2] = temp
        vertices[index] = x

def compareVertex(v1,v2):
    if (v1[0] > v2[0]):
        return True
    elif (v1[0] == v2[0]):
        if (v1[1] < v2[1]):
            return True
        else:
            return False
    else:
        return False

#Kelas untuk menyimpan data gedung versi 2 dimensi
class gedung2D:

    def __init__(self,nama,vertices):
        self.nama = nama
        selft.vertices = vertices

    def print2D():
        orderVertices(vertices)
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

#Menyimpan kumpulan titik pada memory
def loadFile(kumpulan,namaFile):
    f = open(namaFile,"r")
    first = True
    iterator = 0
    for line in f:
        if first:
            iterator = int(line)
            verticesTemp = []
            first = False
        else :
            vertex = ()
            for word in line.split():
                vertex += (float(word),)
            iterator -= 1
            verticesTemp.append(vertex)
            if (iterator < 1):
                kumpulan.append(verticesTemp)
                first = True

kumpulanGedung = []
kumpulanPohon = []
kumpulanJalan = []

loadFile(kumpulanGedung,"resources/gedung.txt")
loadFile(kumpulanPohon,"resources/pohon.txt")
loadFile(kumpulanJalan,"resources/jalan.txt")





"""
def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(-268,-236, -50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()
"""
