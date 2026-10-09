#!/usr/bin/env python
# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.

# TODO: Uncomment the environment to test your agent in one of these more complex environment
# from turtlepy_enacter import TurtlePyEnacter
# from PetitCatEnacter import PetitCatEnacter
# from turtlesim_enacter import TurtleSimEnacter # requires ROS


class Agent:
    def __init__(self, _valence_table):
        """ Creating our agent """
        self._valence_table = _valence_table
        self._action = None
        self._anticipated_outcome = None
        self._memory_outcome = {0 : 0, 1 : 0}   #outcomes are initialzed at 0 per default
        self._cycle_counter = 0

    def action(self, _outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self._anticipated_outcome) +
                  ", Outcome: " + str(_outcome) +
                  ", Satisfaction: (anticipation: " + str(self._anticipated_outcome == _outcome) +
                  ", valence: " + str(self._valence_table[self._action][_outcome]) + ")")
            self._memory_outcome[self._action] = _outcome

        """ Computing the next action to enact """
        # first row
        if self._action is None:
            self._action = 0
            #self._cycle_counter = 1
        else:
            last_valence = self._valence_table[self._action][_outcome]

            # if agent get bored (he got the same action 3 times in a row) he changes his action 
            if self._cycle_counter >= 3:
                self._action = 1 - self._action
                self._cycle_counter = 1

            # if its valence is negative the agent changes his action
            elif last_valence < 0:
                self._action = 1 - self._action
                self._cycle_counter += 1

            # if not he repeat the same action
            else:
                self._cycle_counter += 1

        # same action make same outcome
        self._anticipated_outcome = self._memory_outcome[self._action]

        return self._action


class Environment1:
    """ In Environment 1, action 0 yields outcome 0, action 1 yields outcome 1 """
    def outcome(self, _action):
        # return int(input("entre 0 1 ou 2"))
        if _action == 0:
            return 0
        else:
            return 1


class Environment2:
    """ In Environment 2, action 0 yields outcome 1, action 1 yields outcome 0 """
    def outcome(self, _action):
        if _action == 0:
            return 1
        else:
            return 0


class Environment3:
    """ Environment 3 yields outcome 1 only when the agent alternates actions 0 and 1 """
    def __init__(self):
        """ Initializing Environment3 """
        self.previous_action = 0

    def outcome(self, _action):
        _outcome = 1
        if _action == self.previous_action:
            _outcome = 0
        self.previous_action = _action
        return _outcome


# TODO Define the valance of interactions (action, outcome)
# valences = [[-1, 1], [-1, 1]]
valences = [[1, -1], [1, -1]]
# TODO Choose an agent
a = Agent(valences)
# TODO Choose an environment
# e = Environment1()
e = Environment2()
# e = Environment3()
# e = TurtlePyEnacter()
# e = TurtleSimEnacter()

if __name__ == '__main__':
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    for i in range(20):
        action = a.action(outcome)
        outcome = e.outcome(action)
