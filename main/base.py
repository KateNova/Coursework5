from main.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Результат игры: Ничья'
        if self.player.hp <= 0:
            self.battle_result = f'Результат игры: {self.enemy.name} выиграл'
        if self.enemy.hp <= 0:
            self.battle_result = f'Результат игры: {self.player.name} выиграл'
        return self._end_game()

    def _abstract_stamina_regeneration(self, unit):
        if unit.stamina + self.STAMINA_PER_ROUND >= unit.unit_class.max_stamina:
            unit.stamina = unit.unit_class.max_stamina
        else:
            unit.stamina += self.STAMINA_PER_ROUND

    def _stamina_regeneration(self):
        self._abstract_stamina_regeneration(self.player)
        self._abstract_stamina_regeneration(self.enemy)

    def next_turn(self):
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self):
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        result = self._check_players_hp()
        if result:
            return result
        return f'{self.player.hit(self.enemy)}\n{self.next_turn()}'

    def player_use_skill(self):
        result = self._check_players_hp()
        if result:
            return result
        return f'{self.player.use_skill(self.enemy)}\n{self.next_turn()}'
