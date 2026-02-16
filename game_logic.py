import random
import pygame

class Game:
    def __init__(self):
        self.maze = []
        self.maze_to_solve = []
        self.colliders = []

        self.easy_levels = [
            (), # 0 self.level start at 1
            (), # 1 self.level start at 1 but is calling out of the class Game at the on_event(event)
            (3, 2), # Start here
            (4, 2), (4, 2), (4, 3),
            (2, 2) # Avoid Errors
        ]

        self.medium_levels = [
            (), # 0 self.level start at 1
            (), # 1 self.level start at 1 but is calling out of the class Game at the on_event(event)
            (4, 3), # Start here
            (4, 3), (4, 3),
            (5, 3), (5, 3), (5, 3), (5, 3), (5, 4), (5, 4),
            (2, 2) #Avoid Errors
        ]

        self.hard_levels = [
            (),
            (),
            (4, 4), (5, 4), 
            (5, 4), (5, 5), (5, 5), 
            (6, 4), (6, 4),
            (2, 2) # Avoid Erros 
        ]

        self.screen_w = 1280
        self.screen_h = 720
        self.cell_size = 0 
        self.offset_x = 0
        self.offset_y = 0
        self.cell_visited = 0
        self.counter_cell_to_win = 0

        self.maze_timeout = 0
        self.timer_next_level = 0
        self.timer = 0
        self.actual_time = 0

        self.cols = 0
        self.rows = 0

        self.img_empty_path = pygame.image.load("src/game_panels/empty_panel.png").convert_alpha()
        self.img_wrong_path = pygame.image.load("src/game_panels/wrong_panel.png").convert_alpha()
        self.img_right_path = pygame.image.load("src/game_panels/right_panel.png").convert_alpha()

        self.defeat = False
        self.victory_level = False
        self.victory = False
        self.show_maze = False

        self.time_paused = 0
        self.timer_is_frozen = False

        self.puntuacion = 0
        self.level = 1
        self.life = 3
        self.time = 0
        self.max_level = 0
        self.name = ""
        self.result = ""

        self.font_timer = pygame.font.SysFont("Arial", 34, bold=True)

    def create_unicursal_maze(self, width, height, time, min_coverage=0.5):
        self.cell_visited = 0
        self.counter_cell_to_win = 0
        self.cols = 0
        self.rows = 0
        self.timer = 0
        self.timer_next_level = 0
        self.show_maze = True
        self.victory_level = False
        self.maze_timeout = pygame.time.get_ticks() + (time * 1000)

        rows, cols = height * 2 + 1, width * 2 + 1
        total_cells = (width * height)

        self.rows, self.cols = rows, cols
        
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
        
        self.maze_to_solve = [[1] * self.cols for _ in range(self.rows)]

        while True:
            self.maze = [[1] * cols for _ in range(rows)]
            
            start_x = random.randrange(1, cols - 1, 2)
            start_y = random.randrange(1, rows - 1, 2)
            self.maze[start_y][start_x] = 0
            cells_visited = 1

            def remove_walls(cx, cy):
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
                                cells_visited += 1
                                self.maze[ny][nx] = 0
                                cells_visited += 1
                                
                                if remove_walls(nx, ny):
                                    return True
                
                return True

            remove_walls(start_x, start_y)

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

                self.cell_visited = cells_visited

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

    def event_to_change(self, event):
        if self.defeat or self.victory_level or self.show_maze or len(self.colliders) == 0: return

        pos_mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.colliders[r][c].collidepoint(pos_mouse):
                        if pygame.mouse.get_pressed()[0]:

                            if self.maze[r][c] == 0 and self.maze_to_solve[r][c] == 1:
                                self.maze_to_solve[r][c] = 2
                                self.counter_cell_to_win += 1
                            
                            if self.maze[r][c] == 1:
                                self.maze_to_solve[r][c] = 3
                                self.life -= 1
            if self.life <= 0:
                self.timer = pygame.time.get_ticks() + 3000
                self.defeat = True
                                
    def validate_victory(self):
        if ((self.time - self.actual_time) // 1000) <= 0:
            self.defeat = True

        if self.level > self.max_level:
            self.puntuacion += ((self.time - self.actual_time) // 1000) * 2
            self.victory = True

        if self.counter_cell_to_win == self.cell_visited and not self.victory_level and not self.victory:
            self.victory_level = True
            self.puntuacion += ((self.time - self.actual_time) // 1000) * 2
            self.timer_next_level = self.actual_time + 4000  

            self.time_paused = (self.time - self.actual_time) // 1000
            self.timer_is_frozen = True

    def reset(self, time, life, max_level):
        self.time = pygame.time.get_ticks() + time
        self.life = life
        self.puntuacion = 0
        self.level = 1
        self.max_level = max_level
        self.victory = False
        self.defeat = False
        self.result = ""

    def data_screen(self, screen):
        if not self.timer_is_frozen:
            if self.level == 1:
                restante_ms = (self.time - self.actual_time) // 1000
            else:
                restante_ms = (self.time - self.actual_time + 3000) // 1000
        else:
            restante_ms = self.time_paused

        texto_reloj = self.font_timer.render(f"Time: {max(0, restante_ms)} seg", True, (255, 255, 255))
        texto_vida = self.font_timer.render(f"Life(s): {self.life}", True, (255, 255, 255))
        texto_score = self.font_timer.render(f"Score: {self.puntuacion}", True, (255, 255, 255))
        texto_name = self.font_timer.render(f"Name: {self.name}", True, (255, 255, 255))
        texto_level = self.font_timer.render(f"Level: {self.level}/{self.max_level}", True, (255, 255, 255))

        if self.victory:
            screen.blit(texto_vida, (540, 260))
            screen.blit(texto_score, (540, 300))
            screen.blit(texto_name, (540, 340))
        elif self.defeat:
            screen.blit(texto_vida, (540, 260))
            screen.blit(texto_score, (540, 300))
            screen.blit(texto_name, (540, 340))
            screen.blit(texto_level, (540, 380))
        else:
            screen.blit(texto_reloj, (20, 20))
            screen.blit(texto_vida, (20, 60))
            screen.blit(texto_score, (20, 100))
            screen.blit(texto_name, (20, 140))
            screen.blit(texto_level, (20, 180))

    def logic(self, screen, title_winning, title_losing):
        self.actual_time = pygame.time.get_ticks()

        if self.show_maze and not self.victory:
            if self.actual_time < self.maze_timeout:
                self.draw_maze(screen)
                        
                segundos_restantes = (self.maze_timeout - self.actual_time) // 1000
                texto_timer = self.font_timer.render(f"Memorize: {segundos_restantes + 1}", True, (255, 255, 255))
                screen.blit(texto_timer, (20, 20))
            else:
                self.time += 6000
                self.timer_is_frozen = False
                self.show_maze = False
        else:
            if not self.defeat:
                self.draw_maze_to_solve(screen)
                self.data_screen(screen)

                if self.victory:
                    self.result = "VICTORY"
                else:
                    if self.victory_level:
                        if self.actual_time < self.timer_next_level:
                            title_winning.draw(screen)

                            segundos_restantes = (self.timer_next_level - self.actual_time) // 1000
                            texto_timer = self.font_timer.render(f"Continue: {segundos_restantes + 1} seg", True, (255, 255, 255))
                            screen.blit(texto_timer, (20, 220))
                        else:
                            self.level += 1
                            if self.max_level == 5:
                                w, h = self.easy_levels[self.level]
                                self.create_unicursal_maze(w, h, 5)
                            elif self.max_level == 10:
                                self.time += 4000
                                w, h = self.medium_levels[self.level]
                                self.create_unicursal_maze(w, h, 4)
                            elif self.max_level == 8:
                                self.time += 9000
                                w, h = self.hard_levels[self.level]
                                self.create_unicursal_maze(w, h, 3)
            else:
                if self.actual_time < self.timer:
                    title_losing.draw(screen)
                    self.draw_maze_to_solve(screen)
                else:
                    self.result = "DEFEAT"
