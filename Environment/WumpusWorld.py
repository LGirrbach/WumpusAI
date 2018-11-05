import random

from Environment.PlainWumpusWorld import PlainWumpusWorld
from Environment.FieldClass import Field


class WumpusWorld(PlainWumpusWorld):
    def __init__(self, n=4):
        super().__init__(n)

        self.performance = 0
        self.WIN_SCORE = 1000
        self.LOSE_SCORE = -1000

        self.environment = [[Field() for _ in range(n)] for _ in range(n)]
        x_gold, y_gold = random.choice(self._fields_without_start)
        x_wumpus, y_wumpus = random.choice(self._fields_without_start)
        # print("Wumpus: ", x_wumpus, y_wumpus)
        self.environment[x_wumpus][y_wumpus].assign_wumpus()
        # print("Gold: ", x_gold, y_gold)
        # print()
        self.environment[x_gold][y_gold].assign_glitter()
        for x_wumpus_neighbor, y_wumpus_neighbour in self.neighbours((x_wumpus, y_wumpus)):
            self.environment[x_wumpus_neighbor][y_wumpus_neighbour].assign_stench()
        for x_field, y_field in self._fields_without_start:
            if random.random() < 0.2:
                self.environment[x_field][y_field].assign_pit()
                for x_field_neighbor, y_field_neighbour in self.neighbours((x_field, y_field)):
                    self.environment[x_field_neighbor][y_field_neighbour].assign_breeze()

        self.possible_action = {action: True for action in self.actions}
        # self.actions = ("forward", "turnright", "turnleft", "grab", "shoot", "climb")

        self.agent_position = (0, 0)
        self.agent_direction = "S"  # Possible: N(orth), E(ast), S(outh), W(est)

        self.scream_pending = False
        self.has_gold = False


    def get_actions(self):
        x, y = self.agent_position
        self.possible_action["grab"] = self.environment[x][y].has_glitter()
        self.possible_action["climb"] = self.agent_position == (0, 0)
        return list([action for action, value in self.possible_action.items() if value])

    def do_action(self, action):
        if action not in self.actions:
            raise NotImplementedError

        self.performance -= 1
        if action.lower() == "forward":
            x_position, y_position = self.agent_position
            x_new, y_new = self._direction_forward_transformations[self.agent_direction](x_position, y_position)
            # print(x_new, y_new, self.environment[x_new][y_new].has_wumpus())
            if (x_new, y_new) in self.neighbours((x_position, y_position)):
                self.agent_position = x_new, y_new
                x_position, y_position = x_new, y_new
            if (self.environment[x_position][y_position].has_pit()
                    or self.environment[x_position][y_position].has_wumpus()):
                self.performance += self.LOSE_SCORE
                return False, self.performance
            else:
                return True, self.performance
        elif action.lower() == "turnright":
            self.agent_direction = self.direction_list[(self.direction_list.index(self.agent_direction) +1 ) % 4]
            return True, self.performance
        elif action.lower() == "turnleft":
            self.agent_direction = self.direction_list[(self.direction_list.index(self.agent_direction) - 1) % 4]
            return True, self.performance
        elif action.lower() == "grab":
            x_position, y_position = self.agent_position
            if self.environment[x_position][y_position].has_glitter():
                self.has_gold = True
                self.environment[x_position][y_position].take_gold()
            return True, self.performance
        elif action.lower() == "shoot":
            if not self.possible_action["shoot"]:
                return True, self.performance
            else:
                self.performance -= 10
                x_arrow, y_arrow = self.agent_position
                print(self.forward_field((x_arrow, y_arrow), self.agent_direction))
                while self.forward_field((x_arrow, y_arrow), self.agent_direction) != (x_arrow, y_arrow):
                    x_arrow, y_arrow = self.forward_field((x_arrow, y_arrow), self.agent_direction)
                    if self.environment[x_arrow][y_arrow].has_wumpus():
                        self.environment[x_arrow][y_arrow].kill_wumpus()
                        self.scream_pending = True
            self.possible_action["shoot"] = False
            return True, self.performance
        elif action.lower() == "climb":
            if self.agent_position == (0, 0):
                if self.has_gold:
                    self.performance += self.WIN_SCORE
                return False, self.performance
            else:
                return True, self.performance

    def get_sensor(self):
        x, y = self.agent_position
        stench, breeze, glitter = self.environment[x][y].get_sensor()
        scream = self.scream_pending
        self.scream_pending = False
        return stench, breeze, glitter, scream


if __name__ == '__main__':
    # random.seed(10)
    pass