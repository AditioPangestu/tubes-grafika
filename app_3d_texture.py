from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import pygame
    
ESCAPE = '\033'
 
window = 0
ID = 0

#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0

DIRECTION = 1

#cube
X_cube = 2.0
Y_cube = 1.0
Z_cube = 1.0

image = []

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
 
def keyPressed(*args):
        if args[0] == ESCAPE:
                sys.exit()
 
 
def DrawGLScene():
        global X_AXIS,Y_AXIS,Z_AXIS
        global DIRECTION
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
        glLoadIdentity()
        glTranslatef(0.0,0.0,-6.0)
 
        #glRotatef(X_AXIS,1.0,0.0,0.0)
        glRotatef(Y_AXIS,0.0,1.0,0.0)
        #glRotatef(Z_AXIS,0.0,0.0,1.0)
         
        # Draw Cube (multiple quads)
        loadImage('resources/2cc/barat.jpg')
        '''FRONT'''
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0); glVertex3f(-X_cube, -Y_cube,  Z_cube);
        glTexCoord2f(1.0, 0.0); glVertex3f( X_cube, -Y_cube,  Z_cube);
        glTexCoord2f(1.0, 1.0); glVertex3f( X_cube,  Y_cube,  Z_cube);
        glTexCoord2f(0.0, 1.0); glVertex3f(-X_cube,  Y_cube,  Z_cube);
        glEnd();

        '''BACK'''
        loadImage('resources/2cc/timur.jpg')
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0); glVertex3f(-X_cube, -Y_cube, -Z_cube);
        glTexCoord2f(0.0, 1.0); glVertex3f(-X_cube,  Y_cube, -Z_cube);
        glTexCoord2f(1.0, 1.0); glVertex3f( X_cube,  Y_cube, -Z_cube);
        glTexCoord2f(1.0, 0.0); glVertex3f( X_cube, -Y_cube, -Z_cube);
        glEnd();
 #        '''TOP'''
 #        glTexCoord2f(0.0, 0.0); glVertex3f(-X_cube,  Y_cube, -Z_cube);
 #        glTexCoord2f(1.0, 0.0); glVertex3f(-X_cube,  Y_cube,  Z_cube);
 #        glTexCoord2f(1.0, 1.0); glVertex3f( X_cube,  Y_cube,  Z_cube);
 #        glTexCoord2f(0.0, 1.0); glVertex3f( X_cube,  Y_cube, -Z_cube);

 #        '''BOTTOM'''
 #        glTexCoord2f(0.0, 0.0); glVertex3f(-X_cube, -Y_cube, -Z_cube);
 #        glTexCoord2f(1.0, 0.0); glVertex3f( X_cube, -Y_cube, -Z_cube);
 #        glTexCoord2f(1.0, 1.0); glVertex3f( X_cube, -Y_cube,  Z_cube);
 #        glTexCoord2f(0.0, 1.0); glVertex3f(-X_cube, -Y_cube,  Z_cube);

        '''RIGHT'''
        loadImage('resources/2cc/selatan.jpg')
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0); glVertex3f( X_cube, -Y_cube,  Z_cube);
        glTexCoord2f(1.0, 0.0); glVertex3f( X_cube, -Y_cube, -Z_cube);
        glTexCoord2f(1.0, 1.0); glVertex3f( X_cube,  Y_cube, -Z_cube);
        glTexCoord2f(0.0, 1.0); glVertex3f( X_cube,  Y_cube,  Z_cube);
        glEnd();

        '''LEFT'''
        loadImage('resources/2cc/utara.jpg')
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0); glVertex3f(-X_cube, -Y_cube, Z_cube);
        glTexCoord2f(1.0, 0.0); glVertex3f(-X_cube, -Y_cube, -Z_cube);
        glTexCoord2f(1.0, 1.0); glVertex3f(-X_cube,  Y_cube, -Z_cube);
        glTexCoord2f(0.0, 1.0); glVertex3f(-X_cube,  Y_cube, Z_cube);
        glEnd();
 
        X_AXIS = X_AXIS - 2
        Z_AXIS = Z_AXIS - 2
        Y_AXIS = Y_AXIS - 2
 
        glutSwapBuffers()
 
 
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
      
def main():
    global window
    global ID

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutInitWindowPosition(200,200)

    window = glutCreateWindow('OpenGL Python Textured Cube')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    # loadImage('resources/2cc/barat.jpg')
    glutMainLoop()
 
if __name__ == "__main__":
        main() 