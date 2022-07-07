from utils import *

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
        
        
def combat_action_magic_missile(combatant, target, friendly, hostile, battlefield, gear):
    index = combatant.character_class.index("Wizard")
    mod = 3+(combatant.character_level[index]//3)
    damage = rollSum(mod,4) + mod
    target.change_HP(-damage)
    if target.character_name != "": 
        print(f"{target.character_name} was hit for {damage} damage!")
    elif target.description != "":
        print(f"{target.description} was hit for {damage} damage!")
    else:
        print(f"<GENERIC ENTITY> was hit for {damage} damage!")

def combat_action_extra_attack():
  pass

def combat_action_acid_splash():
  pass


# <General description / narrative description>
# 1) Option 1 <STR>
# 2) Option 2 <CHA>
# 3) Fight
#  ...

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