import sys
from dnd import *
from test_adventure import *

CURRENT_CHARACTERS = []
player = None

"""
    REMINDERS:
    
    1) Finished adding in the starting equipment for the FIGHTER class
    2) We need to actuall add the equipment to the player toon upon 
        creation.
    3) Introduce a generic purchase system so that the player can make
        decisions about which equipment they want. This can also be used
        in the future to make interactions with vendors more accessible.
"""


def test_story(player):
  nodes = input_story("test_adventure.txt")
  story = build_story(nodes)
  story.resolve(player)

if __name__ == '__main__':
  done = False
  temp = None
  while not done:
    valid = False
    while not valid:
      print("Welcome to DnW!")
      print("1) Load game")
      print("2) New game")
      print("3) Characters")
      print("4) Quit")
      userInput = input(": ")
      if userInput.isdecimal() and 1 <= int(userInput) <= 4:
        valid = True
      else:
        print(f"ERROR: '{userInput}' is not a valid response. Please enter a number 1 - 4")
      match userInput:
        case "1":
          print("option1")
        case "2":
          print("option2")
          if player:
            test_story(player)
          else:
            print("error, make a character first")
        case "3":
          print("option3")
          player = create_character_menu()
        case "4":
          done = True
        case _:
          print("ERROR")
  print("...closing game... thanks for playing...")
      




'''

  #print(nodes)
  player = Player()
  player.character_name = "Zap Branigan"
  player.character_attributes["DEX"] = 15

  gear = Gear()
  gear.gear_type = "ATTR"
  gear.gear_subType = "STR"
  gear.gear_modifier = 20

  player.character_gear[gear.gear_type].append(gear)
  
  gear = Gear()
  gear.gear_type = "ATTR"
  gear.gear_subType = "DEX"
  gear.gear_modifier = 20

  player.character_gear[gear.gear_type].append(gear)
  
  gear = Gear()
  gear.gear_type = "ATTR"
  gear.gear_subType = "WIS"
  gear.gear_modifier = 20

  player.character_gear[gear.gear_type].append(gear)
  
  sword = Weapon()
  sword.description = "Sword of the Thousand Truths"
  sword.gear_type = "COMBAT"
  sword.gear_sub_type = "MELEE"
  sword.damage = "2d20"
  sword.gear_modifier = 3
  
  player.character_gear[sword.gear_type].append(sword)

  # story = build_test_adventure()
  
'''
