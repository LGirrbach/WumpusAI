from Environment.PlainWumpusWorld import PlainWumpusWorld
from Deprecated.KB2 import KB2
from Logic.OperatorClasses import *
from HelperFunctions import symbol, neighbour_symbols

def init_wumpus_kb(plain_wumpus_world_map):
    wumpus_kb = KB2()
    for coordinates_field in plain_wumpus_world_map.allFields:
        neighbours_field = plain_wumpus_world_map.neighbours(coordinates_field)
        wumpus_symbol = symbol('W', *coordinates_field)
        pit_symbol = symbol('P', *coordinates_field)
        breeze_symbol = symbol('B', *coordinates_field)
        stench_symbol = symbol('S', *coordinates_field)

        wumpus_condition = BiconditionalFormula(
            wumpus_symbol,
            ConjunctionFormula(*neighbour_symbols('S', neighbours_field))
        )
        pit_condition = BiconditionalFormula(
            pit_symbol,
            ConjunctionFormula(*neighbour_symbols('B', neighbours_field))
        )
        breeze_implication = BiconditionalFormula(
            breeze_symbol,
            DisjunctionFormula(*neighbour_symbols('P', neighbours_field))
        )
        stench_implication = BiconditionalFormula(
            stench_symbol,
            DisjunctionFormula(*neighbour_symbols('W', neighbours_field))
        )
        wumpus_kb.tell(wumpus_condition)
        wumpus_kb.tell(pit_condition)
        wumpus_kb.tell(breeze_implication)
        wumpus_kb.tell(stench_implication)
        print('Ein Feld Fertig:', coordinates_field)

    wumpus_kb.tell(NegationFormula(symbol('W', 0, 0)))
    wumpus_kb.tell(NegationFormula(symbol('P', 0, 0)))
    return wumpus_kb

if __name__ == '__main__':
    w = PlainWumpusWorld()
    my_kb = init_wumpus_kb(w)
