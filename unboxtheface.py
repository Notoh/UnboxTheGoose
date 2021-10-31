class Face:
    matrix = []

    def __init__(self):
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def __init__(self, new_matrix):
        self.matrix = new_matrix

    def clear(self):
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
