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

UAlgorithm = "R' L' F2 B2 R L D R' L' F2 B2 R L"
UprimeAlgorithm = "R' L' F2 B2 R L D' R' L' F2 B2 R L"
U2Algorithm = "B2 R2 L2 F2 D2 B2 R2 L2 F2"

# [ corners VS edges
#    [ loop step
#       [ start VS end
#          [ y, x
# ]  ]  ]  ]
loops = [[ # Corners
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
slices = [[ # U face
    [[4, 0, 2,  1], [3, 1, 0,  1]],
    [[1, 1, 2, -1], [4, 0, 2,  1]],
    [[2, 0, 0, -1], [1, 1, 2, -1]],
    [[3, 1, 0,  1], [2, 0, 0, -1]]
],[ # L face
    [[4, 1, 0, 1], [0, 1, 0, 1]],
    [[5, 1, 0, 1], [4, 1, 0, 1]],
    [[2, 1, 0, 1], [5, 1, 0, 1]],
    [[0, 1, 0, 1], [2, 1, 0, 1]]
],[ # F face
    [[0, 0, 2,  1], [3, 0, 2,  1]],
    [[1, 0, 2,  1], [0, 0, 2,  1]],
    [[5, 0, 0, -1], [1, 0, 2,  1]],
    [[3, 0, 2,  1], [5, 0, 0, -1]]
],[ # R face
    [[4, 1, 2, 1], [5, 1, 2, 1]],
    [[0, 1, 2, 1], [4, 1, 2, 1]],
    [[2, 1, 2, 1], [0, 1, 2, 1]],
    [[5, 1, 2, 1], [2, 1, 2, 1]]
],[ # B face
    [[0, 0, 0,  1], [1, 0, 0,  1]],
    [[3, 0, 0,  1], [0, 0, 0,  1]],
    [[5, 0, 2, -1], [3, 0, 0,  1]],
    [[1, 0, 0,  1], [5, 0, 2, -1]]
],[ # D face
    [[2, 0, 2,  1], [3, 1, 2, -1]],
    [[1, 1, 0,  1], [2, 0, 2,  1]],
    [[4, 0, 0, -1], [1, 1, 0,  1]],
    [[3, 1, 2, -1], [4, 0, 0, -1]]
]]


def getSliceCoors(group): # Interprets a 1x4 element from the above 4D matrix
    dimensionalValues = [[0, 0], [0, 0], [0, 0]]
    #print("[" + str(group[0]) + ", " + str(group[1]) + ", " + str(group[2]) + ", " + str(group[3]) + "] ---> ", end="")
    for i in range(0, 3):
        dimensionalValues[i] = [
            int(round((group[1] * -1 + 1) * group[2] + group[1] * (group[3] * i - (group[3] - 1)))),
            int(round(group[1] * group[2] + (group[1] * -1 + 1) * (group[3] * i - (group[3] - 1))))
        ]
    # print("[[" + str(dimensionalValues[0][0]) + ", " + str(dimensionalValues[0][1]) + "], [" + str(dimensionalValues[1][0]) + ", " + str(dimensionalValues[1][1]) + "], [" + str(dimensionalValues[2][0]) + ", " + str(dimensionalValues[2][1]) + "]]")
    return dimensionalValues


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

    #cube rotation function by Matthew.
    #input the amount to be rotated, and then each face will have that amount applied to it (theory from Josiah)
    #example: if amount=1, then 1->2, 2->3, ... 5->0
    def rotateCube(self, amount):
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    self.sides[i][j][k] = (self.sides[i][j][k] + amount) % 6

    #check if the cube is solved
    def cubeIsSolved(self):
        for i in range(6): #loop through each face

            faceColour = self.sides[i][0][0] #grab a sample colour

            #check if any colours in the cube are not the same as the original
            for j in range(3):
                for k in range(3):
                    if self.sides[i][j][k] != faceColour:
                        return False
        return True

def cycle(cube, face, times):
    # Loop the chosen face
    for uselessVariable in range(0, times):
        pieceHold = [cube.sides[face][loops[0][0][0][0]][loops[0][0][0][1]], cube.sides[face][loops[1][0][0][0]][loops[1][0][0][1]]]
        for i in range(1, 4):
            cube.sides[face][loops[0][i][1][0]][loops[0][i][1][1]] = cube.sides[face][loops[0][i][0][0]][loops[0][i][0][1]]
            cube.sides[face][loops[1][i][1][0]][loops[1][i][1][1]] = cube.sides[face][loops[1][i][0][0]][loops[1][i][0][1]]
        cube.sides[face][loops[0][0][1][0]][loops[0][0][1][1]] = pieceHold[0]
        cube.sides[face][loops[1][0][1][0]][loops[1][0][1][1]] = pieceHold[1]

        # Cycle Sections for the chosen face
        coorFrom = getSliceCoors(slices[face][0][0])
        coorTo = []
        sliceHold = [cube.sides[slices[face][0][0][0]][coorFrom[0][0]][coorFrom[0][1]], cube.sides[slices[face][0][0][0]][coorFrom[1][0]][coorFrom[1][1]], cube.sides[slices[face][0][0][0]][coorFrom[2][0]][coorFrom[2][1]]]
        for y in range(1, 4):
            coorFrom = getSliceCoors(slices[face][y][0])
            coorTo = getSliceCoors(slices[face][y][1])
            for i in range(0, 3):
                cube.sides[slices[face][y][1][0]][coorTo[i][0]][coorTo[i][1]] = cube.sides[slices[face][y][0][0]][coorFrom[i][0]][coorFrom[i][1]]
        coorTo = getSliceCoors(slices[face][0][1])
        for i in range(0, 3):
            cube.sides[slices[face][0][1][0]][coorTo[i][0]][coorTo[i][1]] = sliceHold[i]





"""testCube = Cube(
    [[0, 1, 2], [3, 0, 5], [6, 7, 8]],
    [[2, 2, 2], [3, 1, 3], [5, 5, 5]],
    [[0, 0, 0], [1, 2, 1], [4, 4, 4]],
    [[9, 8, 7], [6, 3, 4], [3, 2, 1]],
    [[0, 1, 2], [0, 4, 2], [0, 1, 2]],
    [[5, 4, 3], [5, 5, 3], [5, 4, 3]]
)"""
"""testCube = Cube(
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
    [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
    [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
    [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
)"""
testCube = Cube(
    [[0, 0, 8], [0, 0, 0], [7, 0, 0]],
    [[1, 1, 7], [1, 1, 1], [8, 1, 1]],
    [[7, 2, 2], [2, 2, 2], [2, 2, 8]],
    [[3, 3, 8], [3, 3, 3], [7, 3, 3]],
    [[8, 4, 4], [4, 4, 4], [4, 4, 7]],
    [[5, 5, 7], [5, 5, 5], [8, 5, 5]]
)

testCube.print()

cycle(testCube, trans["D"], 1)

testCube.print()


#########################
# cube string input code:
# by Matthew PB
#########################

#changes U, U', and U2 to their respective algorithms. Also clears any leading and trailing whitespace.
def roatateCommandsParseU(str):
    str = str.replace("U", UAlgorithm)
    str = str.replace("U'", UprimeAlgorithm)
    str = str.replace("U2", U2Algorithm)
    str = str.strip()
    return str

#test of the above
str = "   D D D   U U       U2 U'"
print(roatateCommandsParseU(str))

##pass in the cube and the string of commands, and it will be rotated by said amount
def rotateCubeFromString(cube, str):

    #loop through each command
    for i in str.split():
        command = [cube,0,1] #by default, it is the 0th face and is clockwise
        command[1] = trans[i[0]]

        #checking if there is a second argument in the command
        if i.length > 1:
            if i[1] == '\'': #counter cloclwise
                command[2] = 3
            elif i[1] == '2': #180 turn
                command[2] = 2

        #call the function
        cycle(*command) #the '*' apparently is called "unpacking", which breaks the list down into arguments.