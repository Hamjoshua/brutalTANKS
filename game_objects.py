from constants import *
import pygame
import os
import sys
from math import cos, sin

# todo у этой библиотеки слишком много зависимостей. нехорошо
MOVE_STEP = 1

def load_image(name, colorkey=None):
    fullname = os.path.join('data/sprites', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    if colorkey == 0:
        image = pygame.image.load(fullname)
    else:
        image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

# Корпуса и башни игроков
green_tank_turret = pygame.transform.scale(load_image(
    "green_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
green_tank_hull = pygame.transform.scale(load_image(
    "green_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
red_tank_turret = pygame.transform.scale(load_image(
    "red_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
red_tank_hull = pygame.transform.scale(load_image(
    "red_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
blue_tank_turret = pygame.transform.scale(load_image(
    "blue_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
blue_tank_hull = pygame.transform.scale(load_image(
    "blue_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
violet_tank_turret = pygame.transform.scale(load_image(
    "violet_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
violet_tank_hull = pygame.transform.scale(load_image(
    "violet_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))

# Корпуса и башни ботов
salad_tank_turret = pygame.transform.scale(load_image(
    "salad_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
salad_tank_hull = pygame.transform.scale(load_image(
    "salad_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
normal_tank_turret = pygame.transform.scale(load_image(
    "normal_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
normal_tank_hull = pygame.transform.scale(load_image(
    "normal_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
beast_tank_hull = pygame.transform.scale(load_image(
    "beast_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
beast_tank_turret = pygame.transform.scale(load_image(
    "beast_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
heavy_tank_hull = pygame.transform.scale(load_image(
    "heavy_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
heavy_tank_turret = pygame.transform.scale(load_image(
    "heavy_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
crash_tank = pygame.transform.scale(load_image(
    "crached_turret.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
convoy_hull = pygame.transform.scale(load_image(
    "convoy_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
convoy_turret = pygame.transform.scale(load_image(
    "convoy_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
convoy_crash = pygame.transform.scale(load_image(
    "convoy_crash.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
bullet_0 = pygame.transform.scale(load_image(
    "bullet_0.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
bullet_hero = pygame.transform.scale(load_image(
    "bullet_hero.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
bullet_heavy = pygame.transform.scale(load_image(
    "bullet_heavy.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
bullet_beast = pygame.transform.scale(load_image(
    "bullet_beast.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
bullet_tnt = pygame.transform.scale(load_image(
    "bullet_tnt.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
boss_hull = pygame.transform.scale(load_image(
    "boss.png", colorkey=-1), (640, 240))

# Локальный режим: клавиши
all_green_controls = load_image("all_green_controls.png", colorkey=0)
all_blue_controls = load_image("all_blue_controls.png", colorkey=0)
all_red_controls = load_image("all_red_controls.png", colorkey=0)
all_violet_controls = load_image("all_violet_controls.png", colorkey=0)
shoot_green_control = load_image("shoot_green_control.png", colorkey=0)
shoot_blue_control = load_image("shoot_blue_control.png", colorkey=0)
shoot_red_control = load_image("shoot_red_control.png", colorkey=0)
shoot_violet_control = load_image("shoot_violet_control.png", colorkey=0)

# Эффекты
lava = pygame.transform.scale(load_image(
    "lava.jpg", colorkey=0), (TILE_SIZE, TILE_SIZE))
explosion = pygame.transform.scale(load_image(
    "explosion.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
flash = pygame.transform.scale(load_image(
    "unbreak.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
smoke = pygame.transform.scale(load_image(
    "smoke.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
target_search = pygame.transform.scale(load_image(
    "target_search.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
target_confirmed = pygame.transform.scale(load_image(
    "target_confirmed.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))

# Интерфейс - очки здоровья
health = pygame.transform.scale(load_image(
    "health.png", colorkey=0), (25, 25))
losted_health = pygame.transform.scale(load_image(
    "losted_health.png", colorkey=0), (25, 25))
extra_health = pygame.transform.scale(load_image(
    "extra_health.png", colorkey=0), (25, 25))

# Объекты карты
map_life = pygame.transform.scale(load_image(
    "map_life.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
map_uran = pygame.transform.scale(load_image(
    "map_uran.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
map_energy = pygame.transform.scale(load_image(
    "map_energy.png", colorkey=0), (TILE_SIZE, TILE_SIZE))
map_boost = pygame.transform.scale(load_image(
    "map_boost.png", colorkey=0), (TILE_SIZE, TILE_SIZE))

# Инициализация персонажей для катсцен
unknown = pygame.transform.scale(load_image(
    "unknown.png", colorkey=0), (100, 100))
comander = pygame.transform.scale(load_image(
    "comander.png", colorkey=0), (100, 100))
soldier = pygame.transform.scale(load_image(
    "allied.png", colorkey=0), (100, 100))
radar = pygame.transform.scale(load_image(
    "convoy.png", colorkey=0), (100, 100))
serzant = pygame.transform.scale(load_image(
    "serzant.png", colorkey=0), (100, 100))
CHARACTERS_DICT = {None: unknown,
                   'Командир Брэдли': comander,
                   'Солдат': soldier,
                   'Связист Игорь': radar,
                   'Сержант': serzant}

normal_bullet_dict = {0: bullet_0, 'damage_type': TANK_BULLET}
hero_bullet_dict = {0: bullet_hero, 'damage_type': TANK_BULLET}
heavy_bullet_dict = {0: bullet_heavy, 'damage_type': URAN_BULET}
beast_bullet_dict = {0: bullet_beast, 'damage_type': ENERGY_BULLET}
tnt_bullet_dict = {0: bullet_tnt, 'damage_type': TNT_BULLET}

CONTROLLED_PLAYERS_DICT = {CONTROL_KEYS_V1[SHOOT]: {'name': 'Green',
                                                    'all_sprite': all_green_controls,
                                                    'shoot_sprite': shoot_green_control,
                                                    'sprite_coord': lambda x: (0, 0),
                                                    'control_set': CONTROL_KEYS_V1},
                           CONTROL_KEYS_V2[SHOOT]: {'name': 'Red',
                                                    'all_sprite': all_red_controls,
                                                    'shoot_sprite': shoot_red_control,
                                                    'sprite_coord': lambda x: (
                                                        WINDOW_WIDTH - x.get_width(), 0),
                                                    'control_set': CONTROL_KEYS_V2},
                           CONTROL_KEYS_V3[SHOOT]: {'name': 'Blue',
                                                    'all_sprite': all_blue_controls,
                                                    'shoot_sprite': shoot_blue_control,
                                                    'sprite_coord': lambda x: (
                                                        WINDOW_WIDTH - x.get_width(),
                                                        WINDOW_HEIGHT - x.get_height()),
                                                    'control_set': CONTROL_KEYS_V3},
                           CONTROL_KEYS_V4[SHOOT]: {'name': 'Violet',
                                                    'all_sprite': all_violet_controls,
                                                    'shoot_sprite': shoot_violet_control,
                                                    'sprite_coord': lambda x: (
                                                        0, WINDOW_HEIGHT - x.get_height()),
                                                    'control_set': CONTROL_KEYS_V4}}

# [(green_tank_hull, green_tank_turret),
#                                     (red_tank_hull, red_tank_turret),
#                                     (blue_tank_hull, blue_tank_turret),
#                                     (violet_tank_hull, violet_tank_turret)]

TANKS_DICT = {'Tank': {'sprite': (normal_tank_hull, normal_tank_turret),
                       'life': 1,
                       'dict_id_bullets': normal_bullet_dict},
              'Beast': {'sprite': (beast_tank_hull, beast_tank_turret),
                        'life': 1,
                        'dict_id_bullets': beast_bullet_dict},
              'Player': {'sprite': (green_tank_hull, green_tank_turret),
                         'life': 2,
                         'dict_id_bullets': hero_bullet_dict},
              'Heavy': {'sprite': (heavy_tank_hull, heavy_tank_turret),
                        'life': 2,
                        'dict_id_bullets': heavy_bullet_dict},
              'Allied': {'sprite': (salad_tank_hull, salad_tank_turret),
                         'life': 1,
                         'dict_id_bullets': normal_bullet_dict},
              'Convoy': {'sprite': (convoy_hull, convoy_turret),
                         'life': 2,
                         'dict_id_bullets': 0}}


# def calculate_distance_for_player(object):
#     obj_coords = object.get_position()
#     pl_coords = get_player_coords()
#     a, b = abs(obj_coords[0] - pl_coords[0]) + 1, abs(obj_coords[1] - pl_coords[1])
#     c = pow((a ** 2 + b ** 2), 0.5)
#     if object.__repr__() == 'Player':
#         return load_user_info()[load_current_user()]['sound_value'] / 100
#     percent = round(1 / c, 3) * (load_user_info()[load_current_user()]['sound_value'] / 100)
#     return percent if percent >= 0.08 else 0


# def play_sound(object, name_of_sound):
#     if object is not None:
#         sound = object.sound_dict[name_of_sound]
#         volume = calculate_distance_for_player(object)
#         if name_of_sound == 'death':
#             volume += 0.2
#         sound.set_volume(volume)
#         if (object.__repr__() == 'Beast' and name_of_sound == 'death') or \
#                 name_of_sound == 'near_fly':
#             sound.play()
#         else:
#             sound.play(maxtime=1000, fade_ms=200)
#             sound.fadeout(500)
#     else:
#         volume = load_user_info()[load_current_user()]['sound_value'] / 100
#         sound = pygame.mixer.Sound(name_of_sound)
#         sound.set_volume(volume)
#         sound.play()

class GameCell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, tile_size=TILE_SIZE):
        super(GameCell, self).__init__()


class BreakableGameCell(GameCell):
    def __init__(self, x: int, y: int, tile_size=TILE_SIZE):
        super(BreakableGameCell, self).__init__(x, y, TILE_SIZE)


class Tank(pygame.sprite.Sprite):
    def __init__(self, position, rotate_turret=0,
                 rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, respawn=False):
        super().__init__()

        self.speed = 0.20
        self.accuracy = 0.20
        self.health = TANKS_DICT[self.__repr__()]['life']
        self.team = 'black'
        self.respawn = respawn
        self.control_keys = control_keys
        self.is_crashed = False
        self.kills = 0

        self.crash_tank_image_turret = crash_tank
        self.dict_id_bullets = TANKS_DICT[self.__repr__()]['dict_id_bullets']

        # инициализация корпуса и башни
        self.init_tank_graphics(position, rotate_hull, rotate_turret)

        self.group = group
        if self.group is not None:
            self.group.add(self)
            self.group.add(self.tank_turret)

        # таймеры
        self.shooting_cooldown = 40 * FPS
        self.current_shooting_cooldown = 0

        self.move_forward_cooldown = 8 * FPS
        self.current_move_forward_cooldown = 0

        self.move_back_cooldown = 10 * FPS
        self.current_move_back_cooldown = 0

        self.turn_cooldown = 20 * FPS
        self.current_turn_cooldown = 0

        self.turn_turret_cooldown = 30 * FPS
        self.current_turn_turret_cooldown = 0

        # # init sound_dict
        # self.sound_dict = dict()
        # self.sound_dict['fire'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'fire.mp3'))
        # self.sound_dict['death'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'death.mp3'))
        # self.sound_dict['move'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'move.mp3'))
        # self.sound_dict['respawn'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'other', 'respawn.mp3'))

        if self.respawn:
            self.respawn_time = 10 * FPS
            self.respawn_args = (position, rotate_hull, rotate_turret)

    def init_tank_graphics(self, position, rotate_hull, rotate_turret):
        # башня
        self.tank_turret = pygame.sprite.Sprite()
        # todo посмотреть нужно ли давать несколько вариантов графики Player
        self.tank_turret.image = TANKS_DICT[self.__repr__()]['sprite'][1]
        self.tank_turret.rect = self.tank_turret.image.get_rect()
        self.tank_turret.rect.x = position[0]
        self.tank_turret.rect.y = position[1]

        # корпус
        self.image = TANKS_DICT[self.__repr__()]['sprite'][0]
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.init_anima()

        self.rotate_turret = 0
        self.set_turret_rotate(rotate_turret)
        self.rotate_hull = 0
        self.add_rotate(rotate_hull)
        self.x, self.y = position

    def init_anima(self):
        # Анимации для корпуса
        hgw, hgh = TILE_SIZE, TILE_SIZE
        small = pygame.transform.scale(self.image, (hgw, hgh - 5))
        surf = pygame.Surface((hgw, hgh), pygame.SRCALPHA, 32)
        surf.blit(small, (hgw // 2 - small.get_width() // 2,
                          hgh // 2 - small.get_height() // 2))
        self.orig = self.image.copy()
        self.animated_hull = surf

        # Анимации для башни
        surf = pygame.Surface((hgw, hgh), pygame.SRCALPHA, 32)
        surf.blit(self.tank_turret.image, (0, 5))
        self.orig_turret = self.tank_turret.image.copy()
        self.animated_turret = surf

    def refill_health(self):
        self.health = TANKS_DICT[self.__repr__()]['life']

    def update_timers(self, clock):
        if self.image != self.orig:
            self.image = self.orig

        if self.tank_turret.image != self.orig_turret and not self.is_crashed:
            self.tank_turret.image = self.orig_turret

        speed_of_update = 40
        self.current_shooting_cooldown -= speed_of_update
        self.current_move_forward_cooldown -= speed_of_update
        self.current_move_back_cooldown -= speed_of_update
        self.current_turn_cooldown -= speed_of_update
        self.current_turn_turret_cooldown -= speed_of_update
        if self.respawn and self.is_crashed:
            self.respawn_time -= 1
            self.clear_the_tank()
            if self.respawn_time <= 0:
                # Очищение танка от всех бонусов, которые он мог собрать
                self.move_forward_cooldown = 8 * FPS
                self.shooting_cooldown = 40 * FPS
                self.dict_id_bullets = TANKS_DICT[self.__repr__()]['dict_id_bullets']

                self.respawn_time = 10 * FPS
                self.is_crashed = False
                self.init_tank_graphics(*self.respawn_args)
                self.set_position(self.respawn_args[0][0], self.respawn_args[0][1])
                self.refill_health()

    def get_position(self):
        return self.x, self.y

    def get_rotate(self):
        return self.rotate_turret, self.rotate_hull

    def set_control_keys(self, keys):
        self.control_keys = keys

    def set_position(self, x, y):
        self.image = self.animated_hull
        self.tank_turret.rect.x += x
        self.tank_turret.rect.y += y
        self.rect.x += x
        self.rect.y += y
        self.x, self.y = x, y

    def set_turret_rotate(self, rotate):
        self.rotate_turret = (self.rotate_turret + rotate) % 360
        self.orig_turret = pygame.transform.rotate(self.orig_turret, rotate)
        self.animated_turret = pygame.transform.rotate(self.animated_turret, rotate)

    def add_rotate(self, rotate):
        self.rotate_hull = (self.rotate_hull + rotate) % 360
        self.orig = pygame.transform.rotate(self.orig, rotate)
        self.animated_hull = pygame.transform.rotate(self.animated_hull, rotate)
        # self.image = pygame.transform.rotate(self.image, rotate)
        # self.set_turret_rotate(rotate)

    # todo оптимизровать нахождение угла
    def get_cutted_angle(self) -> int:
        angle = self.rotate_hull
        while angle > 90:
            angle -= 90
        return angle

    # todo move не должен возвращать bool!
    def calc_x_y(self, hypotenuse):
        if self.rotate_hull == 180 | self.rotate_hull == 0:
            return hypotenuse, 0

        if self.rotate_hull == 90 | self.rotate_hull == 270:
            return 0, hypotenuse

        angle = self.get_cutted_angle()
        x = abs(sin(angle) * hypotenuse)
        y = abs(cos(angle) * hypotenuse)

        return x, y

    def move_rect(self, step):
        x, y = self.calc_x_y(step)
        # узнать направление
        if self.rotate_hull > 90 & self.rotate_hull < 270:
            y *= -1
        if self.rotate_hull < 360 & self.rotate_hull > 180:
            x *= -1
        self.set_position(x, y)

    def move_forward(self, step=MOVE_STEP):
            if self.current_move_forward_cooldown <= 0:
                self.move_rect(step)

                self.current_move_forward_cooldown = self.move_forward_cooldown
                return True
            return False

    def move_back(self, step=MOVE_STEP):
        if self.current_move_back_cooldown <= 0:
            self.move_rect(-step)
            self.current_move_back_cooldown = self.move_back_cooldown
            return True
        return False

    def turn_right(self):
        if self.current_turn_cooldown <= 0:
            self.set_rotate(270)
            self.current_turn_cooldown = self.turn_cooldown
            return True
        return False

    def turn_left(self):
        if self.current_turn_cooldown <= 0:
            self.set_rotate(90)
            self.current_turn_cooldown = self.turn_cooldown
            return True
        return False

    def turn_turret_right(self):
        if self.current_turn_turret_cooldown <= 0:
            self.set_turret_rotate(270)
            self.current_turn_turret_cooldown = self.turn_turret_cooldown
            return True
        return False

    def turn_turret_left(self):
        if self.current_turn_turret_cooldown <= 0:
            self.set_turret_rotate(90)
            self.current_turn_turret_cooldown = self.turn_turret_cooldown
            return True
        return False

    def shoot(self, bullets_list):
        if self.current_shooting_cooldown <= 0:
            self.tank_turret.image = self.animated_turret
            bullets_list.append(Bullet(
                self.get_position(), self.rotate_turret, self.dict_id_bullets, self))
            self.current_shooting_cooldown = self.shooting_cooldown
            return True
        return False

    def destroy_the_tank(self, another_group):
        self.is_crashed = True
        self.tank_turret.image = pygame.transform.rotate(
            self.crash_tank_image_turret, self.get_rotate()[1])
        if self.__repr__() != 'Player' and not self.respawn:
            another_group.remove(self)

    def clear_the_tank(self):
        self.group.remove(self)
        self.group.remove(self.tank_turret)

    def __repr__(self):
        return 'Tank'


class Convoy(Tank):
    def __init__(self, position, rotate_turret=0,
                 rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, respawn=False):
        super().__init__(position, rotate_turret, rotate_hull,
                         control_keys, group, respawn)
        self.team = 'green'
        self.speed = 1
        self.accuracy = 1
        self.move_forward_cooldown = 35 * FPS        

        self.crash_tank_image_turret = convoy_crash
        self.turn_turret_cooldown *= 3

    def shoot(self, bullets_list):
        if self.turn_turret_right():
            pass

    def __repr__(self):
        return 'Convoy'


class Player(Tank):
    def __init__(self, position, rotate_turret=0,
                 rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, respawn=False):
        super().__init__(position, rotate_turret,
                         rotate_hull, control_keys, group, respawn)

        # Иницализация уникальных звуков для игрока
        # self.sound_dict['turn_turret'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'turn_turret.mp3'))
        # self.sound_dict['move'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'move.mp3'))
        # self.sound_dict['brake'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'brake.mp3'))
        # self.sound_dict['turn_hull'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'tanks', self.__repr__(), 'turn_hull.mp3'))
        self.team = 'green'

        # Поворт турели
        self.is_turret_rotating_right_up = False
        self.is_turret_rotating_left_up = False

        self.is_stop = True

    def __repr__(self):
        return 'Player'

    def init_tank_graphics(self, position, rotate_hull, rotate_turret):
        colorset_from_controlkeys_index = [CONTROL_KEYS_V1, CONTROL_KEYS_V2, CONTROL_KEYS_V3,
                                           CONTROL_KEYS_V4].index(self.control_keys)

        super().init_tank_graphics(position, rotate_hull, rotate_turret)

    def turn_turret_left(self):
        super().turn_turret_left()

    def turn_turret_right(self):
        super(Player, self)

    def set_position(self, x, y):
        super(Player, self).set_position(x, y)
        self.is_stop = False

    def turn_left(self):
        super(Player, self).turn_left()

    def turn_right(self):
        super(Player, self).turn_right()

    def play_brake(self):
        if not self.is_stop:
            self.is_stop = True


class Allied(Tank):
    def __init__(self, position, rotate_turret=0,
                 rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, respawn=False):
        super().__init__(position, rotate_turret,
                         rotate_hull, control_keys, group, respawn)
        self.team = 'green'
        self.speed = 0.25
        self.accuracy = 0.25

    def __repr__(self):
        return 'Allied'


class Beast(Tank):
    def __init__(self, position, rotate_turret=0,
                 rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, respawn=False):
        super().__init__(position, rotate_turret,
                         rotate_hull, control_keys, group, respawn)
        self.speed = 0.666
        self.accuracy = 0.333

        self.move_forward_cooldown = 16 * FPS

    def __repr__(self):
        return 'Beast'

    def set_position(self, position):
        self.image = self.animated_hull
        self.tank_turret.rect.x, self.tank_turret.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE
        self.rect.x, self.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE
        self.x, self.y = position


class Heavy(Tank):
    def __init__(self, position, rotate_turret=0,
                 rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, respawn=False):
        super().__init__(position, rotate_turret,
                         rotate_hull, control_keys, group, respawn)
        self.speed = 0.10
        self.accuracy = 0.40        

    def __repr__(self):
        return 'Heavy'


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, rotate, bullet_dict, owner=None):
        super().__init__()
        self.x, self.y = position
        self.owner = owner

        image = bullet_dict[0]
        self.damage_type = bullet_dict.get('damage_type', None)

        self.image = pygame.transform.rotate(image, rotate)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE

        self.group = pygame.sprite.Group()
        self.group.add(self)

        # self.sound_dict = dict()
        # self.sound_dict['collision_unbreak'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'bullets', 'collision_unbreak.mp3'))
        # self.sound_dict['collision_break'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'bullets', 'collision_break.mp3'))
        # self.sound_dict['near_fly'] = pygame.mixer.Sound(
        #     os.path.join(SOUND_DIR, 'bullets', 'near_fly.mp3'))

    def get_position(self):
        return self.x, self.y

    def get_direction_move(self):
        return self.direction_move

    def set_position(self, position):
        self.x, self.y = position

    def next_move(self):
        self.x += self.direction_move[0]
        self.y += self.direction_move[1]
        self.rect.x, self.rect.y = \
            self.x * TILE_SIZE, self.y * TILE_SIZE

    def render(self, screen):
        self.group.draw(screen)


class MapObject(pygame.sprite.Sprite):
    def __init__(self, position, respawn, respawn_time, hidden):
        super(MapObject, self).__init__()
        self.x, self.y = position

        self.respawn = respawn
        self.respawn_cooldown = respawn_time
        self.respawn_time = respawn_time

        self.hidden = hidden

    def init_image(self):
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x * TILE_SIZE, self.y * TILE_SIZE

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def trigger_action(self, map):
        if not self.respawn:
            map.map_objects.remove(self)
        else:
            self.hidden = True

    def do_respawn(self):
        self.respawn_time -= 1
        if self.respawn_time == 0:
            self.hidden = False
            self.respawn_time = self.respawn_cooldown

    def __repr__(self):
        return 'MapObject'


class Life_MapObject(MapObject):
    def __init__(self, position, respawn, respawn_time, hidden):
        super().__init__(position, respawn, respawn_time, hidden)
        self.image = map_life
        self.init_image()

    def trigger_action(self, map):
        super().trigger_action(map)
        # Танк, который наступил на объект карты
        x, y = self.get_position()
        map.map[y][x].health += 1
        # play_sound(None, os.path.join(SOUND_DIR, 'other', 'recharge.wav'))

    def __repr__(self):
        return 'Life_MapObject'


class Boost_MapObject(MapObject):
    def __init__(self, position, respawn, respawn_time, hidden):
        super().__init__(position, respawn, respawn_time, hidden)
        self.image = map_boost
        self.init_image()

    def trigger_action(self, map):
        super().trigger_action(map)
        # Танк, который наступил на объект карты
        x, y = self.get_position()
        tank = map.map[y][x]
        tank.shooting_cooldown -= tank.shooting_cooldown / 100 * 30
        tank.move_forward_cooldown -= tank.move_forward_cooldown / 100 * 30

    def __repr__(self):
        return 'Boost_MapObject'


class Gun_MapObject(MapObject):
    def __init__(self, position, respawn, respawn_time, hidden):
        super().__init__(position, respawn, respawn_time, hidden)

    def trigger_action(self, map, gun_image, take_sound_name, gun_bullet_dict, which_fire_sound):
        super().trigger_action(map)
        # Танк, который наступил на объект карты
        x, y = self.get_position()
        tank = map.map[y][x]
        tank.tank_turret.image = gun_image
        tank.init_anima()
        old_rotate = tank.get_rotate()[0]
        tank.rotate_turret = 0
        tank.dict_id_bullets = gun_bullet_dict
        tank.set_turret_rotate(old_rotate)


class Uran_MapObject(Gun_MapObject):
    def __init__(self, position, respawn, respawn_time, hidden):
        super().__init__(position, respawn, respawn_time, hidden)
        self.image = map_uran
        self.init_image()

    def trigger_action(self, map):
        take_sound = os.path.join(SOUND_DIR, 'other', 'uran_taked.mp3')
        super().trigger_action(map, heavy_tank_turret, take_sound, heavy_bullet_dict, 'Heavy')

    def __repr__(self):
        return 'Uran_MapObject'


class Energy_MapObject(Gun_MapObject):
    def __init__(self, position, respawn, respawn_time, hidden):
        super().__init__(position, respawn, respawn_time, hidden)
        self.image = map_energy
        self.init_image()

    def trigger_action(self, map):
        take_sound = os.path.join(SOUND_DIR, 'other', 'energy_taked.mp3')
        super().trigger_action(map, beast_tank_turret, take_sound, beast_bullet_dict, 'Beast')

    def __repr__(self):
        return 'Energy_MapObject'
