import random
import pygame

class Game:
    def __init__(self):
        self.maze = []
        self.maze_to_solve = []
        self.colliders = []

        self.screen_w = 1280
        self.screen_h = 720
        self.cell_size = 0 
        self.offset_x = 0
        self.offset_y = 0

        self.cols = 0
        self.rows = 0

        self.img_empty_path = pygame.image.load("src/game_panels/empty_panel.png").convert_alpha()
        self.img_wrong_path = pygame.image.load("src/game_panels/wrong_panel.png").convert_alpha()
        self.img_right_path = pygame.image.load("src/game_panels/right_panel.png").convert_alpha()

    def create_unicursal_maze(self, width, height, min_coverage=0.5):
        rows, cols = height * 2 + 1, width * 2 + 1
        total_cells = (width * height)

        self.rows, self.cols = rows, cols
        
        if cols > rows:
            area_util_h = 720 * 0.6 
            margen_superior = 720 * 0.4

            size_v = (area_util_h - self.rows) // self.rows
            size_h = (1280 * 0.8 - self.cols) // self.cols
            self.cell_size = int(min(size_v, size_h))

            maze_width_px = (self.cols * self.cell_size) + (self.cols - 1)
            maze_height_px = (self.rows * self.cell_size) + (self.rows - 1)

            self.offset_x = (1280 - maze_width_px) // 2

            espacio_sobrante_v = area_util_h - maze_height_px
            self.offset_y = margen_superior + (espacio_sobrante_v // 2)
        else:
            max_w = 1280 
            max_h = 720 

            size_v = (max_h - self.rows) // self.rows
            size_h = (max_w - self.cols) // self.cols

            self.cell_size = int(min(size_v, size_h))

            maze_width_px = (self.cols * self.cell_size) + (self.cols - 1)
            maze_height_px = (self.rows * self.cell_size) + (self.rows - 1)

            self.offset_x = (1280 - maze_width_px) // 2
            self.offset_y = (720 - maze_height_px) // 2
        
        self.maze_to_solve = [[1] * self.cols for _ in range(self.rows)]

        while True:
            self.maze = [[1] * cols for _ in range(rows)]
            
            start_x = random.randrange(1, cols - 1, 2)
            start_y = random.randrange(1, rows - 1, 2)
            #self.maze[start_y][start_x] = 2
            self.maze[start_y][start_x] = 0
            cells_visited = 1

            def remove_walls(cx, cy, count):
                nonlocal cells_visited
                direcciones = [(0, -2), (0, 2), (-2, 0), (2, 0)]
                random.shuffle(direcciones)

                for dx, dy in direcciones:
                    nx, ny = cx + dx, cy + dy

                    if 1 <= nx < cols - 1 and 1 <= ny < rows - 1:
                        if self.maze[ny][nx] == 1:
                            vecinos_vivos = 0
                            for ddx, ddy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                if self.maze[ny + ddy][nx + ddx] in [0, 2]:
                                    vecinos_vivos += 1
                            
                            if vecinos_vivos <= 1:
                                self.maze[cy + dy // 2][cx + dx // 2] = 0
                                self.maze[ny][nx] = 0
                                cells_visited += 1
                                
                                if remove_walls(nx, ny, count + 1):
                                    return True
                
                #self.maze[cy][cx] = 3
                return True

            remove_walls(start_x, start_y, 1)

            if cells_visited >= (total_cells * min_coverage):
                size = int(self.cell_size * 0.9)
                self.img_empty = pygame.transform.scale(self.img_empty_path, (size, size))
                self.img_wrong = pygame.transform.scale(self.img_wrong_path, (size, size))
                self.img_right = pygame.transform.scale(self.img_right_path, (size, size))

                self.colliders = []
                for r in range(self.rows):
                    fila_rects = []
                    for c in range(self.cols):
                        pos_x = self.offset_x + (c * self.cell_size)
                        pos_y = self.offset_y + (r * self.cell_size)
                        fila_rects.append(pygame.Rect(pos_x, pos_y, self.cell_size, self.cell_size))
                    self.colliders.append(fila_rects)

                return self.maze
            
                

    def draw_maze(self, screen):
        for r in range(self.rows):
            for c in range(self.cols):
                valor = self.maze[r][c]
                pos_x = self.offset_x + (c * self.cell_size)
                pos_y = self.offset_y + (r * self.cell_size)

                if valor == 1:
                    screen.blit(self.img_empty, (pos_x, pos_y))
                else:
                    screen.blit(self.img_right, (pos_x, pos_y))
    

    def draw_maze_to_solve(self, screen):
        for r in range(self.rows):
            for c in range(self.cols):
                valor = self.maze_to_solve[r][c]
                
                pos_x = self.offset_x + (c * self.cell_size)
                pos_y = self.offset_y + (r * self.cell_size)

                if valor == 2:
                    screen.blit(self.img_right, (pos_x, pos_y))
                elif valor == 3:
                    screen.blit(self.img_wrong, (pos_x, pos_y))
                else:
                    screen.blit(self.img_empty, (pos_x, pos_y))

    def event_to_change(self, event, click):
        if len(self.colliders) == 0: return
        if click: return

        pos_mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.colliders[r][c].collidepoint(pos_mouse):
                        if pygame.mouse.get_pressed()[0]:
                            if self.maze[r][c] == 0:
                                self.maze_to_solve[r][c] = 2
                            elif self.maze[r][c] == 1:
                                self.maze_to_solve[r][c] = 3

    def print_maze(self):
        symbols = {0: " ", 1: "#", 2: "S", 3: "E"}
        for row in self.maze:
            print("".join([symbols.get(c, "?") for c in row]))
