import os
import cv2
import csv
import bitboard_cube

# os.system('sudo fswebcam -d /dev/video0 ~/image1.jpg')
# os.system('sudo fswebcam -d /dev/video1 ~/image2.jpg')

with open('colors.csv') as colors_file:
    reader = csv.reader(colors_file, delimiter=',')
    color_rows = [tuple(row) for row in reader]

with open('pixels.csv') as pixels_file:
    pixel_reader = csv.reader(pixels_file, delimiter=',')
    pixel_rows = [tuple(row) for row in pixel_reader]

img1 = cv2.imread('image1.jpg', cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('image2.jpg', cv2.IMREAD_UNCHANGED)

pixel_color = {}

faces = [[-1, -1, -1, -1, bitboard_cube.UP, -1, -1, -1, -1],
         [-1, -1, -1, -1, bitboard_cube.LEFT, -1, -1, -1, -1],
         [-1, -1, -1, -1, bitboard_cube.FRONT, -1, -1, -1, -1],
         [-1, -1, -1, -1, bitboard_cube.RIGHT, -1, -1, -1, -1],
         [-1, -1, -1, -1, bitboard_cube.BACK, -1, -1, -1, -1],
         [-1, -1, -1, -1, bitboard_cube.DOWN, -1, -1, -1, -1]]


for (image, pixel, x, y, sticker, face) in pixel_rows:
    if int(image) == 1:
        b, g, r = (img1[int(y), int(x)])
    else:
        b, g, r = (img2[int(y), int(x)])
    sticker = int(sticker)
    face = int(face)

    if int(color_rows[0][0]) <= r <= int(color_rows[0][3]) and int(color_rows[0][1]) <= g <= int(
            color_rows[0][4]) and int(
            color_rows[0][2]) <= b <= int(color_rows[0][5]):
        # print(pixel + ' white')
        faces[face][sticker] = bitboard_cube.UP
    elif int(color_rows[1][0]) <= r <= int(color_rows[1][3]) and int(color_rows[1][1]) <= g <= int(
            color_rows[1][4]) and int(
            color_rows[1][2]) <= b <= int(color_rows[1][5]):
        # print(pixel + ' green')
        faces[face][sticker] = bitboard_cube.LEFT
    elif int(color_rows[2][0]) <= r <= int(color_rows[2][3]) and int(color_rows[2][1]) <= g <= int(
            color_rows[2][4]) and int(
            color_rows[2][2]) <= b <= int(color_rows[2][5]):
        # print(pixel + ' red')
        faces[face][sticker] = bitboard_cube.FRONT
    elif int(color_rows[3][0]) <= r <= int(color_rows[3][3]) and int(color_rows[3][1]) <= g <= int(color_rows[3][4]) and int(
            color_rows[3][2]) <= b <= int(color_rows[3][5]):
        # print(pixel + ' blue')
        faces[face][sticker] = bitboard_cube.RIGHT
    elif int(color_rows[4][0]) <= r <= int(color_rows[4][3]) and int(color_rows[4][1]) <= g <= int(color_rows[4][4]) and int(
            color_rows[4][2]) <= b <= int(color_rows[4][5]):
        # print(pixel + ' orange')
        faces[face][sticker] = bitboard_cube.BACK
    elif int(color_rows[5][0]) <= r <= int(color_rows[5][3]) and int(color_rows[5][1]) <= g <= int(color_rows[5][4]) and int(
            color_rows[5][2]) <= b <= int(color_rows[5][5]):
        # print(pixel + ' yellow')
        faces[face][sticker] = bitboard_cube.DOWN
    else:
        print(pixel + ' NONE', r, g, b)

cube = bitboard_cube.Cube()

cube.set_cube(faces)
cube.print_cube()