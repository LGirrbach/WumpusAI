from Environment.WumpusWorld import WumpusWorld
from WumpusAgent import Agent

import random

def main():
    random.seed(10)
    wumpus_world = WumpusWorld()
    my_agent = Agent()
    while True:
        print('Turn: {i}'.format(i=my_agent.time))
        print('Perception:', wumpus_world.get_sensor())
        stench, breeze, glitter, scream = wumpus_world.get_sensor()
        agent_position = wumpus_world.agent_position
        agent_direction = wumpus_world.agent_direction
        possible_actions = wumpus_world.get_actions()
        my_agent.perceive(breeze, stench, glitter, scream, agent_position, agent_direction)
        print('Agent Position:', my_agent.position)
        print('Agent Direction:', my_agent.direction)
        print('Possible Actions:', possible_actions)
        action = my_agent.get_action(possible_actions)
        if action not in possible_actions:
            if action == 'exit' or action == 'quit' or action == 'q':
                break
            print('Invalid action!')
            continue
        if action == 'grab' and wumpus_world.environment[my_agent.position[0]][my_agent.position[1]].has_glitter():
            my_agent.have_gold = True
        print('Action:', action)
        res, perf = wumpus_world.do_action(action)
        print('New Position:', wumpus_world.agent_position)
        print('New Direction:', wumpus_world.agent_direction)
        if not res:
            print('Game over')
            print('Score:', perf)
            break
        else:
            pass
            print('Turn ends')
            print('---------------------------------------------')
            print()

def run_with_stats():
    import cProfile, pstats, io
    from pstats import SortKey

    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == '__main__':
    main()
