from __future__ import print_function
from PIL import Image
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

kumpulanGedung3D = []

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
                glTexCoord2f(0.0, 0.0); glVertex3fv(self.vertices[vertex])
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
    ID = 0
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
def loadFile(namaFile):
    global kumpulanGedung3D

    f = open(namaFile, "r")
    first = True
    iterator = 0
    counter = 1
    x = 1
    print('Loading', end = '')
    for line in f:
        line = line.split('\n')[0]
        print('.', end = '')
        if first:
            iterator = int(line)
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
            elif counter == 2:
                for word in line.split():
                    edge += (int(word),)
            elif counter == 3:
                for word in line.split():
                    surface += (int(word),)
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
                    kumpulanGedung3D.append(gedung3D(verticesTemp, edgesTemp, surfacesTemp, selatan, utara, barat, timur, atas))
                first = True

#menampilkan seluruh bentuk berdasarkan kumpulan titik
def printKumpulan():
    for vertices in kumpulanGedung3D:
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glVertex2fv(vertex)
        glEnd()

# def main():
#     glutInit(sys.argv)
#     glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
#     glutInitWindowSize(640,480)
#     glutInitWindowPosition(200,200)

#     window = glutCreateWindow('OpenGL Python Textured Cube')

#     glutDisplayFunc(DrawGLScene)
#     glutIdleFunc(DrawGLScene)
#     glutKeyboardFunc(keyPressed)
#     InitGL(640, 480)
#     # loadImage('resources/2cc/barat.jpg')
#     glutMainLoop()

def main():
    loadFile("resources/gedung3d.txt")
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
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for obj in kumpulanGedung3D:
            obj.print3D()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    loadFile("resources/gedung3d.txt")
    for haha in kumpulanGedung3D:
        print(haha.atas.x)