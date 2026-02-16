import pygame
from helper.draw_button import Button
from helper.handle_volume import Volume
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

        # Imagenes Pantalla Juego y Seleccion De Dificultad
        self.img_choose_difficulty = pygame.image.load("src/img_background/Difficulty/Static_img.png").convert_alpha()
        self.img_game = pygame.image.load("src/img_background/Game/Game_img.png").convert_alpha()
        self.img_option = pygame.image.load("src/img_background/Option/Option_img.png").convert_alpha()

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
        self.all_win_defeat_buttons = pygame.sprite.Group()
        self.all_username_buttons = pygame.sprite.Group()

        self.result_value = "Main_Menu"

        # Titulo Pantalla Inicio
        self.title_init = Titles(138, 19, "src/img_titles_background/init.png")

        # Botones Lobby
        options_button = Button(140, 375, "src/img_button/options_button.png", "src/img_button/options_button_hover.png", "OPTIONS")
        start_button = Button(490, 355, "src/img_button/start_button.png", "src/img_button/start_button_hover.png", "USERNAME")
        exit_button = Button(900, 370, "src/img_button/exit_button.png", "src/img_button/exit_button_hover.png", "QUIT")
        self.all_lobby_buttons.add(options_button, start_button, exit_button)

        # Titulo Pantalla Dificultad
        self.title_difficulty = Titles(350, 22, "src/img_titles_background/difficulty.png")

        # Botones Seleccionar Dificultad
        easy_button = Button(140, 330, "src/img_button/easy_button.png", "src/img_button/easy_button_hover.png", "EASY")
        medium_button = Button(490, 330, "src/img_button/medium_button.png", "src/img_button/medium_button_hover.png", "MEDIUM")
        hard_button = Button(900, 330, "src/img_button/hard_button.png", "src/img_button/hard_button_hover.png", "HARD")
        back_button = Button(20, 630, "src/img_button/back_button.png", "src/img_button/back_button_hover.png", "Main_Menu")
        self.all_difficulty_buttons.add(easy_button, medium_button, hard_button, back_button)

        # Botones Opciones Inicio
        self.title_options = Titles(390, 30, "src/img_titles_background/option.png")

        self.all_options_buttons.add(back_button)

        # Titulo Perdiste y Ganando
        self.title_losing = Titles(380, 22, "src/img_titles_background/losing.png")
        self.title_win = Titles(372, 16, "src/img_titles_background/winning.png")

        # Botones Pantalla Derrota
        try_again = Button(430, 450, "src/img_button/try_again.png", "src/img_button/try_again_hover.png", "RETRY")
        self.retry = ""
        back_button_defeat = Button(500, 550,  "src/img_button/back_button.png",  "src/img_button/back_button_hover.png", "MENU_DIFFICULTY")
        self.all_win_defeat_buttons.add(try_again, back_button_defeat)

        # Manejar volumen del juego
        self.handle_volume = Volume()

        # Manejar nomber usuario
        self.font = pygame.font.Font(None, 32)
        self.input_text = pygame.Rect(495, 320, 280, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_pasive = pygame.Color('gray')
        self.active_box_text = False

        # Botones del username
        self.play_button = Button(1000, 630, "src/img_button/play_button.png", "src/img_button/play_button_hover.png", "MENU_DIFFICULTY")

        self.all_username_buttons.add(back_button)

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
        if len(self.game.name) != 0:
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
                    self.game.name = self.game.name[:-1]
                else:
                    if len(self.game.name) < 20: self.game.name += event.unicode

    def on_event(self, event):
        state_menu = None

        if self.result_value == "Main_Menu":
            state_menu = self.all_lobby_buttons
        elif self.result_value == "USERNAME":
            state_menu = self.all_username_buttons
            self.get_username(event)
        elif self.result_value == "MENU_DIFFICULTY":
            state_menu = self.all_difficulty_buttons
        elif self.result_value == "OPTIONS":
            state_menu = self.all_options_buttons
            self.handle_volume.handle_events()
        elif self.result_value == "DEFEAT" or self.result_value == "VICTORY":
            state_menu = self.all_win_defeat_buttons
        elif self.result_value == "EASY" or self.result_value == "MEDIUM" or self.result_value == "HARD":
            self.game.event_to_change(event)

        if state_menu:
            for event_btn in state_menu:
                new_state = event_btn.handle_events(event)

                if new_state is not None:
                    self.result_value = new_state
                
                if new_state == "RETRY":
                    new_state = self.retry 
                    self.result_value = self.retry

                if new_state == "USERNAME":
                    self.game.name = ""

                if new_state == "EASY":
                    self.game.create_unicursal_maze(3, 2, 5)
                    self.game.reset(80000, 2, 5)
                    self.retry = "EASY"
                elif new_state == "MEDIUM":
                    self.game.create_unicursal_maze(4, 3, 4)
                    self.game.reset(59000, 3, 10)
                    self.retry = "MEDIUM"
                elif new_state == "HARD":
                    self.game.create_unicursal_maze(4, 3, 3)
                    self.game.reset(43000, 1, 8)
                    self.retry = "HARD"

        if event.type == pygame.QUIT or self.result_value == "QUIT":
            self.__running = False

    def main_loop(self):
        self.__running = True
        self.get_frames_animation_lobby()

        while self.__running: 
            self.surface.fill("black")

            if self.result_value == "Main_Menu":

                self.move_animation()
                self.surface.blit(self.animation_list[self.frame], (0, 0))
                self.title_init.draw(self.surface)
                self.all_lobby_buttons.draw(self.surface)
            
            elif self.result_value == "USERNAME":
                if self.active_box_text:
                    color = self.color_active
                else:
                    color = self.color_pasive

                self.surface.blit(self.img_option, (0, 0))

                text_choose_name = self.font.render("Type a username:", True, (255, 255, 255))
                self.surface.blit(text_choose_name, (540, 290))
                text_surface = self.font.render(self.game.name, True, (255, 255, 255))
                self.surface.blit(text_surface, (self.input_text.x + 5, self.input_text.y + 5))
                self.input_text.w = max(280, text_surface.get_width() + 10) # Make Box-text stretching

                pygame.draw.rect(self.surface, color, self.input_text, 2)
                self.all_username_buttons.draw(self.surface)
                
            elif self.result_value == "MENU_DIFFICULTY":

                self.surface.blit(self.img_choose_difficulty, (0, 0))
                self.title_difficulty.draw(self.surface)
                self.all_difficulty_buttons.draw(self.surface)

            elif self.result_value == "OPTIONS":

                self.surface.blit(self.img_option, (0, 0))
                self.title_options.draw(self.surface)
                self.handle_volume.draw(self.surface)
                self.all_options_buttons.draw(self.surface)

            elif self.result_value == "EASY" or self.result_value == "MEDIUM" or self.result_value == "HARD":

                self.surface.blit(self.img_game, (0,0))
                self.game.validate_victory()
                self.game.logic(self.surface, self.title_win, self.title_losing)

                if len(self.game.result) != 0:
                    self.result_value = self.game.result

            elif self.result_value == "DEFEAT":

                self.surface.blit(self.img_game, (0,0))
                self.title_losing.draw(self.surface)
                self.game.data_screen(self.surface)
                self.all_win_defeat_buttons.draw(self.surface)

            elif self.result_value == "VICTORY":

                self.surface.blit(self.img_game, (0,0))
                self.title_win.draw(self.surface)
                self.game.data_screen(self.surface)
                self.all_win_defeat_buttons.draw(self.surface)

            for event in pygame.event.get():
                self.on_event(event)

            self.clock.tick(self.__FPS)
            pygame.display.flip()

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    windows = Windows("Maze:Light-Trace") #Size: 1280x720
    windows.main_loop()

main()