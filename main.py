from constants import *
from game_objects import *
from levels import Level1

import pygame
import pygame_gui
import pytmx

# import util_pygame


class GuiResponse:
    message: str
    code: int


class Camera:
    def __init__(self, width, height, shift_x=7, shift_y=7):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.map_x, self.map_y = 0, 0

    def in_range(self, x: int, y: int) -> bool:
        camera_coord = \
            abs(self.rect.x // TILE_SIZE), \
            abs(self.rect.y // TILE_SIZE)

        return x in range(camera_coord[0], self.rect.width) and \
               y in range(camera_coord[1], self.rect.height)

    def apply(self, obj):
        if isinstance(obj, Bullet):
            obj.rect.x += self.rect.left
            obj.rect.y += self.rect.top
        if isinstance(obj, Tank):
            pass
        elif isinstance(obj, pygame.Rect):
            obj.width += self.rect.left
            obj.height += self.rect.top

    def update(self, target, immediately=False):
        if isinstance(target, tuple):
            target_x, target_y = target
            if self.map_x > target_x:
                self.map_x -= 1
            elif self.map_x < target_x:
                self.map_x += 1

            if self.map_y > target_y:
                self.map_y -= 1
            elif self.map_y < target_y:
                self.map_y += 1
            target_x, target_y = self.map_x, self.map_y
        else:
            target_x = target.x
            target_y = target.y
            self.map_x, self.map_y = target_x, target_y

        dx = -(target_x * TILE_SIZE - (self.shift_x * TILE_SIZE))
        dy = -(target_y * TILE_SIZE - (self.shift_y * TILE_SIZE))

        # ограничения камеры, чтобы она не показала черных границы
        if abs(dx) >= (self.width - 14) * TILE_SIZE:
            dx = self.rect.x
            if immediately:
                dx = -(self.width - 15) * TILE_SIZE
        if dx > 0:
            dx = 0

        if abs(dy) >= (self.height - 14) * TILE_SIZE:
            dy = self.rect.y
        if dy > 0:
            dy = 0
            if immediately:
                dx = -(self.height - 15) * TILE_SIZE
        self.rect = pygame.Rect(dx, dy, self.width, self.height)


class GameMap:
    # todo может, все объекты карты будут спрайтами
    def __init__(self, filename):
        self.tiled_map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")

        self.map = self.generate_map()

        self.height = self.tiled_map.height
        self.width = self.tiled_map.width

        # Инициализация слоев
        self.free_tiles = []
        self.break_tiles = []
        self.unbreak_tiles = []

        for y in range(self.height):
            for x in range(self.width):
                type_of_tile = self.get_type_of_tile(x, y)
                id_of_tile = self.tiled_map.get_tile_gid(x, y, 0)
                if 'free' in type_of_tile and id_of_tile not in self.free_tiles:
                    self.free_tiles.append(id_of_tile)
                elif type_of_tile == 'break' and id_of_tile not in self.break_tiles:
                    self.break_tiles.append(id_of_tile)
                elif 'unbreak' in type_of_tile and id_of_tile not in self.unbreak_tiles:
                    self.unbreak_tiles.append(id_of_tile)
        self.shadow = []
        self.lava = []
        self.map_objects = []

    def parse_lava_and_shadow(self, tile_object):
        if tile_object.name == 'Shadow':
            special_group = self.shadow
        else:
            special_group = self.lava
        x = int(tile_object.x // TILE_SIZE)
        y = int(tile_object.y // TILE_SIZE)
        w = int(tile_object.width // TILE_SIZE)
        h = int(tile_object.height // TILE_SIZE)
        for y_step in range(y, y + h):
            for x_step in range(x, x + w):
                special_group.append((x_step, y_step))

    def parse_map_objects(self, tile_object):
        pass
        # x, y = int(tile_object.x // TILE_SIZE), int(tile_object.y // TILE_SIZE)
        # respawn = tile_object.properties.get('respawn', False)
        # respawn_time = tile_object.properties.get('respawn_time', 0)
        # hidden = tile_object.properties.get('hidden', False)
        # init_object_string = f'{tile_object.name}((x, y), {respawn},' \
        #                      f' {respawn_time}, {hidden})'
        #
        # self.map_objects.append(eval(init_object_string))

    def parse_instances(self, tile_object, player_list, tank_list, sprite_group):
        rotate_turret = tile_object.properties['rotate_turret']
        rotate_hull = tile_object.properties['rotate_hull']
        destination = str(tile_object.properties['destination'])
        respawn = tile_object.properties.get('respawn', False)
        x, y = tile_object.x, tile_object.y
        init_object_string = f'{tile_object.name.split(" ")[0]}((x, y),' \
                             f' rotate_turret=rotate_turret,' \
                             f' rotate_hull=rotate_hull, group=sprite_group,' \
                             f' respawn=respawn)'
        if 'Player' in tile_object.name:
            player_list.append(eval(init_object_string))
        else:
            tank_list.append(eval(init_object_string))

        # if destination == 'self':
        #     destinations[tank_list[-1]] = None
        # elif destination == 'player':
        #     destinations[tank_list[-1]] = get_player_coords
        # elif 'detect' in destination:
        #     def detect_func(range_x, range_y):
        #         if get_player_coords()[0] in range_x and \
        #                 get_player_coords()[1] in range_y:
        #             return get_player_coords
        #         return None
        #
        #     ranges = get_ranges_from_detect(destination)
        #     destinations[tank_list[-1]] = (detect_func, ranges)
        # elif 'pos' in destination:
        #     destinations[tank_list[-1]] = \
        #         eval(destination[len('pos '):])

    # todo неправильно, что одновременно инициализация и выдача
    def init_map_objects_and_get_instances(self, sprite_group):
        player_list = []
        tank_list = []
        for tile_object in self.tiled_map.objects:
            # Парсинг тени и лавы
            if tile_object.name in ['Shadow', 'Lava']:
                self.parse_lava_and_shadow(tile_object)
            # Парсинг объектов карты
            elif 'Map' in tile_object.name:
                self.parse_map_objects(tile_object)
            # Парсинг танков
            else:
                self.parse_instances(tile_object, player_list, tank_list, sprite_group)

        return player_list, tank_list

    def get_free_block(self, x, y):
        id_of_free_block = self.tiled_map.get_tile_gid(x, y, 0)
        if id_of_free_block not in self.free_tiles:
            id_of_free_block = self.free_tiles[0]
        return id_of_free_block

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def get_type_of_tile(self, x, y):
        if x not in range(self.width) or y not in range(self.height):
            return None
        check_prop = self.tiled_map.get_tile_properties
        return check_prop(x, y, 0)['type']

    def generate_map(self):
        return [[self.tiled_map.get_tile_gid(x, y, 0)
                 for x in range(self.tiled_map.width)]
                for y in range(self.tiled_map.height)]

    def render(self, screen, camera):
        screen.fill('#000000')
        for layer in self.tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:

                    # Объекты вне зоны действия камеры не будут отрисовываться
                    if not camera.in_range(x, y):
                        continue

                    gid = self.map[y][x]
                    object_stand_on = False
                    # Если на блоке уже кто-то стоит
                    if not isinstance(gid, int):
                        gid = self.get_free_block(x, y)
                        object_stand_on = True

                    tile = self.tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile_rect = pygame.Rect(
                            0, 0, x * self.tiled_map.tilewidth,
                                  y * self.tiled_map.tileheight)
                        camera.apply(tile_rect)
                        screen.blit(tile, (tile_rect.width, tile_rect.height))

                        if (x, y) in self.lava:
                            self.draw_lava(tile_rect)

                        # Если на блоке кто-то стоит, надо отрисовать стоящего
                        # if object_stand_on:
                        #     self.draw_standing_object()

                        if (x, y) in self.shadow:
                            self.draw_shadow(tile_rect)
        self.update_objects()

    def draw_lava(self, tile_rect):
        screen.blit(lava, (tile_rect.width, tile_rect.height))

    def draw_shadow(self, tile_rect):
        shadow = pygame.Surface(
            (self.tiled_map.tilewidth,
             self.tiled_map.tileheight))
        shadow.fill(pygame.Color(0, 0, 0))
        shadow.set_alpha(99)
        screen.blit(shadow, (tile_rect.width,
                             tile_rect.height))

    # def draw_standing_object(self, tile_rect):
    #     screen.blit(self.map[y][x].image,
    #                 (tile_rect.width, tile_rect.height))
    #     if getattr(self.map[y][x], 'tank_turret', False):
    #         screen.blit(self.map[y][x].tank_turret.image,
    #                     (tile_rect.width, tile_rect.height))
    #     if self.map[y][x].respawn:
    #         if self.map[y][x].respawn_time <= 90:
    #             self.map[y][x] = self.get_free_block(x, y)

    def update_objects(self):
        for map_object in self.map_objects:
            x, y = map_object.get_position()
            if map_object.hidden:
                map_object.do_respawn()
            else:
                if isinstance(self.map[y][x], Player):
                    map_object.trigger_action(self)
                else:
                    self.map[y][x] = map_object


class GameManager:
    is_active: bool = True
    is_active_cutscene: bool = False
    events: list = list()
    players: list = list()
    bots: list = list()

    instances_group: pygame.sprite.Group = pygame.sprite.Group()
    static_objects_group: pygame.sprite.Group = pygame.sprite.Group()

    level_name: str
    map: GameMap
    camera: Camera

    def __init__(self, game_map: GameMap):
        self.map = game_map
        self.level_name = self.map.tiled_map.filename
        self.camera = Camera(self.map.width, self.map.height)

        self.players, self.bots = self.map.init_map_objects_and_get_instances(self.instances_group)

    def make_events(self):
        for event in self.events:
            event()

    # todo такое ощущение, что этот метод должен быть в библоитеке взаимосдействия между спрайтами
    def restrict_movement(self, invader_sprite: Tank, defender_sprite):
        if invader_sprite.rect.x > defender_sprite.rect.x or invader_sprite.rect.x < defender_sprite.rect.x:
            invader_sprite.rect.x = defender_sprite.rect.x
        if invader_sprite.rect.y > defender_sprite.rect.y or invader_sprite.rect.y < defender_sprite.rect.y:
            invader_sprite.rect.y = defender_sprite.rect.y

    def move_instance(self, vector: tuple, tank: Tank):
        # todo move_instance
        old_x: int = tank.x
        old_y: int = tank.y

        tank.move_forward()
        collided_sprites = pygame.sprite.spritecollide(tank.image, self.instances_group, False)
        for sprite in collided_sprites:
            self.restrict_movement(tank, sprite)

    def get_vector_for_player(self, player: Player) -> tuple:
        is_movement_key_pressed = False

        if player.is_crashed:
            return None, None
        unpack_player_coords = player.x, player.y
        if not unpack_player_coords:
            cur_x, cur_y = next_x, next_y = player.get_position()
        else:
            cur_x, cur_y = next_x, next_y = unpack_player_coords

        rotate_turret, rotate_hull = player.get_rotate()

        if pygame.key.get_pressed()[player.control_keys[FORWARD]]:
            player.move_forward()

        elif pygame.key.get_pressed()[player.control_keys[BACK]]:
            player.move_back()

        elif pygame.key.get_pressed()[player.control_keys[TURN_RIGHT]]:
            is_movement_key_pressed = True
            # todo определить значение поворота
            player.add_rotate(30)

        elif pygame.key.get_pressed()[player.control_keys[TURN_LEFT]]:
            is_movement_key_pressed = True
            player.add_rotate(-30)

        if (next_x, next_y) == (cur_x, cur_y):
            player.play_brake()

    def move_player(self, player: Player):
        # todo получение вектора движения
        # todo vector в виде отдельного класса
        vector: tuple
        vector = self.get_vector_for_player(player)

        if vector == (None, None):
            return

        # self.move_instance(vector, player)
        collided_sprites = pygame.sprite.spritecollide(player, self.instances_group, False)
        for sprite in collided_sprites:
            self.restrict_movement(player, sprite)

    def update_bots(self):
        pass

    def update_players(self):
        for player in self.players:
            self.move_player(player)
            self.camera.update(player)
            self.camera.apply(player)
            self.map.camera = self.camera
            
    def get_status(self):
        return -1

    def show_cutscenes(self):
        pass

    def render_instances(self, screen):
        all_instances = self.bots + self.players

        for bot in all_instances:
            bot: Tank
            # todo костыль с проверкой вхождения сущности в камеру
            if not self.camera.in_range(bot.x // TILE_SIZE, bot.y // TILE_SIZE):
                continue
            screen.blit(bot.image, (bot.x, bot.y))

    def render(self, screen):
        self.map.render(screen, self.camera)
        self.render_instances(screen)


# todo заняться гуи
class GuiManager:
    def __init__(self):
        pass

    def show_menu(self) -> GuiResponse:
        responce = GuiResponse()
        responce.code = GuiCodes.Ok
        responce.message = "1_lvl"

        return responce        

    def show_pause(self, screen) -> GuiResponse:
        responce = GuiResponse()
        responce.code = GuiCodes.Cancel
        responce.message = "example"

        return responce

    def draw_hud(self, screen, game: GameManager):
        pass

    def show_victory_screen(self, screen) -> GuiResponse:
        responce = GuiResponse()
        responce.code = GuiCodes.Ok
        responce.message = "example"
        
        return responce

    def show_defeat_screen(self, screen) -> GuiResponse:
        responce = GuiResponse()
        responce.code = GuiCodes.Ok
        responce.message = "example"

        return responce


class LevelManager:
    @staticmethod
    def init_level(lvl_name) -> GameManager:
        game: GameManager

        if lvl_name == "1_lvl":
            return Level1.Level.lvl1(lvl_name)


def handle_inactive_game(game: GameManager, screen, gui_manager: GuiManager) -> GameManager:
    status = game.get_status()
    reply: GuiResponse
    if status == GameConditions.GameIsWon:
        reply = gui_manager.show_victory_screen(screen)
        if reply.code == GuiCodes.Ok:
            level: str = game.level_name
            return LevelManager.init_level(level)

    elif status == GameConditions.GameIsLoosed:
        reply = gui_manager.show_defeat_screen(screen)
        if reply.code == GuiCodes.Ok:
            level: str = game.level_name
            return LevelManager.init_level(level)

    elif status == GameConditions.GameIsPaused:
        reply = gui_manager.show_pause(screen)
        if reply.code == GuiCodes.Cancel:
            game.is_active = True
            return game

        # todo как сделать паузу и прочее гуи? будут ли они что-то возвращать?

    if reply.code == GuiCodes.Menu:
        reply = gui_manager.show_menu()
        return LevelManager.init_level(reply.message)
    elif reply.code == GuiCodes.LoadGame:
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
    level: str = gui_manager.show_menu().message
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