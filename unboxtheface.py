class Face:
    matrix = []

    def __init__(self):
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def __init__(self, new_matrix):
        self.matrix = new_matrix

    def clear(self):
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def check_complete(self):
        first_colour = self.matrix[0][0]
        for i in range(3):
            for j in range(3):
                if (self.matrix[i][j] != first_colour):
                    return False
        return True

    def check_integrity(self):
        #check to see if the lenghts of ecah part of the list are correct
        if (self.matrix.length != 3) ||
            (self.matrix[0].length != 3) ||
            (self.matrix[1].length != 3) ||
            (self.matrix[2].length != 3):
                return False

        #check to make sure all values in the list are 0-5 or a color Name
        allowed_vals = [0,1,2,3,4,5,'R','G','B','O','W','Y','r','g','b','o','w','y']
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] not in allowed_vals:
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
            swap_var = self.matrix[row][0]
            self.matrix[row][0] = self.matrix[row][2]
            self.matrix[row][2] = swap_var

    #just rotates the 8 squares on this face. Not the neighbouring ones
    def rotate_face_ccw(self):
        self.matrix = self.transpose()
        self.swap_rows()

    #just rotates the 8 squares on this face. Not the neighbouring ones
    def rotate_face_cw(self):
        self.matrix = self.transpose()
        self.swap_cols()
        
