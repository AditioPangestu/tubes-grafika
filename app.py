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

class gedung3D:
    def __init__(self, vertices, edges, surfaces, selatan, utara, barat, timur, atas):
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
            if counter == 2:
                loadImage('resources/' + self.atas)
            elif counter == 3:
                loadImage('resources/' + self.utara)
            elif counter == 4:
                loadImage('resources/' + self.barat)
            elif counter == 5:
                loadImage('resources/' + self.selatan)
            elif counter == 6:
                loadImage('resources/' + self.timur)
            glBegin(GL_QUADS)
            x = 0
            for vertex in surface:
                x += 1
                # glColor3fv(colors[x])
                glVertex3fv(self.vertices[vertex])
            counter += 1
            glEnd()

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

def loadImage(filename):
      image = pygame.image.load(str(filename))
      ix = image.get_width()
      iy = image.get_height()

      image = pygame.image.tostring(image, "RGBA", 1)

      glBindTexture(GL_TEXTURE_2D, ID)
      glPixelStorei(GL_UNPACK_ALIGNMENT,1)
      glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
      glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

      return ID

#Menyimpan kumpulan titik pada memory
def loadFile(kumpulan, namaFile):
    f = open(namaFile, "r")
    first = True
    iterator = 0
    counter = 1
    x = 1
    for line in f:
        if first:
            iterator = int(line)
            # verticesTemp = []
            # edgesTemp = []
            # surfacesTemp = []
            if counter == 1:
                verticesTemp = ()
                edgesTemp = ()
                surfacesTemp = ()
            first = False
        else :
            vertex = ()
            edge = ()
            surface = ()
            selatan = ""
            utara = ""
            barat = ""
            timur = ""
            atas = ""
            if counter == 1:
                for word in line.split():
                    vertex += (float(word)/10,)
            elif counter == 2:
                for word in line.split():
                    edge += (int(word),)
            elif counter == 3:
                for word in line.split():
                    surface += (int(word),)
            elif counter == 4:
                if x == 1:
                    selatan = str(line)
                elif x == 2:
                    utara = str(line)
                elif x == 3:
                    barat = str(line)
                elif x == 4:
                    timur = str(line)
                elif x == 5:
                    atas = str(line)
            iterator -= 1
            x += 1
            if counter == 1:
                # verticesTemp.append(vertex)
                verticesTemp += (vertex, )
            elif counter == 2:
                # edgesTemp.append(edge)
                edgesTemp += (edge, )
            elif counter == 3:
                # surfacesTemp.append(surface)
                surfacesTemp += (surface, )
            if (iterator < 1):
                counter += 1
                if counter > 4:
                    counter = 1
                    x = 1
                    tempObject = gedung3D(verticesTemp, edgesTemp, surfacesTemp, selatan, utara, barat, timur, atas)
                    kumpulan.append(tempObject)
                first = True

#menampilkan seluruh bentuk berdasarkan kumpulan titik
def printKumpulan(kumpulan):
    for vertices in kumpulan:
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()


def main():
    # kumpulanGedung = []
    kumpulanGedung3D = []
    # kumpulanPohon = []
    # kumpulanJalan = []
    #migrasi file eksternal ke memori
    # loadFile(kumpulanGedung,"resources/gedung.txt")
    loadFile(kumpulanGedung3D,"resources/gedung3d.txt")
    # loadFile(kumpulanPohon,"resources/pohon.txt")
    # loadFile(kumpulanJalan,"resources/jalan.txt")
    # test = gedung2D("test",kumpulanGedung[0])
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 75.0)

    glTranslatef(-20, -25, -75)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-0.5, 0, 0)

                if event.key == pygame.K_UP:
                    glTranslatef(0, -1, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 1, 0)

                if event.key == pygame.K_a:
                    glRotatef(5, 0, -1, 0)
                if event.key == pygame.K_d:
                    glRotatef(5, 0, 1, 0)

                if event.key == pygame.K_w:
                    glRotatef(5, -1, 0, 0)
                if event.key == pygame.K_s:
                    glRotatef(5, 1, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # printKumpulan(kumpulanGedung)
        for obj in kumpulanGedung3D:
            # print(obj.vertices)
            # print(obj.edges)
            # print(obj.surfaces)
            obj.print3D()
        #printKumpulan(kumpulanPohon)
        #printKumpulan(kumpulanJalan)
        pygame.display.flip()
        pygame.time.wait(10)

main()
