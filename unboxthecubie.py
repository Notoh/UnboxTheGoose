

COLOR_BIT_SIZE = 3 #3 bits for each color (0 - 5)
COLOR_MASK = 7 #0b111


#face id == color id
UP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
BACK = 4
DOWN = 5


class Cubie:
    
    color = 0


    def __init__(self, color_lst):
        
        for pair in color_lst:
            self.set_color(pair[0], pair[1])


    def get_color(self, face):
        return self.color >> (face * COLOR_BIT_SIZE) & COLOR_MASK

    def set_color(self, face, new_color):

        #remove the old color
        self.color &= ~(COLOR_MASK << (face * COLOR_BIT_SIZE))

        #apply the new color
        self.color |= new_color << (face * COLOR_BIT_SIZE)
        

    def R_X(self):

        temp = self.get_color(LEFT)
        self.set_color(LEFT, self.get_color(FRONT))
        self.set_color(FRONT, self.get_color(RIGHT))
        self.set_color(RIGHT, self.get_color(BACK))
        self.set_color(BACK, temp)


    def R_XI(self):
        
        temp = self.get_color(LEFT)
        self.set_color(LEFT, self.get_color(BACK))
        self.set_color(BACK, self.get_color(RIGHT))
        self.set_color(RIGHT, self.get_color(FRONT))
        self.set_color(FRONT, temp)


    def R_Y(self):

        temp = self.get_color(UP)
        self.set_color(UP, self.get_color(FRONT))
        self.set_color(FRONT, self.get_color(DOWN))
        self.set_color(DOWN, self.get_color(BACK))
        self.set_color(BACK, temp)


    def R_YI(self):

        temp = self.get_color(UP)
        self.set_color(UP, self.get_color(BACK))
        self.set_color(BACK, self.get_color(DOWN))
        self.set_color(DOWN, self.get_color(FRONT))
        self.set_color(FRONT, temp)


    def R_Z(self):

        temp = self.get_color(UP)
        self.set_color(UP, self.get_color(LEFT))
        self.set_color(LEFT, self.get_color(DOWN))
        self.set_color(DOWN, self.get_color(RIGHT))
        self.set_color(RIGHT, temp)


    def R_ZI(self):

        temp = self.get_color(UP)
        self.set_color(UP, self.get_color(RIGHT))
        self.set_color(RIGHT, self.get_color(DOWN))
        self.set_color(DOWN, self.get_color(LEFT))
        self.set_color(LEFT, temp)


    def print(self):

        print(" {}\n{}{}{}\n {}\n {}\n".format(self.get_color(BACK), self.get_color(LEFT), self.get_color(UP), self.get_color(RIGHT), self.get_color(FRONT), self.get_color(DOWN)))



if __name__ == "__main__":
    
    print("test\n")
    cubie = Cubie([[BACK, 0], [LEFT, 1], [UP, 2], [RIGHT, 3], [FRONT, 4], [DOWN, 5]])
    cubie.print()

    cubie.R_X()
    cubie.print()
    cubie.R_XI()
    cubie.print()
    
    cubie.R_Y()
    cubie.print()
    cubie.R_YI()
    cubie.print()
    
    cubie.R_Z()
    cubie.print()
    cubie.R_ZI()
    cubie.print()

    
        
