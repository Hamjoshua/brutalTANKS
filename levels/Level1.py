from main import GameManager, GameMap


class Level:
    @staticmethod
    def lvl1(map_name):
        map = GameMap("1_lvl.tmx")
        game = GameManager(map)
        return game
