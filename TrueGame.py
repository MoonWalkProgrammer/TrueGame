from dataclasses import asdict, dataclass
from random import choice, randint, randrange
from time import sleep
from typing import List

from colorama import Back, Fore


@dataclass
class FighterInfo:
    """Return fighter description."""
    name: str
    fighter_class: str
    hp: int
    attack: int
    protection_percent: int
    INFORMATION: str = ('Name: {name}\n'
                        'Class: {fighter_class}\n'
                        'Health Points: {hp}\n'
                        'Attack: {attack} damage\n'
                        'Protection: {protection_percent} percent\n')

    def get_information(self) -> str:
        return self.INFORMATION.format(**asdict(self))


class Thing:
    """a class stores the properties of a thing."""
    def __init__(self,
                 name: str,
                 hp_bonus: int,
                 attack_bonus: int,
                 protection_percent_bonus: int,
                 ) -> None:
        self.name = name
        self.hp_bonus = hp_bonus
        self.attack_bonus = attack_bonus
        self.protection_percent_bonus = protection_percent_bonus


class Character:
    """Basic class for all races."""
    def __init__(self,
                 name: str,
                 hp: int,
                 attack: int,
                 protection_percent: int,
                 ) -> None:
        self.name = name
        self.hp = hp
        self.attack = attack
        self.protection_percent = protection_percent

    def set_thing(self, thing: Thing) -> None:
        """Count all bonuses of the thing"""
        self.hp += thing.hp_bonus
        self.attack += thing.attack_bonus
        self.protection_percent += thing.protection_percent_bonus

    def loss_of_health(self, enemy_strike) -> int:
        """Return the damage dealt to the player and count race bonuses."""
        damage: int = round(enemy_strike
                            * (100 - self.protection_percent) / 100)
        self.hp -= damage
        return damage

    def show_fighter_info(self) -> FighterInfo:
        """Return FighterInfo object with needed parameters."""
        return FighterInfo(self.name,
                           self.__class__.__name__,
                           self.hp,
                           self.attack,
                           self.protection_percent)

    def __str__(self) -> str:
        return f'{self.name} the {self.__class__.__name__} has {self.hp} hp.'


class Human(Character):
    """People forge great armor.
People have double HP and double protection."""
    COLOR = Fore.CYAN

    def __init__(self,
                 name: str,
                 hp: int,
                 attack: int,
                 protection_percent: int
                 ) -> None:
        super().__init__(name, hp * 2, attack, protection_percent * 2)


class Ork(Character):
    """Just bloodthirsty killers.
Orks have double attack."""
    COLOR = Fore.LIGHTRED_EX

    def __init__(self,
                 name: str,
                 hp: int,
                 attack: int,
                 protection_percent: int
                 ) -> None:
        super().__init__(name, hp, attack * 2, protection_percent)


class Elf(Character):
    """Elfs are famous for their medicine.
When Elfs are attacked, they recover 5 HP."""
    COLOR = Fore.GREEN

    def __init__(self,
                 name: str,
                 hp: int,
                 attack: int,
                 protection_percent: int
                 ) -> None:
        super().__init__(name, hp, attack, protection_percent)

    def loss_of_health(self, enemy_strike) -> int:
        """Return the damage dealt to the player and count race bonuses."""
        damage: int = round(enemy_strike
                            * (100 - self.protection_percent) / 100)
        self.hp -= damage
        self.hp += 5
        return damage


class Gnome(Character):
    """The longer the gnome lives, the more furious he becomes
If the gnome is attacked, his attack is increased by 20%, and defense by 10%"""
    COLOR = Fore.YELLOW

    def __init__(self,
                 name: str,
                 hp: int,
                 attack: int,
                 protection_percent: int
                 ) -> None:
        super().__init__(name, hp, attack, protection_percent)

    def loss_of_health(self, enemy_strike) -> int:
        damage: int = round(enemy_strike
                            * (100 - self.protection_percent) / 100)
        self.hp -= damage
        self.attack *= 1.2
        self.protection_percent += 10
        return damage


class Arena:
    """Arena class."""

    def __init__(self,
                 races,
                 names: List[str],
                 things_names: List[str]
                 ) -> None:
        self.races = races
        self.names = names
        self.things_names = things_names

    def character_selection_and_presentation(self) -> List[Character]:
        """
        User chooses a fighter
        Fighters are presented in the ring
        Function returns fighters list."""
        characters: list = []
        for _ in range(10):
            names_copy: List[str] = self.names.copy()
            character: Character = choice(self.races)(choice(names_copy),
                                                      randint(40, 50),
                                                      randint(5, 10),
                                                      randint(1, 4))
            characters.append(character)
            names_copy.remove(character.name)

        for i in range(len(characters)):
            things_names_copy = self.things_names.copy()
            for _ in range(4):
                if characters[i].protection_percent <= 10:
                    thing: Thing = Thing(choice(things_names_copy),
                                         randint(1, 10),
                                         randint(1, 5),
                                         randint(1, 3))
                    characters[i].set_thing(thing)
                    things_names_copy.remove(thing.name)
            print(Back.BLACK + Fore.RESET + str(i))
            print(characters[i].COLOR + characters[i].__doc__)
            print(f'{characters[i].show_fighter_info().get_information()}\n')
            sleep(0.5)

        fighters: List = []
        first_fighter_index: int = int(input(Fore.RESET + 'Choose your fighter '
                                       '(a number from 0 to 9): '))
        print()
        first_fighter: Character = characters[first_fighter_index]
        fighters.append(first_fighter)
        characters.remove(first_fighter)
        fighters: List[Character] = [first_fighter, choice(characters)]

        print(Fore.RESET + 'WELCOME TO RHE LORD OF THE RINGS ARENA!\n')
        sleep(2)
        print(Fore.RED + 'IN THE RED CORNER OF THE RING:')
        print(f'{fighters[0].show_fighter_info().get_information()}\n')
        sleep(2)
        print(Fore.BLUE + 'IN THE BLUE CORNER OF THE RING:')
        print(f'{fighters[1].show_fighter_info().get_information()}\n')
        sleep(2)

        print(Fore.RESET + 'FIGHT STARTS IN...')
        for i in range(3, 0, -1):
            print(i)
            sleep(1)
        print()

        return fighters

    def fight(self, fighters: List[Character]) -> None:
        """This function describes the battle process."""
        round: int = 1
        while True:
            sleep(1)
            fighters_copy: List[Character] = fighters.copy()
            attacking: Character = fighters_copy.pop(randrange(2))
            defending: Character = fighters_copy[0]
            damage: int = defending.loss_of_health(attacking.attack)

            print(Fore.RESET + f'Round {round}')
            if attacking == fighters[0]:
                fore_color = Fore.RED
            else:
                fore_color = Fore.BLUE
            print(fore_color + f'{attacking.name} hits {defending.name} '
                  f'for {damage:.0f} daamage')
            print(Fore.RED + f'{fighters[0]}')
            print(Fore.BLUE + f'{fighters[1]}\n')
            round += 1

            if defending.hp <= 0:
                break
        print(fore_color + f'{attacking.name} the {attacking.__class__.__name__} wins!\n')


races = [Human, Ork, Elf, Gnome]
names: List[str] = ['James', 'Michael', 'William', 'David', 'Daniel',
                    'Steven', 'Edward', 'Brian', 'Jose', 'Frank',
                    'Raymond', 'Walter', 'Peter', 'Douglas', 'Ryan',
                    'Juan', 'Jack', 'Bruce', 'Bobby', 'Martin']
things_names: List[str] = ['Bow', 'Sword', 'Ax', 'Cudgel', 'Dagger'
                           'Belt', 'Ring', 'Gloves', 'Mantle', 'Boots'
                           'Armor', 'Helmet', 'Pants', 'Necklace', 'Mask']


def main() -> None:
    arena: Arena = Arena(races, names, things_names)
    fighters: List[Character] = arena.character_selection_and_presentation()
    arena.fight(fighters)


if __name__ == '__main__':
    main()
    answer: str = input(Fore.RESET + 'Wanna play again? (y/n) ')
    while answer.lower() == 'y':
        main()
        answer: str = input(Fore.RESET + 'Wanna play again? (y/n) ')
