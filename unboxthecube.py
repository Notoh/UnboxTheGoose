from unboxtheface import Face

CLOCK_WISE = 0
COUNTER_CLOCKWISE = 1

U_F = 0 #up
L_F = 1 #left
F_F = 2 #front
R_F = 3 #right
B_F = 4 #bottom
D_F = 5 #down

class Cube:

    '''

    


    '''

    faces = []

    def __init__(self):
        self.faces = [Face(U_F, B_F, F_F, L_F, R_F), Face(L_F, U_F, R_F, B_F, F_F), Face(F_F, U_F, D_F, L_F, R_F), Face(R_F, U_F, D_F, F_F, B_F), Face(B_F, U_F, D_F, R_F, L_F), Face(D_F, F_F, B_F, L_F, R_F)]

    
    def rotate(self, index, direction):

        if direction == CLOCK_WISE:
            
            #rotate the face
            faces[index].rotate_clock_wise(direction);

            #rotate the adjacent small cube
            
            

        
    
        
    def clear(self):

        #clear all faces
        for face in self.faces:
            face.clear()




    '''DEBUG FUNCTIONS'''

    def check_integrity(self)-> bool:

    #cube must have 6 faces
        if len(self.faces) != 6:
            return False
        
     #check each face's integrity
        for face in faces:
            if not face.check_integrity():
                return False

        return True;

    def print_cube(self):

        for face in self.faces:
            print(face.curr)
            face.print_face();
            print('\n')
    
    
        


if __name__ == "__main__":
    print("test\n")

    cube = Cube()
    cube.print_cube()
