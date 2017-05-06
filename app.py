import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#Vertices berupa list of tuple
#Kelas untuk menyimpan data gedung versi 2 dimensi
class gedung2D:

    def __init__(self,nama,vertices):
        self.nama = nama
        self.vertices = vertices

    def print2D(self):
        glBegin(GL_POLYGON)
        for vertex in self.vertices:
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
                vertex += (float(word)/10,)
            iterator -= 1
            verticesTemp.append(vertex)
            if (iterator < 1):
                kumpulan.append(verticesTemp)
                first = True

#menampilkan seluruh bentuk berdasarkan kumpulan titik
def printKumpulan(kumpulan):
    for vertices in kumpulan:
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()


def main():
    kumpulanGedung = []
    kumpulanPohon = []
    kumpulanJalan = []
    #migrasi file eksternal ke memori
    loadFile(kumpulanGedung,"resources/gedung.txt")
    loadFile(kumpulanPohon,"resources/pohon.txt")
    loadFile(kumpulanJalan,"resources/jalan.txt")
    test = gedung2D("test",kumpulanGedung[0])
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(-20,-20, -50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.5,0,0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-0.5,0,0)

                if event.key == pygame.K_UP:
                    glTranslatef(0,-1,0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0,1,0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,1.0)

                if event.button == 5:
                    glTranslatef(0,0,-1.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        printKumpulan(kumpulanGedung)
        #printKumpulan(kumpulanPohon)
        #printKumpulan(kumpulanJalan)
        pygame.display.flip()
        pygame.time.wait(10)

main()
