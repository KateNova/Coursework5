from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from main.classes import UnitClass
from main.equipment import Weapon, Armor


class BaseUnit(ABC):

    def __init__(self, name: str, unit_class: UnitClass):
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f'{self.name} экипирован оружием {self.weapon.name}'

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f'{self.name} экипирован броней {self.weapon.name}'

    def _count_damage(self, target) -> int:
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage = damage - target.armor.defence * target.unit_class.armor
        target.get_damage(damage)
        return round(damage, 1)

    def get_damage(self, damage: int) -> None:
        self.hp -= damage

    @abstractmethod
    def hit(self, target) -> str:
        pass

    def use_skill(self, target) -> str:
        if self._is_skill_used:
            return 'Навык уже использован.'
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina < self.weapon.stamina_per_hit * self.unit_class.stamina:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'
        damage = self._count_damage(target)
        if damage > 0:
            return f'{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника ' \
                   f'и наносит {damage} урона. '
        if damage == 0:
            return f'{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} ' \
                   f'соперника его останавливает.'


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if randint(0, 100) < 10 and self.stamina >= self.unit_class.skill.stamina and not self._is_skill_used:
            return self.use_skill(target)
        if self.stamina >= self.weapon.stamina_per_hit * self.unit_class.stamina:
            damage = self._count_damage(target)
            if damage:
                return f'{self.name} используя {self.weapon.name} пробивает {target.armor.name} ' \
                       f'и наносит Вам {damage} урона.'
            return f'{self.name} используя{self.weapon.name} наносит удар, но Ваш(а) ' \
                   f'{target.armor.name} его останавливает.'
        return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'
