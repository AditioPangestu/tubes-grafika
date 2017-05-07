import pygame
from pygame.locals import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *

ID = 0
image = []

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

class Gambar:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

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
                drawImage(self.atas)
            elif counter == 3:
                drawImage(self.utara)
            elif counter == 4:
                drawImage(self.barat)
            elif counter == 5:
                drawImage(self.selatan)
            elif counter == 6:
                drawImage(self.timur)
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
      image = pygame.image.load('resources/' + filename)
      ix = image.get_width()
      iy = image.get_height()
      return Gambar(pygame.image.tostring(image, "RGBA", 1), ix, iy)

def drawImage(image):
      glBindTexture(GL_TEXTURE_2D, ID)
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
def loadFile(kumpulan, namaFile):
    f = open(namaFile, "r")
    first = True
    iterator = 0
    counter = 1
    x = 1
    for line in f:
        line = line.split('\n')[0]
        print line
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
            selatan = ''
            utara = ''
            barat = ''
            timur = ''
            atas = ''
        else :
            vertex = ()
            edge = ()
            surface = ()
            if counter == 1:
                for word in line.split():
                    vertex += (float(word)/10,)
                verticesTemp += (vertex, )
            elif counter == 2:
                for word in line.split():
                    edge += (int(word),)
                edgesTemp += (edge, )
            elif counter == 3:
                for word in line.split():
                    surface += (int(word),)
                surfacesTemp += (surface, )
            elif counter == 4:
                if x == 1:
                    selatan = loadImage(str(line))
                elif x == 2:
                    utara = loadImage(str(line))
                elif x == 3:
                    barat = loadImage(str(line))
                elif x == 4:
                    timur = loadImage(str(line))
                elif x == 5:
                    atas = loadImage(str(line))
                x += 1
            iterator -= 1
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
    global ID

    # kumpulanGedung = []
    kumpulanGedung3D = []
    # kumpulanPohon = []
    # kumpulanJalan = []
    #migrasi file eksternal ke memori
    # loadFile(kumpulanGedung,"resources/gedung.txt")
    loadFile(kumpulanGedung3D, "resources/gedung3d.txt")
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