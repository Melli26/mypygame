import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube():
    vertices = [
        [1, 1, 1],
        [1, 1, -1],
        [1, -1, -1],
        [1, -1, 1],
        [-1, 1, 1],
        [-1, -1, -1],
        [-1, -1, 1],
        [-1, 1, -1]
    ]

    # Define triangles using vertex indices
    triangles = [
        (0, 1, 3), (1, 2, 3),  # Right face
        (4, 5, 6), (5, 7, 4),  # Left face
        (0, 3, 4), (4, 6, 3),  # Front face
        (1, 5, 2), (1, 7, 5),  # Back face
        (0, 4, 1), (1, 7, 4),  # Top face
        (2, 5, 6), (3, 6, 2)   # Bottom face
    ]

    # Define colors for each pair of triangles
    colors = [
        (1, 0, 0), (1, 0, 0),  # Red
        (0, 1, 0), (0, 1, 0),  # Green
        (0, 0, 1), (0, 0, 1),  # Blue
        (1, 1, 0), (1, 1, 0),  # Yellow
        (1, 0, 1), (1, 0, 1),  # Magenta
        (0, 1, 1), (0, 1, 1)   # Cyan
    ]

    for i in range(0, len(triangles), 2):
        # Set color for the pair of triangles
        glColor3fv(colors[i])
        glBegin(GL_TRIANGLES)
        for vertex in triangles[i]:
            glVertex3fv(vertices[vertex])
        glEnd()

        glColor3fv(colors[i+1])
        glBegin(GL_TRIANGLES)
        for vertex in triangles[i + 1]:
            glVertex3fv(vertices[vertex])
        glEnd()

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("04 Lab 1")

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0, 0, -5)
glEnable(GL_DEPTH_TEST)  # Enable depth buffer

# Scaling the cube
glScalef(0.5, 0.5, 0.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                glTranslatef(-1, 0, 0)
            elif event.key == pygame.K_d:
                glTranslatef(1, 0, 0)
            elif event.key == pygame.K_w:
                glTranslatef(0, 1, 0)
            elif event.key == pygame.K_s:
                glTranslatef(0, -1, 0)
            elif event.key == pygame.K_DOWN:
                glRotatef(-90, 0, -90, 0)  # Rotate the cube
            elif event.key == pygame.K_UP:
                glRotatef(90, 0, 90, 0)  # Rotate the cube
            elif event.key == pygame.K_RIGHT:
                glRotatef(90, 90, 0, 0)  # Rotate the cube
            elif event.key == pygame.K_LEFT:
                glRotatef(-90, -90, 0, 0)  # Rotate the cube

    glRotatef(1, 1, 0, 0)  # Rotate the cube forward

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()
    pygame.display.flip()
    pygame.time.wait(15)
