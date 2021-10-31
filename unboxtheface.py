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
                
