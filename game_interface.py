import pygame
from helper.draw_button import Button
from helper.draw_titles import Titles
from game_logic import Game

class Windows:
    def __init__(self, CAPTION):
        # Configuración básica de Pygame
        pygame.display.set_caption(CAPTION)
        self.__WIDTH = int(1280)
        self.__HEIGHT = int(720)
        self.surface = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__FPS = int(60)
        self.clock = pygame.time.Clock()
        self.__running = False

        # Importando JUEGO
        self.game = Game()
        #self.game.create_unicursal_maze(4, 2)
        self.maze_timeout = 0
        self.show_maze = False

        # Imagenes Pantalla Juego y Seleccion De Dificultad
        self.img_choose_difficulty = pygame.image.load("src/img_background/Difficulty/Static_img.png").convert_alpha()
        self.img_game = pygame.image.load("src/img_background/Game/Game_img.png").convert_alpha()
        self.img_option = pygame.image.load("src/img_background/Option/Option_img.png").convert_alpha()

        # Configuracion Extra Lobby
        self.__music_file = "src/music/audioOgg.ogg"

        # Animacion Lobby
        self.animation_steps = 30
        self.animation_list = []
        self.frame = 0
        self.current_time = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 180

        self.all_lobby_buttons = pygame.sprite.Group()
        self.all_difficulty_buttons = pygame.sprite.Group()
        self.all_options_buttons = pygame.sprite.Group()

        self.result_value = "Main_Menu"

        # Titulo Pantalla Inicio
        self.title_init = Titles(138, 19, "src/img_titles_background/init.png")

        # Botones Lobby
        img_options_button = "src/img_button/options_button.png"
        img_options_button_hover = "src/img_button/options_button_hover.png"
        options_button = Button(140, 375, img_options_button, img_options_button_hover, "OPTIONS")

        img_start_button = "src/img_button/start_button.png"
        img_start_button_hover = "src/img_button/start_button_hover.png"
        start_button = Button(490, 355, img_start_button, img_start_button_hover, "MENU_DIFFICULTY")

        img_exit_button = "src/img_button/exit_button.png"
        img_exit_button_hover = "src/img_button/exit_button_hover.png"
        exit_button = Button(900, 370, img_exit_button, img_exit_button_hover, "QUIT")

        self.all_lobby_buttons.add(options_button, start_button, exit_button)

        # Titulo Pantalla Dificultad
        self.title_difficulty = Titles(350, 22, "src/img_titles_background/difficulty.png")

        # Botones Seleccionar Dificultad
        img_easy_button = "src/img_button/easy_button.png"
        img_easy_button_hover = "src/img_button/easy_button_hover.png"
        easy_button = Button(140, 330, img_easy_button, img_easy_button_hover, "EASY")

        img_medium_button = "src/img_button/medium_button.png"
        img_medium_button_hover = "src/img_button/medium_button_hover.png"
        #medium_button = Button(490, 330, img_medium_button, img_medium_button_hover, "MEDIUM")

        img_hard_button = "src/img_button/hard_button.png"
        img_hard_button_hover = "src/img_button/hard_button_hover.png"
        hard_button = Button(900, 330, img_hard_button, img_hard_button_hover, "HARD")

        img_back_button = "src/img_button/back_button.png"
        img_back_button_hover = "src/img_button/back_button_hover.png"
        back_button = Button(20, 630, img_back_button, img_back_button_hover, "Main_Menu")

        self.all_difficulty_buttons.add(easy_button, hard_button, back_button)

        # Botones Opciones Inicio
        self.title_options = Titles(390, 30, "src/img_titles_background/option.png")

        self.all_options_buttons.add(back_button)

        # Botones Opciones
        #self.img_icon_settings = "src/img_button/icon_settings.png"
        #self.icon_settings = Button(1226, 8, self.img_icon_settings, self.img_icon_settings)

    def music_lobby(self):
        try:
            pygame.mixer.music.load(self.__music_file)
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(0.4)
        except pygame.error as e:
            print(f"Error loading music: {e}")

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

    def on_event(self, event):
        state_menu = None

        if self.result_value == "Main_Menu":
            state_menu = self.all_lobby_buttons
        elif self.result_value == "MENU_DIFFICULTY":
            state_menu = self.all_difficulty_buttons
        elif self.result_value == "OPTIONS":
            state_menu = self.all_options_buttons
        elif self.result_value == "EASY":
            self.game.event_to_change(event, self.show_maze)

        if state_menu:
            for event_btn in state_menu:
                new_state = event_btn.handle_events(event)

                if new_state is not None:
                    self.result_value = new_state
                
                if new_state == "EASY":
                    self.game.create_unicursal_maze(8, 2)
                    self.show_maze = True
                    self.maze_timeout = pygame.time.get_ticks() + 5000


        if event.type == pygame.QUIT or self.result_value == "QUIT":
            self.__running = False

    def main_loop(self):
        self.__running = True
        self.music_lobby()
        if self.result_value == "Main_Menu":
            self.get_frames_animation_lobby()

        while self.__running: 
            self.surface.fill("black")

            if self.result_value == "Main_Menu":

                self.move_animation()
                self.surface.blit(self.animation_list[self.frame], (0, 0))
                self.title_init.draw(self.surface)
                self.all_lobby_buttons.draw(self.surface)

            elif self.result_value == "MENU_DIFFICULTY":

                self.surface.blit(self.img_choose_difficulty, (0, 0))
                self.title_difficulty.draw(self.surface)
                self.all_difficulty_buttons.draw(self.surface)

            elif self.result_value == "OPTIONS":

                self.surface.blit(self.img_option, (0, 0))
                self.title_options.draw(self.surface)
                self.all_options_buttons.draw(self.surface)

            elif self.result_value == "EASY":

                self.surface.blit(self.img_game, (0,0))
                tiempo_actual = pygame.time.get_ticks()

                if self.show_maze:
                    if tiempo_actual < self.maze_timeout:
                        self.game.draw_maze(self.surface)
                    else:
                        self.show_maze = False
                else:
                    self.game.draw_maze_to_solve(self.surface)
                    

            for event in pygame.event.get():
                self.on_event(event)

            self.clock.tick(self.__FPS)
            pygame.display.flip()

def main():
    pygame.init()
    pygame.mixer.init() 
    windows = Windows("Maze:Light-Trace") #Size: 1280x720
    windows.main_loop()

main()