import collections
import time
from functools import cache

UP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
BACK = 4
DOWN = 5

FACE_NUM = 6
STICKER_NUM = 8
STICKER_CENTER_EXTERNAL_INDEX = 4
STICKER_CENTER_INTERNAL_INDEX = 8
STICKER_BIT_SIZE = 4
STICKER_MASK = 15

FACE_COMPLETENESS_MASK = [0,286331153,572662306,858993459,1145324612,1431655765]

#cube adj edges, [face_index, s1, s2, s3]
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

        self.faces = [0, 0, 0, 0, 0, 0]

        for face_index in range(FACE_NUM):
            for i in range(STICKER_NUM):
                self.faces[face_index] |= face_index << (i * STICKER_BIT_SIZE)




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
            face_index = new_face[STICKER_EXTERNAL_INDEX]

            for sticker_index in range(STICKER_NUM + 1):
                if sticker_index != STICKER_EXTERNAL_INDEX:
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
                return False;
        return True


    '''
    args: face's index, clockwise rotating times
    return:

    Rotating the stickers in a face clockwise
    '''
    #@cache
    def rotate(self, face_index, times):

        assert(0 <= times <= 4)

        #rotate face
        left_shift_bits = 2 * times * STICKER_BIT_SIZE
        right_shift_bits = 32 - left_shift_bits;

        left_bits = (self.faces[face_index] << left_shift_bits) & ((1 << 32) - 1)
        right_bits = self.faces[face_index] >> right_shift_bits

        self.faces[face_index] = left_bits | right_bits


        print(bin(self.faces[face_index]))


        #rotate adjcent edges
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




if __name__ == "__main__":
    
    print("Test:")
    begin = time.time()
    
    cube = Cube()
    cube.print_cube()
    
    
    cube.rotate(RIGHT, 3)
    cube.print_cube()
    cube.rotate(LEFT, 3)
    cube.print_cube()
    cube.rotate(FRONT, 2)
    cube.print_cube()
    cube.rotate(BACK, 2)
    cube.print_cube()
    cube.rotate(RIGHT, 1)
    cube.print_cube()
    cube.rotate(LEFT, 1)
    cube.print_cube()
    cube.rotate(DOWN, 1)
    cube.print_cube()


    
    cube.rotate(RIGHT, 3)
    cube.print_cube()
    cube.rotate(LEFT, 3)
    cube.print_cube()
    cube.rotate(FRONT, 2)
    cube.print_cube()
    cube.rotate(BACK, 2)
    cube.print_cube()
    cube.rotate(RIGHT, 1)
    cube.print_cube()
    cube.rotate(LEFT, 1)
    cube.print_cube()

    cube.get_color(UP, 2)
    
    #UAlgorithm = "R' L' F2 B2 R L D R' L' F2 B2 R L"
    

    end = time.time()
    print(end - begin)
