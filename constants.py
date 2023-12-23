import enum
import pygame

class GameConditions(enum.IntEnum):
    GameIsLoosed = enum.auto()
    GameIsWon = enum.auto()
    GameIsPaused = enum.auto()


class GuiResponses(enum.IntEnum):
    Ok = enum.auto()
    Cancel = enum.auto()
    Menu = enum.auto()
    Settings = enum.auto()
    LoadGame = enum.auto()
    SaveGame = enum.auto()

# Управление todo может не понадобиться

FORWARD = 91
BACK = 92
TURN_RIGHT = 93
TURN_LEFT = 94
TURN_RIGHT_TURRET = 95
TURN_LEFT_TURRET = 96
SHOOT = 97
CONTROL_KEYS_V1 = {FORWARD: pygame.K_w, BACK: pygame.K_s,
                   TURN_RIGHT: pygame.K_d, TURN_LEFT: pygame.K_a,
                   TURN_RIGHT_TURRET: pygame.K_e, TURN_LEFT_TURRET: pygame.K_q,
                   SHOOT: pygame.K_r}
CONTROL_KEYS_V2 = {FORWARD: pygame.K_g, BACK: pygame.K_b,
                   TURN_RIGHT: pygame.K_n, TURN_LEFT: pygame.K_v,
                   TURN_RIGHT_TURRET: pygame.K_h, TURN_LEFT_TURRET: pygame.K_f,
                   SHOOT: pygame.K_c}
CONTROL_KEYS_V3 = {FORWARD: pygame.K_i, BACK: pygame.K_k,
                   TURN_RIGHT: pygame.K_l, TURN_LEFT: pygame.K_j,
                   TURN_RIGHT_TURRET: pygame.K_o, TURN_LEFT_TURRET: pygame.K_u,
                   SHOOT: pygame.K_p}
CONTROL_KEYS_V4 = {FORWARD: pygame.K_KP8, BACK: pygame.K_KP2,
                   TURN_RIGHT: pygame.K_KP6, TURN_LEFT: pygame.K_KP4,
                   TURN_RIGHT_TURRET: pygame.K_KP9, TURN_LEFT_TURRET: pygame.K_KP7,
                   SHOOT: pygame.K_KP_PLUS}

# Типы снарядов todo может появиться отдельный класс для снарядов


TANK_BULLET = 10
URAN_BULET = 11
ENERGY_BULLET = 12
TNT_BULLET = 13

TILE_SIZE = 40
TITLE = 'brutalTANKS'
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
FPS = 30


