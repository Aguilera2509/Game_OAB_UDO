import random
import pygame
from helper.draw_titles import Titles
from helper.draw_button import Button
from helper.handle_volume import Volume

from enfocate import GameBase, GameMetadata, COLORS

class Game(GameBase):
    def __init__(self, metada: GameMetadata):
        super().__init__(metada)

        """
        LOGICA INTERFAZ
        """

        # Animacion Lobby
        self.animation_steps = 31
        self.animation_list = []
        self.frame = 0
        self.current_time = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 180

        self.all_lobby_buttons = pygame.sprite.Group()
        self.all_difficulty_buttons = pygame.sprite.Group()
        self.all_options_buttons = pygame.sprite.Group()
        self.all_win_defeat_buttons = pygame.sprite.Group()
        self.all_username_buttons = pygame.sprite.Group()

        self.result = "Main_Menu"
        self.retry = ""

        # Manejar nombre usuario
        self.active_box_text = False

        """
        LOGICA DEL JUEGO
        """

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


    """
        INTERFAZ
    """
    def get_frames_animation_lobby(self):
        for x in range(1, self.animation_steps):
            img_path = f"src/img_background/Init/1280x720/Animation_img_{x}.png"
            img = pygame.image.load(img_path).convert_alpha()
            self.animation_list.append(img)

    def move_animation(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

    def get_username(self, event):
        if len(self.name) != 0:
            self.all_username_buttons.add(self.play_button)
        else:
            self.all_username_buttons.remove(self.play_button)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_text.collidepoint(event.pos):
                self.active_box_text = True
            else:
                self.active_box_text = False
        
        if event.type == pygame.KEYDOWN:
            if self.active_box_text:
                if event.key == pygame.K_DELETE or event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: return
                
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    if len(self.name) < 20: self.name += event.unicode

    def on_event_menu(self, event):
        state_menu = None

        if self.result == "Main_Menu":
            state_menu = self.all_lobby_buttons
        elif self.result == "USERNAME":
            state_menu = self.all_username_buttons
            self.get_username(event)
        elif self.result == "MENU_DIFFICULTY":
            state_menu = self.all_difficulty_buttons
        elif self.result == "OPTIONS":
            state_menu = self.all_options_buttons
            self.handle_volume.handle_events()
        elif self.result == "DEFEAT" or self.result == "VICTORY":
            state_menu = self.all_win_defeat_buttons

        if state_menu:
            for event_btn in state_menu:
                new_state = event_btn.handle_events(event)

                if new_state is not None:
                    self.result = new_state
                
                if new_state == "RETRY":
                    new_state = self.retry 
                    self.result = self.retry

                if new_state == "USERNAME":
                    self.name = ""

                if new_state == "EASY":
                    self.reset(80, 2, 5)
                    self.start_new_level(3, 2, 5)
                    self.retry = "EASY"
                elif new_state == "MEDIUM":
                    self.reset(59, 3, 10)
                    self.start_new_level(4, 3, 4, 0.9)
                    self.retry = "MEDIUM"
                elif new_state == "HARD":
                    self.reset(43, 1, 8)
                    self.start_new_level(4, 3, 3, 0.8)
                    self.retry = "HARD"


    # ----------- CARGA DINAMINCA ---------
    def on_start(self):
        """Carga de recursos dinámicos. 
        Nota: self.surface ya está disponible aquí gracias a GameBase."""

        ### ----------- GAME

        self.img_empty = pygame.image.load("src/game_panels/empty_panel.png").convert_alpha()
        self.img_wrong = pygame.image.load("src/game_panels/wrong_panel.png").convert_alpha()
        self.img_right = pygame.image.load("src/game_panels/right_panel.png").convert_alpha()


        ### ------------ INTERFAZ

        # Imagenes Pantalla Juego y Seleccion De Dificultad
        self.img_choose_difficulty = pygame.image.load("src/img_background/Difficulty/Static_img.png").convert_alpha()
        self.img_game = pygame.image.load("src/img_background/Game/Game_img.png").convert_alpha()
        self.img_option = pygame.image.load("src/img_background/Option/Option_img.png").convert_alpha()

        # Botones Lobby
        options_button = Button(140, 375, "src/img_button/options_button.png", "src/img_button/options_button_hover.png", "OPTIONS")
        start_button = Button(490, 355, "src/img_button/start_button.png", "src/img_button/start_button_hover.png", "USERNAME")
        exit_button = Button(900, 370, "src/img_button/exit_button.png", "src/img_button/exit_button_hover.png", "QUIT")
        self.all_lobby_buttons.add(options_button, start_button, exit_button)

        # Botones Seleccionar Dificultad
        easy_button = Button(140, 330, "src/img_button/easy_button.png", "src/img_button/easy_button_hover.png", "EASY")
        medium_button = Button(490, 330, "src/img_button/medium_button.png", "src/img_button/medium_button_hover.png", "MEDIUM")
        hard_button = Button(900, 330, "src/img_button/hard_button.png", "src/img_button/hard_button_hover.png", "HARD")
        back_button = Button(20, 630, "src/img_button/back_button.png", "src/img_button/back_button_hover.png", "Main_Menu")
        self.all_difficulty_buttons.add(easy_button, medium_button, hard_button, back_button)

        # Botones Opciones Inicio
        self.all_options_buttons.add(back_button)

        # Botones Pantalla Derrota
        try_again = Button(430, 450, "src/img_button/try_again.png", "src/img_button/try_again_hover.png", "RETRY")
        back_button_defeat = Button(500, 550,  "src/img_button/back_button.png",  "src/img_button/back_button_hover.png", "MENU_DIFFICULTY")
        self.all_win_defeat_buttons.add(try_again, back_button_defeat)

        # Manejar volumen del juego
        self.handle_volume = Volume()

        # Botones del username
        self.play_button = Button(1000, 630, "src/img_button/play_button.png", "src/img_button/play_button_hover.png", "MENU_DIFFICULTY")
        self.all_username_buttons.add(back_button)

        # Manejar nombre usuario
        self.font = pygame.font.Font(None, 32)
        self.input_text = pygame.Rect(495, 320, 280, 42)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_pasive = pygame.Color('gray')

        # Titulo Pantalla Inicio
        self.title_init = Titles(138, 19, "src/img_titles_background/init.png")

        # Titulo Pantalla Dificultad
        self.title_difficulty = Titles(350, 22, "src/img_titles_background/difficulty.png")

        # Titulo Pantalla Opciones
        self.title_options = Titles(390, 30, "src/img_titles_background/option.png")

        # Derrota y Victoria
        self.title_losing = Titles(380, 22, "src/img_titles_background/losing.png")
        self.title_win = Titles(372, 16, "src/img_titles_background/winning.png")
        
        # Fuente usando COLORS de la librería
        self.font = pygame.font.SysFont("Arial", 30, bold=True)

        # Animacion inicio
        self.get_frames_animation_lobby()


    """
        GAME
    """
    def start_new_level(self, width, height, time, min_coverage = 0.6) -> list[int]:
        """Lógica para generar el laberinto"""
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
                self.img_empty = pygame.transform.scale(self.img_empty, (size, size))
                self.img_wrong = pygame.transform.scale(self.img_wrong, (size, size))
                self.img_right = pygame.transform.scale(self.img_right, (size, size))

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
            
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pos_mouse = pygame.mouse.get_pos()

        for event in events:
            self.on_event_menu(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for r in range(self.rows):
                    for c in range(self.cols):
                        if self.colliders[r][c].collidepoint(pos_mouse):
                            if pygame.mouse.get_pressed()[0]:
                                if self.defeat or self.victory_level or self.show_maze or len(self.colliders) == 0: return

                                if self.maze[r][c] == 0 and self.maze_to_solve[r][c] == 1:
                                    self.maze_to_solve[r][c] = 2
                                    self.counter_cell_to_win += 1
                                
                                if self.maze[r][c] == 1:
                                    self.maze_to_solve[r][c] = 3
                                    self.life -= 1
        
                                if self.life <= 0:
                                    self.timer = pygame.time.get_ticks() + 3000
                                    self.defeat = True

    def draw_text(self, text, pos) -> None:
        img = self.font.render(text, True, COLORS["texto_principal"])
        self.surface.blit(img, pos)

    def render_maze_full(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                valor = self.maze[r][c]
                # Calculamos posición basada en los offsets y el tamaño de celda
                pos_x = self.offset_x + (c * self.cell_size)
                pos_y = self.offset_y + (r * self.cell_size)

                # Usamos self.surface (inyectada por GameBase) en lugar de 'screen'
                if valor == 1:
                    self.surface.blit(self.img_empty, (pos_x, pos_y))
                else:
                    self.surface.blit(self.img_right, (pos_x, pos_y))

    def render_maze_hidden(self) -> None:
        """Dibuja el progreso del jugador mientras resuelve el laberinto."""
        for r in range(self.rows):
            for c in range(self.cols):
                valor = self.maze_to_solve[r][c]
                pos_x = self.offset_x + (c * self.cell_size)
                pos_y = self.offset_y + (r * self.cell_size)

                # 2 = Camino correcto marcado, 3 = Error, otros = Vacío
                if valor == 2:
                    self.surface.blit(self.img_right, (pos_x, pos_y))
                elif valor == 3:
                    self.surface.blit(self.img_wrong, (pos_x, pos_y))
                else:
                    self.surface.blit(self.img_empty, (pos_x, pos_y))

    def going_next_level(self) -> None:
        """Maneja la transición de niveles y dificultad"""
        self.level += 1

        if self.level > self.max_level:
            self.victory = True
            self.timer_next_level = 0
            return
        
        self.victory_level = False
        self.timer_is_frozen = False

        # Configuración según dificultad
        if self.max_level == 5:
            w, h = self.easy_levels[self.level]
            self.start_new_level(w, h, 5)
        elif self.max_level == 10:
            w, h = self.medium_levels[self.level]
            self.start_new_level(w, h, 4, 0.9)
        elif self.max_level == 8:
            w, h = self.hard_levels[self.level]
            self.start_new_level(w, h, 3, 0.8)

    def update(self, dt: float):
        self.actual_time = pygame.time.get_ticks()

        if self.result == "Main_Menu":
            self.move_animation()
        elif self.result in ["EASY", "MEDIUM", "HARD"]:
            if self.show_maze:

                if self.actual_time >= self.maze_timeout:
                    if self.result == "EASY":
                        self.time += 6000 if self.level == 1 else 9000
                    elif self.result == "MEDIUM":
                        self.time += 6000 if self.level == 1 else 13000
                    else:
                        self.time += 6000 if self.level == 1 else 16000
                    self.timer_is_frozen = False
                    self.show_maze = False

                return 

            if not self.defeat:
                # Validar si el tiempo se agotó (Sustituye validate_victory)
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

                # Lógica de Paso de Nivel
                if self.victory_level:
                    if self.actual_time >= self.timer_next_level:
                        self.going_next_level()
                
                # Lógica de Victoria Total
                if self.victory:
                    self.result = "VICTORY"
            
            else:
                if self.actual_time >= self.timer:
                    self.result = "DEFEAT"

    def render_stats(self) -> None:
        """Dibuja la interfaz de usuario (HUD) y pantallas finales."""
        # 1. Cálculo del tiempo (Lógica original)
        if not self.timer_is_frozen:
            restante_ms = (self.time - self.actual_time) // 1000
        else:
            restante_ms = self.time_paused

        # 2. Preparación de textos (usando COLORS de la librería para consistencia)
        color_texto = COLORS["texto_principal"]
        
        # Diccionario de etiquetas para evitar repetición
        labels = {
            "time": f"Tiempo: {max(0, restante_ms)} seg",
            "live":  f"Vida(s): {self.life}",
            "score": f"Puntuacion: {self.puntuacion}",
            "name":  f"Nombre: {self.name}",
            "level": f"Level: {self.level}/{self.max_level}"
        }

        # 3. Renderizado según el estado del juego
        if self.victory or self.defeat:
            if self.actual_time >= self.timer and self.defeat:
                inicio_y = 260
                # Solo mostramos nivel si es derrota
                keys_a_mostrar = ["live", "score", "name"]
                if self.defeat: keys_a_mostrar.append("level")
                
                for key in keys_a_mostrar:
                    txt_img = self.font.render(labels[key], True, color_texto)
                    self.surface.blit(txt_img, (540, inicio_y))
                    inicio_y += 40
            
            if self.active_box_text >= self.timer_next_level and self.victory:
                inicio_y = 260
                # Solo mostramos nivel si es derrota
                keys_a_mostrar = ["live", "score", "name"]
                if self.defeat: keys_a_mostrar.append("level")
                
                for key in keys_a_mostrar:
                    txt_img = self.font.render(labels[key], True, color_texto)
                    self.surface.blit(txt_img, (540, inicio_y))
                    inicio_y += 40
        else:
            # Pantalla de Juego (HUD Lateral)
            inicio_y = 20
            keys_hud = ["time", "live", "score", "name", "level"]
            
            for key in keys_hud:
                txt_img = self.font.render(labels[key], True, color_texto)
                self.surface.blit(txt_img, (20, inicio_y))
                inicio_y += 40

    def draw(self):
        """Renderizado en la superficie inyectada por el motor."""
        # 1. Limpiar pantalla con colores oficiales
        self.surface.fill(COLORS["carbon_oscuro"])

        if self.result == "Main_Menu":
            self.surface.blit(self.animation_list[self.frame], (0, 0))
            self.title_init.draw(self.surface)
            self.all_lobby_buttons.draw(self.surface)
            
        elif self.result == "USERNAME":
            if self.active_box_text:
                color = self.color_active
            else:
                color = self.color_pasive

            self.surface.blit(self.img_option, (0, 0))

            text_choose_name = self.font.render("Type a username:", True, (255, 255, 255))
            self.surface.blit(text_choose_name, (530, 280))
            text_surface = self.font.render(self.name, True, (255, 255, 255))
            self.surface.blit(text_surface, (self.input_text.x + 5, self.input_text.y))
            self.input_text.w = max(280, text_surface.get_width() + 10) # Make Box-text stretching

            pygame.draw.rect(self.surface, color, self.input_text, 2)
            self.all_username_buttons.draw(self.surface)
                
        elif self.result == "MENU_DIFFICULTY":
            self.surface.blit(self.img_choose_difficulty, (0, 0))
            self.title_difficulty.draw(self.surface)
            self.all_difficulty_buttons.draw(self.surface)

        elif self.result == "OPTIONS":
            self.surface.blit(self.img_option, (0, 0))
            self.title_options.draw(self.surface)
            self.handle_volume.draw(self.surface)
            self.all_options_buttons.draw(self.surface)

        elif self.result == "EASY" or self.result == "MEDIUM" or self.result== "HARD":
            self.surface.blit(self.img_game, (0,0))

            if self.show_maze:
                self.render_maze_full()
                segundos = max(0, (self.maze_timeout - self.actual_time) // 1000)
                self.draw_text(f"Memorize: {segundos + 1}", (20, 20))
            else:
                self.render_maze_hidden()
                self.render_stats()
                if self.victory_level:
                    self.title_win.draw(self.surface)
                    segundos = max(0, (self.timer_next_level - self.actual_time) // 1000)
                    self.draw_text(f"Continuando: {segundos + 1} seg", (20, 220))
                if self.defeat:
                    self.title_losing.draw(self.surface)

        elif self.result == "DEFEAT":
            self.surface.blit(self.img_game, (0,0))
            self.render_stats()
            self.title_losing.draw(self.surface)
            self.all_win_defeat_buttons.draw(self.surface)

        elif self.result == "VICTORY":
            self.surface.blit(self.img_game, (0,0))
            self.render_stats()
            self.title_win.draw(self.surface)
            self.all_win_defeat_buttons.draw(self.surface)

    def reset(self, time_ms: int, lives: int, max_level: int) -> None:
        """Reinicia el estado del juego para una nueva partida."""
        # 1. Tiempos
        self.time = time_ms * 1000 + pygame.time.get_ticks()
        
        # 2. Atributos estándar de GameBase
        self.life = lives        
        self.puntuacion = 0            
        
        # 3. Metadatos y Niveles
        self.level = 1   
        self.max_level = max_level
        
        # 4. Estados de flujo
        self.victory = False
        self.defeat = False
        