class Face:
    matrix = []
    curr = 0
    top = 0
    down = 0
    left = 0
    right = 0

    def __init__(self, new_curr, new_top, new_down, new_left, new_right):
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.curr = new_curr
        self.top = new_top
        self.down = new_down
        self.left = new_left
        self.right = new_right

    def clear(self):
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def check_complete(self):
        first_colour = self.matrix[0][0]
        for i in range(3):
            for j in range(3):
                if (self.matrix[i][j] != first_colour):
                    return False
        return True

    def transpose(self):
        transposed_matrix = self.matrix.copy()
        
        for i in range(3):
            for j in range(3):
                transposed_matrix[i][j] = self.matrix[j][i]
        return transposed_matrix

    def swap_rows(self):
        for col in range(3):
            swap_var = self.matrix[0][col]
            self.matrix[0][col] = self.matrix[2][col]
            self.matrix[2][col] = swap_var

    def swap_cols(self):
        for row in range(3):
            self.matrix[row][0], self.matrix[row][2] = self.matrix[row][2], self.matrix[row][0]

    #just rotates the 8 squares on this face. Not the neighbouring ones
    def rotate_face_ccw(self):
        self.matrix = self.transpose()
        self.swap_rows()

    #just rotates the 8 squares on this face. Not the neighbouring ones
    def rotate_face_cw(self):
        self.matrix = self.transpose()
        self.swap_cols()


    #DEBUG
    def check_integrity(self) -> bool:
        #check to see if the lenghts of ecah part of the list are correct
        if len(self.matrix) != 3:
            return False

        for m in self.matrix:
            if len(m) != 3:
                return False

        #check to make sure all values in the list are 0-5 or a color Name
        allowed_vals = [0,1,2,3,4,5,'R','G','B','O','W','Y','r','g','b','o','w','y']
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] not in allowed_vals:
                    return False

        return True

    def print_face(self):

        for row in self.matrix:
            print(row)

        print()
        
