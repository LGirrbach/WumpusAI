# from Logic.AtomClass import Atom
from Logic.OperatorClasses import NegationFormula
# from Logic.OperatorClasses import ConjunctionFormula, DisjunctionFormula
# from Logic.OperatorClasses import ImplicationFormula, BiconditionalFormula
from HelperFunctions import symbol, direction_transformation_plan, distance
from Environment.PlainWumpusWorld import PlainWumpusWorld
from KnowledgeBase.WumpusKB import init_wumpus_kb

from collections import deque


class Agent:
    def __init__(self, n=4):
        self.wumpus_world_map = PlainWumpusWorld(n)
        self.wumpus_alive = True
        self.have_arrow = True
        self.have_gold = False
        self.time = 0
        self.position = (0, 0)
        self.direction = 'S'

        self.visited_fields = [self.position]
        self.not_visited_field = list(self.wumpus_world_map.fieldsWithoutStart)
        self.agenda = deque()
        self.field_is_safe = dict()
        self.field_is_unsafe = dict()

        self.knowledge_base = init_wumpus_kb(self.wumpus_world_map)

    def perceive(self, breeze, stench, glitter, scream, new_position, new_direction):
        self.position = new_position
        self.direction = new_direction
        x_current_position, y_current_position = self.position
        self.visited_fields.append(self.position)

        self.knowledge_base.tell(NegationFormula(symbol('W', x_current_position, y_current_position)))
        self.knowledge_base.tell(NegationFormula(symbol('P', x_current_position, y_current_position)))

        if scream:
            self.wumpus_alive = False
        if glitter:
            self.knowledge_base.tell(symbol('G', x_current_position, y_current_position))
        if stench:
            self.knowledge_base.tell('S'+str(x_current_position)+str(y_current_position))
        if breeze:
            self.knowledge_base.tell('B'+str(x_current_position)+str(y_current_position))

        self.time += 1

    def get_action(self, actions):
        actions = [action.lower() for action in actions]
        x_position, y_position = self.position
        if 'climb' in actions and self.have_gold and self.position == self.wumpus_world_map.EXIT_POSITION:
            return 'climb'
        elif 'grab' in actions and not self.have_gold and \
            self.knowledge_base.ask(symbol('G', x_position, y_position)):
            return 'grab'
        elif self.agenda:
            return self.next_agenda_step()
        elif self.have_gold and self.position != self.wumpus_world_map.EXIT_POSITION:
            path_calculation_successful, self.agenda = self.calculate_secure_path(self.position,
                                                                                  self.wumpus_world_map.EXIT_POSITION)
            if not path_calculation_successful:
                raise EnvironmentError
            # print(self.agenda)
            return self.next_agenda_step()
        elif self.have_arrow and self.face_wumpus():
            self.have_arrow = False
            return 'shoot'
        else:
            # return 'forward'
            return input('Bitte Aktion eingeben:>> ')

    def next_agenda_step(self):
        next_field = self.agenda[0]
        # print(next_field)
        direction_adjustment_necessary, action = self.turn_to_neighbour(next_field)
        # print(direction_adjustment_necessary, action)
        if not direction_adjustment_necessary:
            _ = self.agenda.popleft()
            return 'forward'
        else:
            return action

    def face_wumpus(self):
        next_field_x, next_field_y = self.wumpus_world_map.forward_field(self.position, self.direction)
        if self.knowledge_base.ask(symbol('W', next_field_x, next_field_y)):
            return True
        else:
            return False

    def ask_secure(self, field):
        wumpus_symbol = symbol('W', *field)
        pit_symbol = symbol('P', *field)
        no_wumpus = self.knowledge_base.ask(NegationFormula(wumpus_symbol))
        no_pit = self.knowledge_base.ask(NegationFormula(pit_symbol))
        return no_wumpus and no_pit

    def turn_to_neighbour(self, coords_neighbour):
        if coords_neighbour not in self.wumpus_world_map.neighbours(self.position):
            raise IndexError
        x_position, y_position = self.position
        x_neighbour, y_neighbour = coords_neighbour
        if x_neighbour < x_position:
            neighbour_direction = 'N'
        elif x_neighbour > x_position:
            neighbour_direction = 'S'
        elif y_neighbour > y_position:
            neighbour_direction = 'E'
        else:
            neighbour_direction = 'W'
        return (False, None) if neighbour_direction == self.direction else (
            True, direction_transformation_plan(self.direction, neighbour_direction)[0])


    def calculate_secure_path(self, coords_field1, coords_field2, path=deque()):
        # print(path)
        if coords_field1 == coords_field2:
            return True, path
        next_fields = [neighbour for neighbour in self.wumpus_world_map.neighbours(coords_field1)
                       if neighbour not in path and self.ask_secure(neighbour)]
        if not next_fields:
            return False, path
        else:
            for next_field in sorted(next_fields, key=lambda nf: distance(nf, coords_field2)):
                path.append(next_field)
                res, path = self.calculate_secure_path(next_field, coords_field2, path)
                if res:
                    return res, path
                _ = path.pop()
