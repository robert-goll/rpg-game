import copy
from utils import *
from entity import *
from random import choice


# Types of events to consider:
# 1) DIalouge = interactions with NPCS
# 2) Combat  = turn based exchange of rolls and challenges
# 3) Skill Checks = i.e. climbing cliff swimming a raging river 


# ACTION_FUNCTIONS[action](combatant,target,battlefield,gear=None)
def combat_encounter(friendly,hostile):
    friendly.extend(hostile)
    all_combatants = friendly
    initiative_order = combat_build_initiative(all_combatants)
    for h in hostile:
        friendly.remove(h)
    battlefield = {
        "FRIENDLY": {
            "SHORT": [],
            "FAR":[]
        },
        "HOSTILE":{
            "SHORT": [],
            "FAR":[]
        }
    }
    battlefield["FRIENDLY"]["FAR"].extend(friendly)
    battlefield["HOSTILE"]["FAR"].extend(hostile)
    done = False
    status = None
    while not done:
        for combatant in initiative_order:
            show_initiative(initiative_order,combatant)
            show_battlefield(initiative_order,battlefield)
            if isinstance(combatant, Player):  # <class 'entity.Player'>:
                action = combat_action_menu(combatant)
                target = combat_target_menu(combatant,initiative_order)
                temp_action = action.split('-')
                gear = None
                if len(temp_action) > 1:
                    gear_description = temp_action[1]
                    for item in combatant.character_gear["COMBAT"]:
                        if item.description == gear_description:
                            gear = item
                            break
                action = temp_action[0]
                ACTION_FUNCTIONS[action](combatant,target,friendly,hostile,battlefield,gear)
            else:
                action = "ATTACK"
                target = choice(friendly)
                temp_action = action.split('-')
                gear = combatant.character_gear["COMBAT"][0]
                ACTION_FUNCTIONS[action](combatant,target,friendly,hostile,battlefield,gear)
            input("...press enter to continue...")
            combat_cleanup(initiative_order,friendly,hostile)
            status = combat_check_resolve(friendly,hostile)
            if status != "continue":
                done = True
                break
    if status == "player_won":
        return True
    else:
        return False
                

def combat_target_menu(player,targets):
    valid = False
    target= None
    while not valid:
        for i in range(len(targets)):
            if targets[i].character_name != "": 
                print(f"{i+1}) {targets[i].character_name}")
            elif targets[i].description != "":
                print(f"{i+1}) {targets[i].description}")
            else:
                print(f"{i+1}) <GENERIC ENTITY>")
        userInput = input(":> ")
        if userInput.isdecimal() and 1 <= int(userInput) <= len(targets):
            valid = True
            target = targets[int(userInput)-1]
        else:
            print(f"Invalid Input, please enter a number between 1 and {len(targets)}")
    return target
    
    
 #TODO - we need to finish this function: it is a copy-paste of combat_target_menu
def combat_action_menu(player):
    valid = False
    action= None
    actions = []
    actions.extend(player.combat_actions)
    if len(player.character_gear["COMBAT"]) > 0:
        for item in player.character_gear["COMBAT"]:
            for act in item.actions:
                actions.append(act + "-" +item.description)
    while not valid:
        for i in range(len(actions)):
            print(f"{i+1}) {actions[i]}")
        userInput = input(":> ")
        if userInput.isdecimal() and 1 <= int(userInput) <= len(actions):
            valid = True
            action = actions[int(userInput)-1]
        else:
            print(f"Invalid Input, please enter a number between 1 and {len(actions)}")
    return action
       

       
''' combat actions:
        attack<specific weapon> 
'''


def combat_build_initiative(args):
    initiative_order = []
#TODO - Error looks to be caused by args being None;
# we should check the resolve of requirment to make sure 
# something is getting passed into combat_encounter
#
# also lets double check the build_enemies function is
# actually creating and returning the NPC objects properly
    for combatant in args:
        i = combatant.getInitiative()
        index = 0
        for index in range(len(initiative_order)):
            if initiative_order[index][0] <= i:
                break
        initiative_order.insert(index, (i, combatant))
    for i in range(len(initiative_order)):
        initiative_order[i] = initiative_order[i][1]
    return initiative_order

    
def combat_action_move(combatant, target, friendly, hostile, battlefield, gear):
    if combatant in battlefield["FRIENDLY"]["SHORT"]:
        battlefield["FRIENDLY"]["SHORT"].remove(combatant)
        battlefield["FRIENDLY"]["FAR"].append(combatant)
    elif combatant in battlefield["FRIENDLY"]["FAR"]:
        battlefield["FRIENDLY"]["FAR"].remove(combatant)
        battlefield["FRIENDLY"]["SHORT"].append(combatant)
    elif combatant in battlefield["HOSTILE"]["SHORT"]:
        battlefield["HOSTILE"]["SHORT"].remove(combatant)
        battlefield["HOSTILE"]["FAR"].append(combatant)
    elif combatant in battlefield["HOSTILE"]["FAR"]:
        battlefield["HOSTILE"]["FAR"].remove(combatant)
        battlefield["HOSTILE"]["SHORT"].append(combatant)
        
def combat_action_attack(combatant, target, friendly, hostile, battlefield, gear):
    relation = None
    if combatant in friendly and target in friendly:
        relation = 0
    elif combatant in hostile and target in hostile:
        relation = 1
    elif combatant in friendly:
        relation = 2
    elif combatant in hostile:
        relation = 3
    
    combatant_pos = None
    target_pos = None
    
    match relation:
        case 0:
            if combatant in battlefield["FRIENDLY"]["SHORT"]:
                combatant_pos = 0
            else:
                combatant_pos = 1
            if target in battlefield["FRIENDLY"]["SHORT"]:
                target_pos = 0
            else:
                target_pos = 1
        case 1:
            if combatant in battlefield["HOSTILE"]["SHORT"]:
                combatant_pos = 2
            else:
                combatant_pos = 3
            if target in battlefield["HOSTILE"]["SHORT"]:
                target_pos = 2
            else:
                target_pos = 3
        case 2:
            if combatant in battlefield["FRIENDLY"]["SHORT"]:
                combatant_pos = 0
            else:
                combatant_pos = 1
            if target in battlefield["HOSTILE"]["SHORT"]:
                target_pos = 2
            else:
                target_pos = 3
        case 3:
            if target in battlefield["FRIENDLY"]["SHORT"]:
                target_pos = 0
            else:
                target_pos = 1
            if combatant in battlefield["HOSTILE"]["SHORT"]:
                combatant_pos = 2
            else:
                combatant_pos = 3
    if abs(combatant_pos-target_pos) > 2:
        if gear.gear_sub_type  == "MELEE":
            print("The attack fails!")
            return           
    else:
        if gear.gear_sub_type == "RANGED":
            print("The attack fails!")
            return
    target_ac = target.getArmorClass()
    attack_mod = None
    if gear.gear_sub_type  == "MELEE":
        attack_mod = combatant.getAttributeModifier("STR")
    else:
        attack_mod = combatant.getAttributeModifier("DEX")
    combatant_attack = rollSum(1,20) + attack_mod + gear.gear_modifier
    if combatant_attack >= target_ac:
        damage = gear.damage.split('d')
        damage = rollSum(int(damage[0]),int(damage[1]))
        target.change_HP(-damage)
        if target.character_name != "": 
            print(f"{target.character_name} was hit for {damage} damage!")
        elif target.description != "":
            print(f"{target.description} was hit for {damage} damage!")
        else:
            print(f"<GENERIC ENTITY> was hit for {damage} damage!")
        
        
# <General description / narrative description>
# 1) Option 1 <STR>
# 2) Option 2 <CHA>
# 3) Fight
#  ...

def combat_cleanup(initiative_order,friendly,hostile):
    dead = []
    for npc in initiative_order:
        if npc.character_currentHP < 1:
            if npc.character_name != "": 
                print(f"{npc.character_name} is dead!")
            elif npc.description != "":
                print(f"{npc.description} is dead!")
            else:
                print(f"<GENERIC ENTITY> is dead!")
            dead.append(npc)
            if npc in friendly:
                friendly.remove(npc)
            else:
                hostile.remove(npc)
    for corpse in dead:
        initiative_order.remove(corpse)


def combat_check_resolve(friendly,hostile):
    if len(friendly) < 1:
        return "player_lost"
    if len(hostile) < 1:
        return "player_won"
    return "continue"
   

def show_initiative(initiative_order,current_npc):
    print(50*'\n')
    print(" -- CURRENT INITIATIVE ORDER -- ")
    count = 1
    for npc in initiative_order:  
        padding = " "
        name_str = ""
        if npc == current_npc:
            padding = ">"
        if npc.character_name != "": 
            name_str = f"{str(count)+' '}{padding} {npc.character_name}"
        elif npc.description != "":
            name_str = f"{str(count)+' '}{padding} {npc.description}"
        else:
            name_str = f"{str(count)+' '}{padding} <GENERIC ENTITY>"
        health_str = f"[{npc.character_currentHP}/{npc.character_totalHP}]"
        print(name_str.ljust(20," "),health_str.rjust(5,' '))
        count += 1
    print(" - - - - - - - - - - - - - - - - ")
    

def show_battlefield(initiative_order,battlefield):
    count = 1
    print("       CURRENT BATTLEFIELD      ")
    print("    FRIENDLY        HOSTILE     ")
    print("  FAR    SHORT    SHORT    FAR  ")
    print(" - - - - - - - - - - - - - - - -")
    for entity in initiative_order:
        f_far   = " "
        f_short = " "
        e_short = " "
        e_far   = " "
        if entity in battlefield["FRIENDLY"]["SHORT"]:
            f_short = str(count)
        elif entity in battlefield["FRIENDLY"]["FAR"]:
            f_far   = str(count)
        elif entity in battlefield["HOSTILE"]["SHORT"]:
            e_short = str(count)
        elif entity in battlefield["HOSTILE"]["FAR"]:
            e_far = str(count)
        count += 1
        print(f"    {f_far}  .  {f_short}    |    {e_short}  .  {e_far}    ")
    print(" - - - - - - - - - - - - - - - -")

   


def combat_action_magic_missile():
  pass

def combat_action_extra_attack():
  pass

def combat_action_acid_splash():
  pass

def list_character_menu():
  pass

def create_character_menu():
  toon = Player()
  # attributes, race, class, skills, feats, equipment, flair
  create_attribute(toon)
  choose_race(toon)
  choose_class(toon)

def create_attribute(toon):
  points = 27
  done = False
  while not done:
    valid = False
    while not valid:
      print("ATTRIBUTE SELECTION")
      print(f"Points Total: {points}")
      print(f"STRENGTH:     {toon.character_attributes['STR']}")
      print(f"DEXTERITY:    {toon.character_attributes['DEX']}")
      print(f"CONSTITUTION: {toon.character_attributes['CON']}")
      print(f"WISDOM:       {toon.character_attributes['WIS']}")
      print(f"INTELIGENCE:  {toon.character_attributes['INT']}")
      print(f"CHARISMA:     {toon.character_attributes['CHA']}")
      print()
      print("Select an action")
      print("1) Increase Attribute")
      print("2) Decrease Attribute")
      print("3) Done")
      menuMode = input(": ")
      if menuMode.isdecimal() and 1 <= int(menuMode) <= 3:
        valid = True
      else:
        print(f"ERROR: '{menuMode}' is not a valid response. Please enter a number 1 - 3")
    if menuMode != "3":
      valid = False
      while not valid:
        print("ATTRIBUTE SELECTION")
        print("1) STRENGTH")
        print("2) DEXTERITY")
        print("3) CONSTITUTION")
        print("4) WISDOM")
        print("5) INTELIGENCE")
        print("6) CHARISMA")
        selAtt = input(": ")
        if selAtt.isdecimal() and 1 <= int(selAtt) <= 6:
          valid = True
        else:
          print(f"ERROR: '{selAtt}' is not a valid response. Please enter a number 1 - 6")
      valid = False
      while not valid:
        print("Please enter a valid Attribute score between 8 - 15:")
        actualAtt = input(": ")
        if actualAtt.isdecimal() and 8 <= int(actualAtt) <= 15:
          valid = True
        else:
          print(f"ERROR: '{actualAtt}' is not a valid response. Please enter a number 8 - 15")
    else:
      actualAtt = 0
      selAtt = None
    pointCost = 0
    actualAtt = int(actualAtt)
    match selAtt:
      case "1":
        selAtt = "STR"
      case "2":
        selAtt = "DEX"
      case "3":
        selAtt = "CON"
      case "4":
        selAtt = "WIS"
      case "5":
        selAtt = "INT"
      case "6":
        selAtt = "CHA"
      case _:
        pass
    match menuMode:
      case "1":
        if actualAtt > toon.character_attributes[selAtt]:
          print("increase stat")
          if actualAtt > 13:
            pointCost += (actualAtt - 13) * 2
          pointCost += (actualAtt  - pointCost//2) - toon.character_attributes[selAtt]
          if pointCost <= points:
            points -= pointCost
            toon.character_attributes[selAtt] = actualAtt
          else:
            print(f"ERROR: The cost to increase {selAtt} to {actualAtt} is too high!")  
        else:
          print(f"ERROR: Please enter a score higher than {toon.character_attributes[selAtt]} for {selAtt}!")

      case "2":
        if actualAtt < toon.character_attributes[selAtt]:
          print("decrease stat")
          if toon.character_attributes[selAtt] > 13:
            pointCost += (toon.character_attributes[selAtt] - 13) * 2
            toon.character_attributes[selAtt] -= (toon.character_attributes[selAtt] - 13)
          pointCost += toon.character_attributes[selAtt] - actualAtt
          points += pointCost
          toon.character_attributes[selAtt] = actualAtt
        else:
          print(f"ERROR: Please enter a score less than {toon.character_attributes} for {selAtt}!")
      case "3":
        if points > 0:
          valid = False
          confirm = None
          while not valid:
            print(f"WARNING: You still have {points} points remaining! Are you sure you're done?")
            print("1) Yes")
            print("2) No")
            confirm = input(": ")
            if confirm.isdecimal() and 1 <= int(confirm) <= 2:
              valid = True
            else:
              print(f"ERROR: '{confirm}' is not a valid response. Please enter a number 1 - 2")
          if confirm == "1":
              done = True
        else:
          done = True

def choose_race(toon):
  done = False
  race_keys = RACES.keys()
  selected_race = None
  while not done:
    valid = False
    while not valid:
      print("RACE SELECTION")
      count = 0
      for k in race_keys:
        count += 1
        print(f"{count}) {RACES[k]['name']}")
      print("Please select your race.")
      userInput = input(": ")
      if userInput.isdecimal() and 1 <= int(userInput) <= count:
        valid = True
        selected_race = k
      else:
        print(f"ERROR: '{userInput}' is not a valid response. Please enter a number 1 - {count}")
    valid = False
    while not valid:
      print("RACE CONFIRMATION")
      print()
      print(f"NAME: {RACES[selected_race]['name']}")
      str = RACES[selected_race]['attributes'][0]
      dex = RACES[selected_race]['attributes'][1]
      con = RACES[selected_race]['attributes'][2]
      inte = RACES[selected_race]['attributes'][3]
      wis = RACES[selected_race]['attributes'][4]
      cha = RACES[selected_race]['attributes'][5]
      print(f"ATTRIBUTES: STR:{str},DEX:{dex},CON:{con},INT:{inte},WIS:{wis},CHA:{cha} ")
      print()
      print("Please confirm your choice.")
      print("1) Yes")
      print("2) No")
      userInput = input(": ")
      if userInput.isdecimal() and 1 <= int(userInput) <= 2:
        valid = True
        done = True
        toon.character_attributes['STR'] += str
        toon.character_attributes['DEX'] += dex
        toon.character_attributes['CON'] += con
        toon.character_attributes['INT'] += inte
        toon.character_attributes['WIS'] += wis
        toon.character_attributes['CHA'] += cha
      else:
        print(f"ERROR: '{userInput}' is not a valid response. Please enter a number 1 - 2")

def choose_class(toon):
  done = False
  class_keys = CLASSES.keys()
  selected_class = None
  while not done:
    valid = False
    while not valid:
      print("CLASS SELECTION")
      count = 0
      for k in class_keys:
        count += 1
        print(f"{count}) {CLASSES[k]['name']}")
      print("Please select your class.")
      userInput = input(": ")
      if userInput.isdecimal() and 1 <= int(userInput) <= count:
        valid = True
        selected_class = k
      else:
        print(f"ERROR: '{userInput}' is not a valid response. Please enter a number 1 - {count}")
    valid = False
    while not valid:
      print("CLASS CONFIRMATION")
      print()
      print(f"NAME: {CLASSES[selected_class]['name']}")
      print()
      print("Please confirm your choice.")
      print("1) Yes")
      print("2) No")
      userInput = input(": ")
      if userInput.isdecimal() and 1 <= int(userInput) <= 2:
        valid = True
        done = True
        toon.character_class.append(selected_class)
        toon.combat_actions.extend(CLASSES[selected_class]["features"]["1"])
      else:
        print(f"ERROR: '{userInput}' is not a valid response. Please enter a number 1 - 2")

ACTION_FUNCTIONS = {
    "MOVE": combat_action_move,
    "INTERACT": lambda : print('OOPS'),
    "EVADE": lambda : print('OOPS'),
    "ASSIT": lambda : print('OOPS'),
    "ATTACK": combat_action_attack,
    "MAGIC MISSILE": combat_action_magic_missile,
    "EXTRA ATTACK": combat_action_extra_attack,
    "ACID SPLASH": combat_action_acid_splash
}