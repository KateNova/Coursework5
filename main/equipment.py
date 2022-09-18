from dataclasses import dataclass, field
from random import uniform
from typing import List, Optional
import json

import marshmallow_dataclass
import marshmallow


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: list[Weapon] = field(default_factory=list)
    armors: list[Armor] = field(default_factory=list)


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> List[str]:
        return [x.name for x in self.equipment.weapons]

    def get_armors_names(self) -> List[str]:
        return [x.name for x in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open('./data/equipment.json') as f:
            data = json.load(f)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
