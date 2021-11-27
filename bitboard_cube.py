import collections
import time

UP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
BACK = 4
DOWN = 5

TRANSLATE_FACE = {"U": UP, "L": LEFT, "F": FRONT, "R": RIGHT, "B": BACK, "D": DOWN}

# ALEX, put all your colours in TRANSLATE_COLOR[your_color]
TRANSLATE_COLOR = [0, 2, 3, 4, 1, 5]

FACE_NUM = 6
STICKER_NUM = 8
STICKER_CENTER_EXTERNAL_INDEX = 4
STICKER_CENTER_INTERNAL_INDEX = 8
STICKER_BIT_SIZE = 4
STICKER_MASK = 15

FACE_COMPLETENESS_MASK = [0,286331153,572662306,858993459,1145324612,1431655765]

PROCESS_DIRECTION = {"'": 3, "2": 2}

#cube adj edges, [internal_face_index, s1, s2, s3]
adj_edges = [
    #UP
    [
        [4, 6, 5, 4], [3, 0, 7, 6], [2, 2, 1, 0], [1, 4, 3, 2]
    ],
    #LEFT
    [
        [4, 0, 7, 6], [0, 0, 7, 6], [2, 0, 7, 6], [5, 0, 7, 6]
    ],
    #FRONT
    [
        [1, 6, 5, 4], [0, 6, 5, 4], [3, 6, 5, 4], [5, 2, 1, 0]
    ],
    #RIGHT
    [
        [0, 4, 3, 2], [4, 4, 3, 2], [5, 4, 3, 2], [2, 4, 3, 2]
    ],
    #BACK
    [
        [5, 6, 5, 4], [3, 2, 1, 0], [0, 2, 1, 0], [1, 2, 1, 0]
    ],
    #DOWN
    [
        [2, 6, 5, 4], [3, 4, 3, 2], [4, 2, 1, 0], [1, 0, 7, 6]
    ]
]

#For each face, there is 1 subarray for each corner, with indices: 0,2,4,6
#in the sub array, it says the face number and internal_index of the sticker of the same cubie x2 (as there are two adjacent stickers on different faces)
adj_corner = [
    #UP
    [
        [1, 2, 4, 6], [4, 4, 3, 0], [3, 6, 2, 2], [2, 0, 1, 4]
    ],
    #LEFT
    [
        [4, 0, 5, 6], [0, 0, 4, 6], [0, 6, 2, 0], [2, 6, 5, 0]
    ],
    #FRONT
    [
        [0, 6, 1, 4], [0, 4, 3, 6], [5, 2, 3, 4], [5, 0, 1, 6]
    ],
    #RIGHT
    [
        [0, 2, 4, 4], [4, 2, 5, 4], [2, 4, 5, 2], [0, 4, 2, 2]
    ],
    #BACK
    [
        [1, 0, 5, 6], [3, 2, 5, 4], [0, 2, 3, 0], [0, 0, 1, 2]
    ],
    #DOWN
    [
        [2, 6, 1, 6], [2, 4, 3, 4], [3, 2, 4, 2], [1, 0, 4, 0]
    ]
]

#For each face, there is 1 subarray for each side, with indices: 1,3,5,7
#in the sub array, it says the face number and internal_index of the sticker on the other part of the cubie
adj_side = [
    #UP
    [
        [4, 5], [3, 7], [2, 1], [1, 3]
    ],
    #LEFT
    [
        [4, 7], [0, 7], [2, 7], [5, 7]
    ],
    #FRONT
    [
        [0, 5], [3, 5], [5, 1], [1, 5]
    ],
    #RIGHT
    [
        [4, 3], [5, 3], [2, 3], [0, 3]
    ],
    #BACK
    [
        [5, 5], [3, 1], [0, 1], [1, 1]
    ],
    #DOWN
    [
        [2, 5], [3, 3], [4, 1], [1, 7]
    ]
]

#cube orientation, index 8 is the center sticker
EXTERNAL_TO_INTERNAL = [
    [0, 1, 2, 7, 8, 3, 6, 5, 4],#UP
    [2, 3, 4, 1, 8, 5, 0, 7, 6],#LEFT
    [0, 1, 2, 7, 8, 3, 6, 5, 4],#FRONT
    [6, 7, 0, 5, 8, 1, 4, 3, 2],#RIGHT
    [4, 5, 6, 3, 8, 7, 2, 1, 0],#BACK
    [0, 1, 2, 7, 8, 3, 6, 5, 4]#DOWN
]


class Cube:

    #an array of 32 bit intergers
    faces = []


    def __init__(self):

        #set to solved configuration
        self.faces = FACE_COMPLETENESS_MASK.copy()



    #Private Methods
                
    '''
    args: face's index, sticker's internal index
    return: sticker's color
    '''
    def __get_color(self, face_index : int, internal_sticker_index : int) -> int:
        
        return self.faces[face_index] >> (internal_sticker_index * STICKER_BIT_SIZE) & STICKER_MASK

    
    '''
    args: face's index, sticker's internal index
    return: sticker's color
    '''
    def __set_color(self, face_index : int, internal_sticker_index : int, new_sticker_color : int):

        shift_bits = internal_sticker_index * STICKER_BIT_SIZE
        self.faces[face_index] &= ~(STICKER_MASK << shift_bits)
        self.faces[face_index] |= new_sticker_color << shift_bits


    #Public Methods:
    '''
    args: array representation of cube's faces
    return:
    Set up the cube given by the face array
    '''
    def set_cube(self, new_cube):

        for new_face in new_cube:
            face_index = new_face[STICKER_CENTER_EXTERNAL_INDEX]

            for sticker_index in range(STICKER_NUM + 1):
                if sticker_index != STICKER_CENTER_EXTERNAL_INDEX:
                    internal_index = EXTERNAL_TO_INTERNAL[face_index][sticker_index]
                    new_color = new_face[sticker_index]
                    self.__set_color(face_index, internal_index, new_color)
                

            
    '''
    args: face's index, sticker's index
    return: sticker's color
    '''
    def get_color(self, face_index : int, sticker_index : int) -> int:

        internal_sticker_index = EXTERNAL_TO_INTERNAL[face_index][sticker_index]
        
        if internal_sticker_index == STICKER_CENTER_INTERNAL_INDEX:
            return face_index
        
        return self.__get_color(face_index, internal_sticker_index)

    
        
    '''
    args: face's index
    return: true if the face is completed
    '''
    #@cache
    def is_face_completed(self, face_index : int) -> bool:
        return (self.faces[face_index] == FACE_COMPLETENESS_MASK[face_index])

    
    '''
    args:
    return: true if the cube is completed
    '''
    #@cache
    def is_cube_completed(self) -> bool:
        
        for face_index in range(FACE_NUM-1):
            if not self.is_face_completed(face_index):
                return False
        return True


    '''
    args: face's index, clockwise rotating times
    return:

    Rotating the stickers in a face clockwise
    '''
    #@cache
    def rotate(self, face_index : int, times : int):

        assert(0 <= times <= 4)

        #rotate face
        left_shift_bits = 2 * times * STICKER_BIT_SIZE
        right_shift_bits = 32 - left_shift_bits

        left_bits = (self.faces[face_index] << left_shift_bits) & ((1 << 32) - 1)
        right_bits = self.faces[face_index] >> right_shift_bits

        self.faces[face_index] = left_bits | right_bits


        # print(bin(self.faces[face_index]))


        #collect adjacent edges to rotate
        edges_lst = collections.deque()

        for arr in adj_edges[face_index]:
            edges = []
            for sticker_index in arr[1:4]:
                edges.append(self.__get_color(arr[0], sticker_index))

            edges_lst.append(edges)


        #rotate clockwise
        edges_lst.rotate(times)

        for i in range(4):
            for j in range(3):
                self.__set_color(adj_edges[face_index][i][0], adj_edges[face_index][i][j+1], edges_lst[i][j])

    '''
    args: side_count (2 or 3), [priority colour (which colour's face do you want), other 1 or 2 colours (based on corner vs side)]
    return: [face_index of priority colour, external_index of priority colour]

    Find the location of a specific piece on the cube.
    '''
    def find_piece(self, side_count : int, colors):
        for face_index in range(FACE_NUM):

            #hunting for corner location
            if (side_count == 3):
                for target_color_external_index in [0,2,6,8]: #corners are always on even external indices, excluding the middle 4

                    #see if a corner has the right target color
                    if (self.get_color(face_index,target_color_external_index) == colors[0]):

                        #check if the other two stickers on the corner cubie are the right colours
                        internal_sticker_corner_index = (int)((EXTERNAL_TO_INTERNAL[face_index][target_color_external_index]) / 2)
                        neighbour_sticker_color_one = self.__get_color(adj_corner[face_index][internal_sticker_corner_index][0],adj_corner[face_index][internal_sticker_corner_index][1])
                        neighbour_sticker_color_two = self.__get_color(adj_corner[face_index][internal_sticker_corner_index][2],adj_corner[face_index][internal_sticker_corner_index][3])

                        #compare the colours
                        if ((neighbour_sticker_color_one == colors[1] and neighbour_sticker_color_two == colors[2]) or (neighbour_sticker_color_one == colors[2] and neighbour_sticker_color_two == colors[1])):
                            return list([face_index, target_color_external_index])

            #hunting for edge location
            if (side_count == 2):
                for target_color_external_index in [1,3,5,7]: #edges are always on odd external indices

                    #see if a side piece has the right target color
                    if (self.get_color(face_index,target_color_external_index) == colors[0]):

                        #check if the other sticker on the cubie is the right colour. This index is for the adj_side list.
                        internal_sticker_side_index = (int)((EXTERNAL_TO_INTERNAL[face_index][target_color_external_index] - 1) / 2)
                        neighbour_sticker_color = self.__get_color(adj_side[face_index][internal_sticker_side_index][0], adj_side[face_index][internal_sticker_side_index][1])
                        
                        #compare the colour
                        if (neighbour_sticker_color == colors[1]):
                            return list([face_index, target_color_external_index])
        
        #return an error list when the corner was not found. Either broken code or invalid input
        return [-1, -1]
    
    '''
    args:  [priority colour (which colour's face do you want), other 1 or 2 colours (based on corner vs side)]
    return: [face_index of priority colour, external_index of priority colour]

    Find the location of a specific piece on the cube.
    
    def find_piece(self, colors: list[int]) -> list[int]:
        side_count = len(colors)
        return self.find_piece(side_count, colors)
    '''

    '''
    args: face'index, placeholder string
    return:

    Print all stickers' color on a face
    '''
    def print_face(self, face_index : int, placeholder : str):
        
        print(placeholder + str(self.__get_color(face_index, 0)), end = '')

        print(self.__get_color(face_index, 1), end = '')
        print(self.__get_color(face_index, 2))
        
        print(placeholder + str(self.__get_color(face_index, 7)), end = '')
        print(face_index, end = '')
        print(self.__get_color(face_index, 3))
        
        print(placeholder + str(self.__get_color(face_index, 6)), end = '')
        print(self.__get_color(face_index, 5), end = '')
        print(self.__get_color(face_index, 4))


    '''
    args:
    return:

    Print the entire cube
    '''
    def print_cube(self):
        
        self.print_face(4, "   ")
        

        for face_index in [1, 0, 3]:
            for sticker_index in range(3):
                print(self.__get_color(face_index, sticker_index), end = '')
        print("")

        
        for face_index in [1, 0, 3]:
            print(self.__get_color(face_index, 7), end = '')
            print(face_index, end = '')
            print(self.__get_color(face_index, 3), end = '')
        print("")

        
        for face_index in [1, 0, 3]:
            for sticker_index in [6, 5, 4]:
                print(self.__get_color(face_index, sticker_index), end = '')
        print("")

        
        self.print_face(2, "   ")
        self.print_face(5, "   ")
        print("\n")

    '''
    args: string of moves

    Executes the moves passed to it, replacing any U, U', or U2 with the correct move set.
    '''
    def do_moves(self, moves, inverse = False):
        moves = moves.split()
        moves = list(map(lambda m: [m, 1] if len(m) == 1 else [m[0], PROCESS_DIRECTION[m[1]]], moves))
        for move in moves:
            if (not(inverse)):
                if (move[0] != ""):
                    self.rotate(TRANSLATE_FACE[move[0]], move[1])
            else:
                if (move[0] != ""):
                    move[1] = move[1] * -1 + 4
        if (inverse):
            for move in reversed(moves):
                if (move[0] != ""):
                    self.rotate(TRANSLATE_FACE[move[0]], move[1])
    
    '''
    Returns (and performs) the moves required to solve PLL
    '''
    def solve_PLL(self):
        for adjust in ["", "U", "U'", "U2"]:
            self.do_moves(adjust)
            for PLLalg in PLL:
                self.do_moves(PLL[PLLalg])
                for auf in ["", "U", "U'", "U2"]:
                    self.do_moves(auf)
                    if (self.is_cube_completed()):
                        return adjust + " " + PLL[PLLalg] + " " + auf 
                    self.do_moves(auf, True)
                self.do_moves(PLL[PLLalg], True)
            self.do_moves(adjust, True)
        return False # If this happens, cube is not at PLL yet.

    '''
    Returns (and performs) the moves required to solve OLL
    '''
    def solve_OLL(self):
        for adjust in ["", "U", "U'", "U2"]:
            self.do_moves(adjust)
            for OLLalg in OLL:
                self.do_moves(OLL[OLLalg])
                if (self.is_face_completed(UP)):
                    return adjust + " " + OLL[OLLalg]
                self.do_moves(OLL[OLLalg], True)
            self.do_moves(adjust, True)
        return False # If this happens, cube is not at OLL yet.

    '''
    Returns (and performs) the moves required to solve the whole Last Layer!!!
    '''
    def solve_LL(self):
        OLLSolution = self.solve_OLL()
        PLLSolution = self.solve_PLL()
        if (OLLSolution != False and PLLSolution != False): return OLLSolution + " " + PLLSolution
        return False # If this happens, cube is not at LL yet.
            
    def cross_piece_solved(self, edge_color):
        piece = self.find_piece(2, [edge_color, 5])
        return True if (piece[0] == edge_color and piece[1] == 7) else False
    
    def F2L_pair_solved(self, left_color, right_color):
        corner = self.find_piece(3, [left_color, right_color, 5])
        edge = self.find_piece(2, [left_color, right_color])
        if (corner[0] != left_color or edge[0] != left_color): return False
        if (corner[1] != 8 or edge[1] != 5): return False
        return True
    
    '''
    Find the corner; if you subtract left_color from this value, you get 0 for ready-to-go and 4 for being in own slot
    '''
    def corner_slot(self, left_color, right_color, end_color = 5):
        corner = self.find_piece(3, [end_color, left_color, right_color])
        return CORNER_MAP[str(corner[0]) + str(corner[1])]
    
    '''
    Find the edge: return -1 if not in slot, otherwise, return the slot, one of [1, 2, 3, 4]
    '''
    def edge_slot(self, first_color, second_color):
        edge = self.find_piece(2, [first_color, second_color])
        if (edge[0] == 0 or edge[0] == 5 or edge[1] < 3 or edge[1] > 5): return -1
        if (edge[1] == 3): return (edge[0] + 2) % 4 + 1
        else: return edge[0]
        
    def orient_alg(self, alg, rotations):
        if (rotations <= 0): return alg
        alg = list(map(lambda move: MOVE_MAP[move], alg.split()))
        alg = ' '.join(alg)
        if (rotations == 1): return alg
        else: return self.orient_alg(alg, rotations - 1)
    
    '''
    Returns (and performs) the moves required to solve the Cross.
    '''
    def solve_Cross(self, pieces = [1, 2, 3, 4], moves = ""):
        #edges = list(map(lambda i: self.find_piece(2, [i, 5]), pieces))
        shortest_solutions = list(map(lambda i: "U U U U U U U U", pieces))
        for i in range(len(pieces)):
            for alg in CROSS:
                possible_solution = self.orient_alg(alg, pieces[i] - 1)
                self.do_moves(possible_solution)
                if self.cross_piece_solved(pieces[i]):
                    if alg == "":
                        if len(pieces) == 1:
                            print("Cross Piece " + str(pieces[i]) + ": ")
                            return moves
                        else:
                            print("Cross Piece " + str(pieces[i]) + ": ")
                            del pieces[i]
                            return self.solve_Cross(pieces, moves)
                    shortest_solutions[i] = possible_solution
                    self.do_moves(possible_solution, True)
                    break
                self.do_moves(possible_solution, True)
        length_of_algs = list(map(lambda alg: alg.count(" "), shortest_solutions))
        index_min = min(range(len(length_of_algs)), key=length_of_algs.__getitem__)
        this_alg = shortest_solutions[index_min]
        self.do_moves(this_alg)
        #print("Solutions: " + str(shortest_solutions) + "  --  Just did: " + this_alg)
        moves += (" " + this_alg)
        print("Cross Piece " + str(pieces[index_min]) + ": " + this_alg)
        if len(pieces) == 1:
            return moves
        else:
            del pieces[index_min]
            return self.solve_Cross(pieces, moves)
    
    '''
    Returns (and performs) the moves required to solve all of F2L!!!.
    '''
    def solve_F2L(self, pairs = [1, 2, 3, 4], moves = ""):
        # For each of the pairs...
        # Find where the corner is.
        # If in any slot, do setup, unless F2L_pair_solved!!!
        # Find where corner is again, put in the relative back-left...
        # Run through every F2L solution, and check if pair solved at the end of each.
        # If solved, do what i did for cross
        # otherwise, undo move and repeat
        # Way afterwards, find the shortest solution!
        # Then be recursive
        solutions = list(map(lambda i: "                        ", pairs))
        curr_moves = ""
        for i in range(len(pairs)):
            curr_moves = ""
            setup_alg = ""
            corner_spot = self.corner_slot(pairs[i], pairs[i] % 4 + 1)
            #print("Corner: " + str(corner_spot))
            edge_spot = self.edge_slot(pairs[i], pairs[i] % 4 + 1)
            #print("Edge: " + str(edge_spot))
            if (corner_spot > 4): # In a slot!
                if (edge_spot == -1): setup_alg = self.orient_alg(F2L_SETUP[0], corner_spot - 5)
                else: setup_alg = self.orient_alg(F2L_SETUP[(edge_spot - corner_spot + 8) % 4], corner_spot - 5)
                self.do_moves(setup_alg)
                curr_moves = setup_alg
            corner_spot = self.corner_slot(pairs[i], pairs[i] % 4 + 1)
            if (corner_spot > 4): # Hashtag FAILURE
                print("\nThe setup for this F2L pair FAILED!!\ncorner: " + str(corner_spot) + ", edge: " + str(edge_spot) + ", color: " + pairs[i] + "\n")
                self.do_moves(setup_alg, True)
            else: # Piece is properly set up
                setup_adjust = ""
                if ((corner_spot - pairs[i] + 5) % 4 == 2): setup_adjust = "U"
                elif ((corner_spot - pairs[i] + 5) % 4 == 3): setup_adjust = "U2"
                elif ((corner_spot - pairs[i] + 5) % 4 == 0): setup_adjust = "U'"
                self.do_moves(setup_adjust)
                if ((corner_spot - pairs[i] + 5) % 4 != 1): curr_moves += (" " + setup_adjust)

                #print("Setup: " + curr_moves)

                for alg in F2L:
                    possible_solution = self.orient_alg(alg, pairs[i] - 1)
                    self.do_moves(possible_solution)
                    if self.F2L_pair_solved(pairs[i], pairs[i] % 4 + 1):
                        if len(pairs) == 1:
                            print("F2L Pair " + str(pairs[i]) + ": Skip!")
                            return (moves + " " + curr_moves + " " + possible_solution)
                        solutions[i] = curr_moves + " " + possible_solution
                        self.do_moves(possible_solution, True)
                        break
                    self.do_moves(possible_solution, True)
                self.do_moves(setup_adjust, True)
                self.do_moves(setup_alg, True)
        length_of_algs = list(map(lambda alg: alg.count(" "), solutions))
        index_min = min(range(len(length_of_algs)), key=length_of_algs.__getitem__)
        this_alg = solutions[index_min]
        self.do_moves(this_alg)
        #print("Solutions: " + str(solutions) + "  --  Just did: " + this_alg)
        moves += (" " + this_alg)
        print("F2L Pair " + str(pairs[index_min]) + ": " + this_alg)
        if len(pairs) == 1:
            return moves
        else:
            del pairs[index_min]
            return self.solve_F2L(pairs, moves)
    
    def solve_cube(self):
        cross_solution = self.solve_Cross()
        print("Solution to Cross: " + cross_solution + "\n")
        F2L_solution = self.solve_F2L()
        print("Solution to First 2 Layers: " + F2L_solution + "\n")
        OLL_solution = self.solve_OLL()
        print("Solution to Orienting Last Layer: " + OLL_solution + "\n")
        PLL_solution = self.solve_PLL()
        print("Solution to Permuting Last Layer: " + PLL_solution + "\n")
        print("---SOLUTION---")
        TOTAL_solution = cross_solution + F2L_solution + " " + OLL_solution + " " + PLL_solution
        print(TOTAL_solution + "\n")
        return TOTAL_solution
    
    '''
    Returns an array full of instructions.
    Format: [[Motor, # of rotations, rotation direction] ... ]
    '''
    def parse_instructions(self, moves):
        moves = moves.strip()
        moves = " ".join(moves.split())
        instructions = moves.split()
        instructions2 = list(map(lambda e: e if e != " " else "", instructions))
        instructions3 = []
        for index in range(len(instructions2)):
            #print("-" + instructions2[index] + "-", end="")
            if instructions2[index] != "":
                info = [TRANSLATE_FACE[instructions2[index][0]], 1, 1]
                if len(instructions2[index]) > 1:
                    if instructions2[index][1] == "'": info[2] = -1
                    else: info[1] = 2
                #print(" " + str(info))
                instructions3.append(info)
        return instructions3



'''
Test 1276 Last Layer positions! (starts on a solved cube)
'''
def test1276(cube):
    for OLLalg in OLL:
        cube.do_moves(OLL[OLLalg])
        for PLLalg in PLL:
            cube.do_moves(PLL[PLLalg])
            #print("\n" + OLLalg + " + " + PLLalg + "\n")
            solved = cube.solve_LL()
            if (solved == False): return False
            #cube.print_cube()
    return True

''' ALGORITHMS! '''

# resource: https://www.speedsolving.com/wiki/index.php/PLL
# resource 2: http://algdb.net/puzzle/333/pll

PLL = {
    "Skip": "", # Skip
    "Aa": "R' F R' B2 R F' R' B2 R2", # Aa
    "Ab": "R2 B2 R F R' B2 R F' R", # Ab
    "E": "R B' R' F R B R' F' R B R' F R B' R' F'", # E
    "F": "R' U R U' R2 F' U' F U R F R' F' R2", # F
    "Ga": "R L U2 R' L' B' U F' U2 B U' F", # Ga
    "Gb": "F' U B' U2 F U' B L R U2 L' R'", # Gb
    "Gc": "L' R' U2 L R F U' B U2 F' U B'", # Gc
    "Gd": "B U' F U2 B' U F' R' L' U2 R L", # Gd
    "H": "L R U2 L' R' F' B' U2 F B", # H
    "Ja": "R U' L' U R' U2 L U' L' U2 L", # Ja
    "Jb": "L' U R U' L U2 R' U R U2 R'", # Jb
    "Na": "R U' L U2 R' U L' R U' L U2 R' U L'", # Na
    "Nb": "R' U L' U2 R U' L R' U L' U2 R U' L", # Nb
    "Ra": "F2 L2 U F U F' U' F' U' L2 F' U F' U'", # Ra
    "Rb": "R' U2 R U2 R' F R U R' U' R' F' R2", # Rb
    "T": "F R U' R' U R U R2 F' R U R U' R'", # T
    "Ua": "R2 U' R' U' R U R U R U' R", # Ua
    "Ub": "R' U R' U' R' U' R' U R U R2", # Ub
    "V": "R' U R' U' B' R' B2 U' B' U B' R B R", # V
    "Y": "F R' F R2 U' R' U' R U R' F' R U R' U' F'", # Y
    "Z": "R U R' U R' U' R' U R U' R' U' R2 U R" # Z
}

# resource: https://www.speedsolving.com/wiki/index.php/OLL

OLL = {
    "Skip": "",
    "1": "R U B' R B R2 U' R' F R F'",
    "2": "F R' F' R U R2 B' R' B U' R'",
    "3": "B U L U' L' B' U' F R U R' U' F'",
    "4": "F U R U' R' F' U B L U L' U' B'",
    "5": "R' F2 L F L' F R",
    "6": "L F2 R' F' R F' L'",
    "7": "B L F' L F L2 B'",
    "8": "R U2 R' U2 R' F R F'",
    "9": "R' U' R U' R' U R' F R F' U R",
    "10": "R U R' U R' F R F' R U2 R'",
    "11": "F' L' U' L U F R B U B' U' R'",
    "12": "F R U R' U' F' U F R U R' U' F'",
    "13": "F U R U2 R' U' R U R' F'",
    "14": "F' U' L' U2 L U L' U' L F",
    "15": "R' F' R L' U' L U R' F R",
    "16": "R B R' L U L' U' R B' R'",
    "17": "R U R' U R' F R F' U2 R' F R F'",
    "18": "F R U R' U F' U2 F' L F L'",
    "19": "L' R B R B R' B' L R2 F R F'",
    "20": "L' R' F' U2 L2 U2 L2 U2 L2 F L R",
    "21": "R U R' U R U' R' U R U2 R'",
    "22": "R U2 R2 U' R2 U' R2 U2 R",
    "23": "R' U2 R F U' R' U' R U F'",
    "24": "L F R' F' L' F R F'",
    "25": "R' F R B' R' F' R B",
    "26": "R U2 R' U' R U' R'",
    "27": "R U R' U R U2 R'",
    "28": "R2 F2 L F L' F2 R F' R",
    "29": "R2 U' R F R' U R2 U' R' F' R",
    "30": "F' L U L2 U L2 U2 L' U F",
    "31": "R' U' F U R U' R' F' R",
    "32": "R U B' U' R' U R B R'",
    "33": "R U R' U' R' F R F'",
    "34": "R U R2 U' R' F R U R U' F'",
    "35": "R U2 R2 F R F' R U2 R'",
    "36": "R U R' U' F' U2 F U R U R'",
    "37": "R' F R F' U' F' U F",
    "38": "L U L' U L U' L' U' L' B L B'",
    "39": "L F' L' U' L U F U' L'",
    "40": "R' F R U R' U' F' U R",
    "41": "F U R U' R' F' R' U2 R U R' U R",
    "42": "R' U' R U' R' U2 R F R U R' U' F'",
    "43": "R' U' F' U F R",
    "44": "F U R U' R' F'",
    "45": "F R U R' U' F'",
    "46": "R' U' R' F R F' U R",
    "47": "F' L' U' L U L' U' L U F",
    "48": "F R U R' U' R U R' U' F'",
    "49": "R B' R2 F R2 B R2 F' R",
    "50": "R' F R2 B' R2 F' R2 B R'",
    "51": "F U R U' R' U R U' R' F'",
    "52": "R' U' R U' R' U F' U F R",
    "53": "R' F' L F' L' F L F' L' F2 R",
    "54": "F R' F' R U2 F2 L F L' F",
    "55": "R' U' F R' F' R F U R U' R' F' R",
    "56": "L F L' U R U' R' U R U' R' L F' L'",
    "57": "R U R' U' R' L F R F' L'"
}

# resource: my gigantic braiiiiin

CROSS = [
    "",
    "L",
    "L'",
    "L2",
    "F L",
    "B' L'",
    "U L2",
    "U' L2", 
    "U2 L2",
    "F' L F",
    "B L' B'",
    "F2 U L2",
    "B2 U' L2",
    "F2 L F2",
    "B2 L' B2",
    "R2 U2 L2",
    "U F' L F",
    "F' U F L2",
    "F U F' L2",
    "B' U' B L2",
    "B U' B' L2",
    "R F' U F L2",
    "L' F U F' L2",
    "L F U F' L2"
]

# Resource: My Gigantic Braiiiiiiiin

F2L = [ # Assuming corner is at U-L-B intersection
    "", # skip lol
# Working with Orange-Green pair
    # Yellow Up
        # Green edge side Up
    "U L' U' L2 F' L' F",
    "U2 L' U2 L U' L' U L",
    "U L' U' L U L' U L U L' U2 L",
    "U' L' U2 L U L' U' L",
        # Orange edge side Up
    "F U2 F2 L F L'",
    "U F U F2 L F L'",
    "U' F U2 F' U' F U F'",
    "F U' F' U' F U' F2 L F L'",
        # Edge in slot
    "F U' F' U F U' F2 L F L'",
    "L F' L' F L' U L",
    # Yellow Back
        # Green edge side Up
    "U' L' U' L",
    "L' U' L U' L' U' L",
    "U' L U2 L2 U' L2 U' L'",
    "L' U L U' L' U' L",
        # Orange edge side Up
    "U2 F U2 F' U' F U2 F'",
    "U2 F U F' U2 F U' F'",
    "F U' F'",
    "F' L F L' U F U F'",
        # Edge in slot
    "U F U F' L F' L' F",
    "L' U2 L U' L' U' L",
    # Yellow Left
        # Green edge side Up
    "L' U' L U2 L' U L",
    "L' U2 L U2 L' U L",
    "U' F U' F' U2 L' U' L",
    "U2 L' U L",
        # Orange edge side Up
    "L' U L U' F U F'",
    "U' F U' F'",
    "U2 F U' F' U F U F'",
    "L' U2 L U' F U F'",
        # Edge in slot
    "L' U' L U' F U F'",
    "L' U L U2 L' U L"
]

F2L_SETUP = [ # Assuming corner is in L-F slot
    "L' U L F U2 F'", # 0 - Edge in same slot
    "F' U' F2 U' F'", # 1 - counterclockwise (from top)
    "R' F U' F' R", # 2
    "L U L2 U L" # 3
]

CORNER_MAP = { # Input: str(face) + str(location_on_face). Output: number based on that diagram I have :)
    "00": 1,
    "02": 4,
    "06": 2,
    "08": 3,
    "10": 1,
    "12": 2,
    "20": 2,
    "22": 3,
    "30": 3,
    "32": 4,
    "40": 4,
    "42": 1,
    "16": 8,
    "18": 5,
    "26": 5,
    "28": 6,
    "36": 6,
    "38": 7,
    "46": 7,
    "48": 8,
    "50": 5,
    "52": 6,
    "56": 8,
    "58": 7
}
MOVES = ["U", "U2", "U'", "L", "L2", "L'", "F", "F2", "F'", "R", "R2", "R'", "B", "B2", "B'"]
MOVE_MAP = { # "rotates" your algorithm clockwise: L becomes F, etc
    "": "",
    "L": "F",
    "L'": "F'",
    "L2": "F2",
    "F": "R",
    "F'": "R'",
    "F2": "R2",
    "R": "B",
    "R'": "B'",
    "R2": "B2",
    "B": "L",
    "B'": "L'",
    "B2": "L2",
    "U": "U",
    "U'": "U'",
    "U2": "U2"
}

UAlgorithm = "R' L' F2 B2 R L D R' L' F2 B2 R L"
scrambleForSample = "B2 L2 D2 B2 D' F2 R2 U2 R2 D' U' B L U2 B U B2 F' R2 U2"
solutionToSample = "U2 R2 F B2 U' B' U2 L' B' U D R2 U2 R2 F2 D B2 D2 L2 B2"

if __name__ == "__main__":
    cube = Cube()
    cube.do_moves(scrambleForSample)

    print("About to solve the following cube:")
    cube.print_cube()
    print("---CALCULATING---\n")
    begin = time.time()
    
    instructions = cube.parse_instructions(cube.solve_cube())
    # print(str(instructions))
    cube.print_cube()

    #print(CROSS[22])
    #newthing = cube.orient_alg(CROSS[22], 0)
    #print(newthing)

    #crossSolution = cube.solve_Cross()
    #print("\nCross solution: " + str(crossSolution))
    #cube.print_cube()

    #cube.do_moves(solutionToSample)
    

    '''
    YAY = test1276(cube)

    if (YAY == True): print("\nHOLY MACKEREL!\n")
    else: print("\nrip i suck")
    '''
    
    end = time.time()
    print("\nTotal Time this took: " + str(end - begin) + "seconds")

