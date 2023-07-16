import tkinter as tk
import keyboard as kbd

from camera import *
from vector4 import *
from vector3 import *

# get the 3D cross-section slice of a 4D object
def slice4D(pt4, w_pos):
    wdot = pt4.w - w_pos # moving a bit in the 4th spatial dimension
    xp = pt4.x / wdot
    yp = pt4.y / wdot
    zp = pt4.z / wdot

    return vec3(xp, yp, zp)

def rotate_tesseract(vertices):
    rotate_speed_x = 0.001
    rotate_speed_y = 0.003
    # Rotate the tesseract
    for i in range(len(vertices)):
        vertex = vertices[i]
        x = vertex[0]
        y = vertex[1]
        z = vertex[2]
        w = vertex[3]

        # x rotation
        y_prime = y * math.cos(rotate_speed_x) - z * math.sin(rotate_speed_x)
        z_prime = y * math.sin(rotate_speed_x) + z * math.cos(rotate_speed_x)

        # y rotation
        x_prime = x * math.cos(rotate_speed_y) + w * math.sin(rotate_speed_y)
        w_prime = -x * math.sin(rotate_speed_y) + w * math.cos(rotate_speed_y)

        vertices[i] = vec4(x_prime, y_prime, z_prime, w_prime)

def main():
    screen_x = 1280
    screen_y = 720

    screen_x_2 = 640
    screen_y_2 = 360

    window = tk.Tk()
    window.geometry('1280x720')
    window.title("Angelorumbrae")

    canvas = tk.Canvas(window, width=screen_x, height=screen_y, bg='black')
    canvas.pack(anchor=tk.CENTER, expand=True)

    # defining a tesseract (hypercube, 4D cube)
    # this one below keeps the original vertices' definition so that we can rewrite 'points'
    # without worrying about losing references to the original vertices
    points_original = [
        vec4(-1, -1, -1, -1), vec4(1, -1, -1, -1), vec4(-1, 1, -1, -1), vec4(1, 1, -1, -1),
        vec4(-1, -1, 1, -1), vec4(1, -1, 1, -1), vec4(-1, 1, 1, -1), vec4(1, 1, 1, -1),
        vec4(-1, -1, -1, 1), vec4(1, -1, -1, 1), vec4(-1, 1, -1, 1), vec4(1, 1, -1, 1),
        vec4(-1, -1, 1, 1), vec4(1, -1, 1, 1), vec4(-1, 1, 1, 1), vec4(1, 1, 1, 1),
    ]

    points = [
        vec4(-1, -1, -1, -1), vec4(1, -1, -1, -1), vec4(-1, 1, -1, -1), vec4(1, 1, -1, -1),
        vec4(-1, -1, 1, -1), vec4(1, -1, 1, -1), vec4(-1, 1, 1, -1), vec4(1, 1, 1, -1),
        vec4(-1, -1, -1, 1), vec4(1, -1, -1, 1), vec4(-1, 1, -1, 1), vec4(1, 1, -1, 1),
        vec4(-1, -1, 1, 1), vec4(1, -1, 1, 1), vec4(-1, 1, 1, 1), vec4(1, 1, 1, 1),
    ]

    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),  # Cube bottom face
        (4, 5), (5, 7), (7, 6), (6, 4),  # Cube top face
        (0, 4), (1, 5), (2, 6), (3, 7),  # Connect bottom and top face
        (8, 9), (9, 11), (11, 10), (10, 8),  # Cube bottom face (inner)
        (12, 13), (13, 15), (15, 14), (14, 12),  # Cube top face (inner)
        (8, 12), (9, 13), (10, 14), (11, 15),  # Connect inner bottom and top face
        (0, 8), (1, 9), (2, 10), (3, 11),  # Connect outer and inner bottom face
        (4, 12), (5, 13), (6, 14), (7, 15),  # Connect outer and inner top face
    ]

    cam = camera()
    cam.pos = vec3(0, 0, -0.8)
    speed = 0.00371
    rot_speed = 0.1

    fov_scaler = 500
    point_size = 2

    w_pos = 8 # position of camera in 4th spatial dimension (ana - kata)

    running = True
    cycle = 0
    while running:

        canvas.delete("all")
        #for p in points:
           #points[points.index(p)].w = points[points.index(p)].w + 1e-3 * math.sin(cycle / 1000)# + vec4(1, 0, 0, 0) * math.sin(cycle / 900)

        rotate_tesseract(points)

        cam.move(vec3(kbd.is_pressed("L") - kbd.is_pressed("J"),
                      kbd.is_pressed("U") - kbd.is_pressed("O"),
                      kbd.is_pressed("I") - kbd.is_pressed("K")) * speed)

        if kbd.is_pressed("R"):
            w_pos += speed
        elif kbd.is_pressed("F"):
            w_pos -= speed

        if kbd.is_pressed("S"):
            cam.rotate(vec3(1, 0, 0) * rot_speed)
        elif kbd.is_pressed("W"):
            cam.rotate(vec3(-1, 0, 0) * rot_speed)

        if kbd.is_pressed("D"):
            cam.rotate(vec3(0, 1, 0) * rot_speed)
        elif kbd.is_pressed("A"):
            cam.rotate(vec3(0, -1, 0) * rot_speed)

        if kbd.is_pressed("Q"):
            cam.rotate(vec3(0, 0, 1) * rot_speed)
        elif kbd.is_pressed("E"):
            cam.rotate(vec3(0, 0, -1) * rot_speed)

        for pt in points:
            pt3 = slice4D(pt, w_pos)
            pt2 = cam.project3D(pt3)
            if pt2:
                canvas.create_oval(screen_x_2 + pt2[0] * fov_scaler - point_size,
                                   screen_y_2 - pt2[1] * fov_scaler - point_size,
                                   screen_x_2 + pt2[0] * fov_scaler + point_size,
                                   screen_y_2 - pt2[1] * fov_scaler + point_size,
                                   fill="blue")

        for e in edges:
            pt_1 = points[e[0]]
            pt_2 = points[e[1]]

            pt3_1 = slice4D(pt_1, w_pos)
            pt3_2 = slice4D(pt_2, w_pos)

            pt2_1 = cam.project3D(pt3_1)
            pt2_2 = cam.project3D(pt3_2)

            if pt2_1 and pt2_2:
                canvas.create_line(screen_x_2 + pt2_1[0] * fov_scaler,
                                   screen_y_2 - pt2_1[1] * fov_scaler,
                                   screen_x_2 + pt2_2[0] * fov_scaler,
                                   screen_y_2 - pt2_2[1] * fov_scaler,
                                   fill="red")

        canvas.update()
        window.update()
        cycle += 1

    window.mainloop()

main()
