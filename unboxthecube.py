from unboxthecubie import Cubie 

UP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
BACK = 4
DOWN = 5


class Cube:
    
    cubies = []

    def __init__(self):

        self.cubies = [[[0, 0, 0],[0, 0, 0],[0, 0, 0]], [[0, 0, 0],[0, 0, 0],[0, 0, 0]], [[0, 0, 0],[0, 0, 0],[0, 0, 0]]]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubies[i][j][k] = Cubie([[UP, UP],[LEFT, LEFT],[FRONT, FRONT],[RIGHT, RIGHT],[BACK, BACK],[DOWN, DOWN]])


    def R_X(self, layer):
        
        #swap four corners
        self.cubies[0][0][layer], self.cubies[0][2][layer] = self.cubies[0][2][layer], self.cubies[0][0][layer]
        self.cubies[0][0][layer], self.cubies[2][2][layer] = self.cubies[2][2][layer], self.cubies[0][0][layer]
        self.cubies[0][0][layer], self.cubies[2][0][layer] = self.cubies[2][0][layer], self.cubies[0][0][layer]

        #swap four edges
        self.cubies[0][1][layer], self.cubies[1][0][layer] = self.cubies[1][0][layer], self.cubies[0][1][layer]
        self.cubies[1][0][layer], self.cubies[2][1][layer] = self.cubies[2][1][layer], self.cubies[1][0][layer]
        self.cubies[2][1][layer], self.cubies[1][2][layer] = self.cubies[1][2][layer], self.cubies[2][1][layer]


        #update cubies color
        for i in range(3):
            for j in range(3):
                self.cubies[i][j][layer].R_X()


    def R_XI(self, layer):

        #swap four corners
        self.cubies[0][0][layer], self.cubies[2][0][layer] = self.cubies[2][0][layer], self.cubies[0][0][layer]
        self.cubies[0][0][layer], self.cubies[2][2][layer] = self.cubies[2][2][layer], self.cubies[0][0][layer]
        self.cubies[0][0][layer], self.cubies[0][2][layer] = self.cubies[0][2][layer], self.cubies[0][0][layer]

        #swap four edges
        self.cubies[2][1][layer], self.cubies[1][2][layer] = self.cubies[1][2][layer], self.cubies[2][1][layer]
        self.cubies[1][0][layer], self.cubies[2][1][layer] = self.cubies[2][1][layer], self.cubies[1][0][layer]
        self.cubies[0][1][layer], self.cubies[1][0][layer] = self.cubies[1][0][layer], self.cubies[0][1][layer]
        

        #update cubies color
        for i in range(3):
            for j in range(3):
                self.cubies[i][j][layer].R_XI()

    
    def R_Z(self, layer):
        
        #swap four corners
        self.cubies[0][layer][0], self.cubies[0][layer][2] = self.cubies[0][layer][2], self.cubies[0][layer][0]
        self.cubies[0][layer][0], self.cubies[2][layer][2] = self.cubies[2][layer][2], self.cubies[0][layer][0]
        self.cubies[0][layer][0], self.cubies[2][layer][0] = self.cubies[2][layer][0], self.cubies[0][layer][0]

        #swap four edges
        self.cubies[0][layer][1], self.cubies[1][layer][0] = self.cubies[1][layer][0], self.cubies[0][layer][1]
        self.cubies[1][layer][0], self.cubies[2][layer][1] = self.cubies[2][layer][1], self.cubies[1][layer][0]
        self.cubies[2][layer][1], self.cubies[1][layer][2] = self.cubies[1][layer][2], self.cubies[2][layer][1]


        #update cubies color
        for i in range(3):
            for j in range(3):
                self.cubies[i][j][layer].R_Z()


    def R_ZI(self, layer):

        #swap four corners
        self.cubies[0][layer][0], self.cubies[2][layer][0] = self.cubies[2][layer][0], self.cubies[0][layer][0]
        self.cubies[0][layer][0], self.cubies[2][layer][2] = self.cubies[2][layer][2], self.cubies[0][layer][0]
        self.cubies[0][layer][0], self.cubies[0][layer][2] = self.cubies[0][layer][2], self.cubies[0][layer][0]

        #swap four edges
        self.cubies[2][layer][1], self.cubies[1][layer][2] = self.cubies[1][layer][2], self.cubies[2][layer][1]
        self.cubies[1][layer][0], self.cubies[2][layer][1] = self.cubies[2][layer][1], self.cubies[1][layer][0]
        self.cubies[0][layer][1], self.cubies[1][layer][0] = self.cubies[1][layer][0], self.cubies[0][layer][1]
        

        #update cubies color
        for i in range(3):
            for j in range(3):
                self.cubies[i][j][layer].R_ZI()



    def print(self):
        
        for j in range(3):
            for k in range(3):
                print(self.cubies[0][j][k].get_color(BACK), end = '')
            print("")
        print("\n")

        
        for k in range(3):
            for i in range(3):
                print(self.cubies[i][0][k].get_color(LEFT), end = '')
            print("")
        print("\n")

        
        for i in range(3):
            for j in range(3):
                print(self.cubies[i][j][2].get_color(UP), end = '')
            print("")
        print("\n")

        
        for k in range(2, -1, -1):
            for i in range(3):
                print(self.cubies[i][0][k].get_color(RIGHT), end = '')
            print("")
        print("\n")

        
        for j in range(3):
            for k in range(2, -1, -1):
                print(self.cubies[0][j][k].get_color(FRONT), end = '')
            print("")
        print("\n")

        
        for i in range(2, -1, -1):
            for j in range(3):
                print(self.cubies[i][j][0].get_color(DOWN), end = '')
            print("")
        print("\n")

    

if __name__ == "__main__":
    
    print("test\n")
    cube = Cube()
    cube.print()

    #cube.R_X(2)
    #cube.print()

