from main import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

green_tank_turret = pygame.transform.scale(load_image(
            "green_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
green_tank_hull = pygame.transform.scale(load_image(
            "green_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
red_tank_turret = pygame.transform.scale(load_image(
            "red_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
red_tank_hull = pygame.transform.scale(load_image(
            "red_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
beast_tank_hull = pygame.transform.scale(load_image(
            "beast_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
beast_tank_turret = pygame.transform.scale(load_image(
            "beast_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
heavy_tank_hull = pygame.transform.scale(load_image(
            "heavy_hull.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
heavy_tank_turret = pygame.transform.scale(load_image(
            "heavy_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
crash_tank = pygame.transform.scale(load_image(
            "crached_turret.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))
bullet_0 = pygame.transform.scale(load_image(
            "bullet_0.png", colorkey=-1), (TILE_SIZE, TILE_SIZE))

sprites_dict = {'Tank': (red_tank_hull, red_tank_turret),
                'Beast': (beast_tank_hull, beast_tank_turret),
                'Player': (green_tank_hull, green_tank_turret),
                'Heavy': (heavy_tank_hull, heavy_tank_turret)}

normal_bullet_dict = {0: bullet_0}


class Tank(pygame.sprite.Sprite):
    def __init__(self, position, rotate_turret=0, rotate_hull=0, control_keys=CONTROL_KEYS_V1, group=None, is_player=False):
        super().__init__()

        self.is_player = is_player

        self.speed = 0.20
        self.accuracy = 0.20
        self.health = 1

        self.crash_tank_image_turret = crash_tank
        self.dict_id_bullets = normal_bullet_dict

        # init turret
        self.tank_turret = pygame.sprite.Sprite()
        self.tank_turret.image = sprites_dict[self.__repr__()][1]
        self.tank_turret.rect = self.tank_turret.image.get_rect()
        self.tank_turret.rect.x, self.tank_turret.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE

        # init hull
        self.image = sprites_dict[self.__repr__()][0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE

        self.rotate_turret = 0
        self.set_turret_rotate(rotate_turret)
        self.rotate_hull = 0
        self.set_rotate(rotate_hull)
        self.x, self.y = position

        self.group = group
        if self.group is not None:
            self.group.add(self)
            self.group.add(self.tank_turret)

        self.control_keys = control_keys
        self.is_crashed = False

        # timers
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

    def update_timers(self, clock):
        self.current_shooting_cooldown -= clock.get_time()
        self.current_move_forward_cooldown -= clock.get_time()
        self.current_move_back_cooldown -= clock.get_time()
        self.current_turn_cooldown -= clock.get_time()
        self.current_turn_turret_cooldown -= clock.get_time()

    def get_position(self):
        return self.x, self.y

    def get_rotate(self):
        return self.rotate_turret, self.rotate_hull

    def set_control_keys(self, keys):
        self.control_keys = keys

    def set_position(self, position):
        self.tank_turret.rect.x, self.tank_turret.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE
        self.rect.x, self.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE
        self.x, self.y = position

    def set_turret_rotate(self, rotate):
        self.rotate_turret = (self.rotate_turret + rotate) % 360
        self.tank_turret.image = pygame.transform.rotate(self.tank_turret.image, rotate)

    def set_rotate(self, rotate):
        self.rotate_hull = (self.rotate_hull + rotate) % 360
        self.image = pygame.transform.rotate(self.image, rotate)
        self.set_turret_rotate(rotate)

    def move_forward(self):
        if self.current_move_forward_cooldown <= 0:
            direction_move = [round(i) for i in DIRECTION_MOVE_BY_ANGLE[self.rotate_hull]]
            self.set_position((self.x + direction_move[0], self.y + direction_move[1]))
            self.current_move_forward_cooldown = self.move_forward_cooldown
            return True
        return False

    def move_back(self):
        if self.current_move_back_cooldown <= 0:
            direction_move = [round(i) for i in DIRECTION_MOVE_BY_ANGLE[self.rotate_hull]]
            self.set_position((self.x - direction_move[0], self.y - direction_move[1]))
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
            bullets_list.append(Bullet(
                self.get_position(), self.rotate_turret, self.dict_id_bullets[0]))
            self.current_shooting_cooldown = self.shooting_cooldown
            return True
        return False

    def destroy_the_tank(self, another_group):
        self.is_crashed = True
        self.tank_turret.image = pygame.transform.rotate(
            self.crash_tank_image_turret, self.get_rotate()[1])
        if not self.is_player:
            another_group.remove(self)

    def clear_the_tank(self):
        self.group.remove(self)
        self.group.remove(self.tank_turret)

    def __repr__(self):
        if self.is_player:
            return 'Player'
        else:
            return 'Tank'


class Beast(Tank):
    def __init__(self, position, rotate_turret=0, rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, is_player=False):
        super().__init__(position, rotate_turret, rotate_hull, control_keys, group, is_player)
        self.speed = 0.666
        self.accuracy = 0.333

    def __repr__(self):
        return 'Beast'


class Heavy(Tank):
    def __init__(self, position, rotate_turret=0, rotate_hull=0, control_keys=CONTROL_KEYS_V1,
                 group=None, is_player=False):
        super().__init__(position, rotate_turret, rotate_hull, control_keys, group, is_player)
        self.speed = 0.10
        self.accuracy = 0.40
        self.health = 2

    def __repr__(self):
        return 'Heavy'


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, rotate, image):
        super().__init__()
        self.x, self.y = position
        self.direction_move = DIRECTION_MOVE_BY_ANGLE[rotate]

        self.image = pygame.transform.rotate(image, rotate)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = \
            position[0] * TILE_SIZE, position[1] * TILE_SIZE

        self.group = pygame.sprite.Group()
        self.group.add(self)

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

