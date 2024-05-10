import random
import pygame

class CaveGeneration_CA:

    def __init__(self, grid_size, seed):
        if not seed == None:
            random.seed(seed, 2)
        else:
            random.seed(version=2)
        
        self.grid_size = grid_size
        self.grid = None


    def generate(self):
        print("""
               
    This is a Cave Generator that uses
    Cellular Automata to randomly generate caves
    based on the user inputted parameters.
              
    The use of this is to allow the user to
    1. Understand about Cave generation and CAs
    2. Find the correct parameters for their own CAs

""")

        CELL_SIZE = int(input("\nWhat is the cell size (2 unit is 2 x 2 area units) > "))
        B_LIMIT = int(input("\nWhat is the birth limit > "))
        D_LIMIT = int(input("What is the death limit > "))
        P_CHANCE = int(input("What is the percent chance of an alive cell > "))
        INTIAL_INTERATIONS = int(input("\nHow many intial generations do you want > "))

        print("Generating Base Grid...\n")


        self._generate_grid(P_CHANCE, INTIAL_INTERATIONS, D_LIMIT, B_LIMIT)
        self._create_Display(self.grid, CELL_SIZE)


        print("Press enter to make a new iteration")
        print("Press q to quit the generator")

        while True:
            user_input = input("> ")

            if user_input == "":
                INTIAL_INTERATIONS = INTIAL_INTERATIONS + 1
                print(f"\nGeneration #: {INTIAL_INTERATIONS}\n")

                self._generate_step(D_LIMIT, B_LIMIT)
                self._create_Display(self.grid, CELL_SIZE)  

            elif user_input == "q":
                break


    def _generate_grid(self, p_chance, intial_gen, death_limit, birth_limit):
        self.grid = [[0 for y in range(self.grid_size[1])] for x in range(self.grid_size[0])]

        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                if random.randint(1, 100) <= p_chance:
                    self.grid[x][y] = 1
                else:
                    self.grid[x][y] = 0

        for i in range(intial_gen):
            self._generate_step(death_limit=death_limit, birth_limit=birth_limit)


    def _generate_step(self, death_limit, birth_limit):
        width = len(self.grid)
        height = len(self.grid[0])

        new_grid = [[0 for y in range(height)] for x in range(width)]

        for x in range(width):
            for y in range(height):
                total_neighboors = self._find_neighboor(self.grid, (x, y))

                if self.grid[x][y] == 1:
                    if total_neighboors > death_limit:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0
                else:
                    if total_neighboors < birth_limit:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0

        self.grid = new_grid


    def _find_neighboor(self, grid, grid_pos):
        neighboors = 0

        for i in range(grid_pos[0]-1, grid_pos[0]+1):
            for j in range(grid_pos[1]-1, grid_pos[1]+1):
                if grid[i][j] == 1 and not (i,j) == grid_pos:
                    neighboors +=1

        return neighboors


    # This function (_create_Display) only purpose is to paint the grid once the grid is done with generating
    # Credit: https://github.com/HunterSTL/ProceduralCaveSimulation/blob/main/CaveSimulation.py#L59
    #
    # This function was originally found on this repository, 
    # as I didn't know how to use PyGame to create windows and draw grids.
    def _create_Display(self, grid, cell_size):
        pygame.init()

        width = len(grid)
        height = len(grid[0])

        win_size = (width * 1, height * 1)
        window = pygame.display.set_mode(win_size)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for x in range(width):
                for y in range(height):

                    if grid[x][y] == 0:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                    
                    pygame.draw.rect(window, color, (x*cell_size, y*cell_size, cell_size, cell_size))
            
            pygame.display.flip()

        pygame.quit()