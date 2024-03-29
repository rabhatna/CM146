#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')


    offensive_plan = Sequence(name='Offensive Strategy')

    offensive_plan_large = Sequence(name='Offenseive Plan Large')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan_large.child_nodes = [largest_fleet_check, attack]

    offensive_plan_near = Sequence(name='Offenseive Plan Near')
    enemy_nearby = Check(enemy_planets_near)
    attack_near = Action(attack_weakest_near_enemy_planet)
    offensive_plan_near.child_nodes = [enemy_nearby, attack_near]

    offensive_plan_aggresive = Sequence(name = 'Agressive Sequence')
    neutral_planet_check = Check(if_no_neutral_planet_available)
    attack_weakest_action = Action(attack_weakest_enemy_planet)
    offensive_plan_aggresive.child_nodes = [neutral_planet_check, attack_weakest_action]

    offensive_plan.child_nodes = [offensive_plan_large, offensive_plan_near]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]



    defensive_sequence = Sequence(name = 'Defense')
    incoming_Attack_check = Check(check_incoming)
    defense_action = Action(defend)
    defensive_sequence.child_nodes = [incoming_Attack_check, defense_action]

    root.child_nodes = [defensive_sequence, offensive_plan, spread_sequence, attack.copy()]

    txt_file = open("Tree_to_string.txt", "w")
    txt_file.write(root.tree_to_string())
    txt_file.close()

    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
