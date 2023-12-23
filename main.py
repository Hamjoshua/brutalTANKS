from constants import *
from game_objects import *

import pygame
import pygame_gui
from pytmx import load_pygame


class GuiManager:
    def __init__(self):
        pass


class GuiResponse:
    message: string
    code: int


class Camera:
    def __init__(self):
        pass


class GameMap:
    def __init__(self):
        pass


class GameManager:
    is_active: bool = True
    instances_group: pygame.sprite.Group
    static_objects_group: pygame.sprite.Group

    def __init__(self):
        pass

    def make_events(self):
        for event in self.events:
            event()

    def move_instance(self, vector: int, tank: Tank):
        # todo move_instance
        old_x: int = tank.x
        old_y: int = tank.y

    def move_player(self, player: Player):
        # todo получение вектора движения
        vector: int = 0
        self.move_instance(vector, player)

    def update_players(self):
        for player in self.players:
            self.move_player(player)


class LevelManager:
    def __init__(self):
        pass


def handle_inactive_game(game: GameManager, screen, gui_manager: GuiManager) -> GameManager:
    status = game.get_status()
    reply: GuiResponse
    if status == GameConditions.GameIsWon:
        reply = gui_manager.show_victory_screen(screen)
        if reply.code == GuiResponses.Ok:
            level: string = game.level
            return LevelManager.init_level(level)

    elif status == GameConditions.GameIsLoosed:
        reply = gui_manager.show_defeat_screen(screen)
        if reply.code == GuiResponses.Ok:
            level: string = game.level
            return LevelManager.init_level(level)

    elif status == GameConditions.GameIsPaused:
        reply = gui_manager.show_pause(screen)
        if reply.code == GuiResponses.Cancel:
            game.is_active = True
            return game

        # todo как сделать паузу и прочее гуи? будут ли они что-то возвращать?

    if reply == GuiResponses.Menu:
        level: string = gui_manager.show_menu()
        return LevelManager.init_level(level)
    elif reply.code == GuiResponses.LoadGame:
        saved_filename = reply.message
        return LevelManager.load_game(saved_filename)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    running: bool = True
    # level_loader: LevelManager = LevelManager() todo статичный класс
    gui_manager: GuiManager = GuiManager()
    game: GameManager
    level: string = gui_manager.show_menu()
    game = LevelManager.init_level(level)  # todo странно выглядит. стоит перестроить

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game.is_active_cutscene:
            # todo показ катсцен (возможно, через гуи)
            game.show_cutscenes()
        elif game.is_active:
            game.make_events()
            game.update_players()
            game.update_bots()
        else:
            handle_inactive_game(game, screen, gui_manager)

        game.render(screen)
        gui_manager.draw_hud(screen, game)  # todo у гуи тоже могут быть кастомные поля
        pygame.display.flip()
        clock.tick()
    pygame.quit()


if __name__ == '__main__':
    main()