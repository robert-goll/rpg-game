from utils import *

class Entity():
    pass


RACES = {
    'human': {
        'name': 'Human',
        'attributes': [1, 1, 1, 1, 1, 1],
        'features': 0
    },
    'elf': {
        'name': 'Elf',
        'attributes': [0, 2, 0, 1, 0, 0],
        'features': 0
    },
    'dwarf': {
        'name': 'Dwarf',
        'attributes': [2, 0, 2, 0, 0, 0],
        'features': 0
    },
    'halfling': {
        'name': 'Halfling',
        'attributes': [0, 2, 1, 0, 0, 0],
        'features': 0
    }
}

CLASSES = {
    'fighter': {
        'name': 'Fighter',
        'features': {
          "1" : ["Second Wind"],
          "3" : ["Extra Attack"],
          "5" : ["Extra Attack"],
          "7" : [],
          "9" : ["Indomitable"],
          "11" : ["Extra Attack"],
          "13" : [],
          "15" : [],
          "17" : [],
          "19" : ["Extra Attack"]
        },
        'hitdie': '1d10'
    },
    'wizard': {
        'name': 'Wizard',
        'features': {
          "1" : ["Magic Missile","Acid Splash"],
          "3" : ["Invisibility"],
          "5" : ["Fireball"],
          "7" : [],
          "9" : [],
          "11" : [],
          "13" : [],
          "15" : [],
          "17" : [],
          "19" : ["Greater Wish"]
        },
        'hitdie': '1d6'
    }
}


# CLASSES FOR ENTITIES
class NPC(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.character_name = ""
        self.description = ""
        self.character_class = [""]
        self.character_level = [0]
        self.character_experience = 0
        self.character_alignment = "TN"
        self.character_race = [""]
        self.character_gender = ""
        self.combat_actions = ["MOVE","INTERACT","EVADE","ASSIST"]
        # TODO - POSSIBLY add taunt in the future

        self.character_attributes = {
            "STR": 8,
            "DEX": 8,
            "CON": 8,
            "INT": 8,
            "WIS": 8,
            "CHA": 8
        }
        self.character_totalHP = 10
        self.character_currentHP = 10

        self.character_skills = {
            "athletics": 0,
            "acrobatics": 0,
            "endurance": 0,
            "knowledge": 0,
            "nature": 0,
            "social": 0
        }

        self.character_gear = {
            "ATTR": [],
            "SKILL": [],
            "ARMOR": [],
            "TRINKET": [],
            "COMBAT": []
        }
        
        self.attack_count = 1
        self.action_count = 1

    def getAttributeModifier(self, attribute):
        return (self.character_attributes[attribute] - 10) // 2

    def getArmorClass(self):
        modifiers = 0
        for armor in self.character_gear["ARMOR"]:
            modifiers += armor.gear_modifier
        for trinket in self.character_gear["TRINKET"]:
            if trinket.gear_subType == "AC":
                modifiers += trinket.gear_modifier
        return 8 + self.getAttributeModifier('DEX') + modifiers

    def getInitiative(self):
        modifiers = 0
        # TODO = update according to the current character_gear dictionary labels; "trinkets"
        for trinket in self.character_gear["TRINKET"]:
            if trinket.gear_subType == "initiative":
                modifiers += trinket.gear_modifier
        return modifiers + rollSum(1, 20)

    def change_attribute(self, attribute, value):
        self.character_attributes[attribute] += value

    def change_skill(self, skill, value):
        self.character_skills[skill] += value

    def change_HP(self, value):
        self.character_currentHP += value

    def change_XP(self, value):
        self.character_experience += value


class Player(NPC):
    def __init__(self):
        NPC.__init__(self)


        #TODO - add a way to provide combat actions with gear
class Gear(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.description = ""
        self.actions = []
        self.value = 0
        self.gear_modifier = 0
        self.gear_type = ""
        self.gear_sub_type = ""
        
class Weapon(Gear):
    def __init__(self):
        super().__init__()
        self.damage = ""
        self.actions.append('ATTACK')

# subtypes: AC, initiative
