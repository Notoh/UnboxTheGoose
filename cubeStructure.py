# The Cube Structure System
# Author: Josiah Plett
# Date: Nov 5th 2021



# Examples of how Cube class works:
"""
Cube.sides[trans["U"]] = [
    [0, 3, 5],
    [0, 3, 4],
    [2, 1, 1]
]

U turn:
Cube.turn(trans["U"], 1)

U' turn:
Cube.turnU(trans["U"], -1)

U2 turn:
Cube.turnU(2)
"""

trans = {"U": 0, "L": 1, "F": 2, "R": 3, "B": 4, "D": 5}
unTrans = ["U", "L", "F", "R", "B", "D"]

# [ corners VS edges
#    [ loop step
#       [ start VS end
#          [ y, x
# ]  ]  ]  ]
loop = [[ # Corners
    [[0, 0], [0, 2]],
    [[2, 0], [0, 0]],
    [[2, 2], [2, 0]],
    [[0, 2], [2, 2]]
],[ # Edges
    [[1, 0], [0, 1]],
    [[2, 1], [1, 0]],
    [[1, 2], [2, 1]],
    [[0, 1], [1, 2]]
]]

# [ face 
#    [ loop step
#       [ start VS end
#          [ Face, Axis (slice), Index (slice), Direction (slice)
# ]  ]  ]  ]
section = [[ # U face
    [[5, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [5, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
],[ # L face
    [[5, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [5, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
],[ # F face
    [[5, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [5, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
],[ # R face
    [[5, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [5, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
],[ # D face
    [[5, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [5, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
],[ # B face
    [[5, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [5, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
]]

class Cube:
    def __init__(self, U, L, F, R, B, D):
        self.sides = [U, L, F, R, B, D]

    def print(self):
        # B face
        print("          ___________")
        for y in range(0, 3):
            print("          |  ", end = "")
            for x in range(0, 3):
                print(str(self.sides[4][y][x]) + " ", end = "")
            print(" |")

        # L, U, R faces
        faces = [1, 0, 3]
        print("__________|_________|__________")
        for y in range(0, 3):
            for value in faces:
                print("|  ", end="")
                for x in range(0, 3):
                    print(str(self.sides[value][y][x]) + " ", end = "")
                print(" ", end="")
            print("|")
        print("|_________|_________|_________|")
        # F, D faces
        faces = [2, 5]
        for value in faces:
            for y in range(0, 3):
                print("          |  ", end = "")
                for x in range(0, 3):
                    print(str(self.sides[value][y][x]) + " ", end = "")
                print(" |")
            print("          |_________|")
        print("")

    def turn(face, dir):
        #match face:
            #case 0:
        pass


def cycle(cube, face, dir):
    # Loop the chosen face
    mainHold = [cube.sides[face][loop[0][0][0][0]][loop[0][0][0][1]], cube.sides[face][loop[1][0][0][0]][loop[1][0][0][1]]]
    for i in range(1, 4):
        cube.sides[face][loop[0][i][1][0]][loop[0][i][1][1]] = cube.sides[face][loop[0][i][0][0]][loop[0][i][0][1]]
        cube.sides[face][loop[1][i][1][0]][loop[1][i][1][1]] = cube.sides[face][loop[1][i][0][0]][loop[1][i][0][1]]
    cube.sides[face][loop[0][0][1][0]][loop[0][0][1][1]] = mainHold[0]
    cube.sides[face][loop[1][0][1][0]][loop[1][0][1][1]] = mainHold[1]

    # Cycle Sections for the chosen face
    

        


testCube = Cube(
    [[0, 1, 2], [3, 0, 5], [6, 7, 8]],
    [[2, 2, 2], [3, 1, 3], [5, 5, 5]],
    [[0, 0, 0], [1, 2, 1], [4, 4, 4]],
    [[9, 8, 7], [6, 3, 4], [3, 2, 1]],
    [[0, 1, 2], [0, 4, 2], [0, 1, 2]],
    [[5, 4, 3], [5, 5, 3], [5, 4, 3]]
)

testCube.print()

cycle(testCube, trans["U"], 1)

testCube.print()