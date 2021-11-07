
UP = 0;
LEFT = 1;
FRONT = 2;
RIGHT = 3;
BACK = 4;
DOWN = 5;

FACE_NUM = 6
STICKER_NUM = 8
STICKER_BIT_SIZE = 4
STICKER_MASK = 15



#cube rotation index
[
    [],
    [],
    [],
    [],
    [],
    []
]


class Cube:

    #an array of 32 bits interger
    faces = []


    def __init__(self):

        self.faces = [0, 0, 0, 0, 0, 0]

        for face_index in range(FACE_NUM):
            
            for i in range(STICKER_NUM):
                self.faces[face_index] |= face_index << (i * STICKER_BIT_SIZE)




    '''
    args: face's index
    return: face's bits sequence
    '''
    def get_face(self, face_index : int) -> int:
        
        return self.faces[face_index]


    '''
    args: face's index, sticker's index
    return: sticker's color
    '''
    def get_color(self, face_index : int, sticker_index : int) -> int:
        
        return self.faces[face_index] >> (sticker_index * STICKER_BIT_SIZE) & STICKER_MASK

    '''
    args: face's index, new face's bits sequence
    return:
    '''
    def set_face(self, face_index : int, new_face : int):
        
        self.faces[face_index] = new_face

    
    '''
    args: face's index, sticker's index
    return: sticker's color
    '''
    def set_color(self, face_index : int, sticker_index : int, new_sticker_color : int):

        shift_bits = sticker_index * STICKER_BIT_SIZE
        self.faces[face_index] &= ~(STICKER_MASK << shift_bits)
        self.faces[face_index] |= new_sticker_color << shift_bits
        

    
    

    '''
    args: face'index, placeholder string
    return:

    Print all stickers' color on a face
    '''
    def print_face(self, face_index : int, placeholder : str):
        
        print(placeholder + str(self.get_color(face_index, 0)), end = '')

        print(self.get_color(face_index, 1), end = '')
        print(self.get_color(face_index, 2))
        
        print(placeholder + str(self.get_color(face_index, 7)), end = '')
        print(face_index, end = '')
        print(self.get_color(face_index, 3))
        
        print(placeholder + str(self.get_color(face_index, 6)), end = '')
        print(self.get_color(face_index, 5), end = '')
        print(self.get_color(face_index, 4))



    '''
    args:
    return:

    Print the entire cube
    '''
    def print_cube(self):
        
        self.print_face(4, "   ")
 
        for i in range(3):
            print(self.get_color(1, i), end = '')
        for i in range(3):
            print(self.get_color(0, i), end = '')
        for i in range(3):
            print(self.get_color(3, i), end = '')
        print("")
            
        print(self.get_color(1, 7), end = '')
        print(self.get_color(1, 1), end = '')
        print(self.get_color(1, 3), end = '')
        print(self.get_color(0, 7), end = '')
        print(self.get_color(0, 1), end = '')
        print(self.get_color(0, 3), end = '')
        print(self.get_color(3, 7), end = '')
        print(self.get_color(3, 1), end = '')
        print(self.get_color(3, 3))
            
        print(self.get_color(1, 6), end = '')
        print(self.get_color(1, 5), end = '')
        print(self.get_color(1, 4), end = '')
        print(self.get_color(0, 6), end = '')
        print(self.get_color(0, 5), end = '')
        print(self.get_color(0, 4), end = '')
        print(self.get_color(3, 6), end = '')
        print(self.get_color(3, 5), end = '')
        print(self.get_color(3, 4))
        
        self.print_face(2, "   ")
        self.print_face(5, "   ")




    '''
    args: face's index, clockwise rotating times
    return:

    Rotating the stickers in a face clockwise
    '''
    def rotate(self, face_index, times):

        assert(0 <= times <= 4)
        
        left_shift_bits = 2 * times * STICKER_BIT_SIZE
        right_shift_bits = 32 - left_shift_bits;

        left_bits = self.faces[face_index] << left_shift_bits & ((1 << 33) - 1)
        right_bits = self.faces[face_index] >> right_shift_bits

        self.faces[face_index] = left_bits | right_bits

        



        


    

if __name__ == "__main__":
    print("Test:")
    cube = Cube()

    
    for i in range(8):
        cube.set_color(0, i, i)

    
    cube.print_cube()


    
    cube.print_face(0, "")
    cube.rotate(0, 3)
    cube.print_face(0, "")
