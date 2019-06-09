import random, math, pickle, time
import interface, utils
import numpy as np
from rl import RLAlgorithm
from collections import defaultdict
from utils import progressBar
from copy import deepcopy
from sklearn.neural_network import MLPRegressor

EXPLORATIONPROB = 0.3


class QLearningAlgorithm(RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2, weights = None):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.numIters = 0
        self.rl_type = "qlearning"

        if weights:
            self.weights = defaultdict(float, weights)
        else:
            self.weights = defaultdict(float)

    def __str__(self):
        return "Qlearning"

    def stopExploration(self):
        self.explorationProb = 0

    def exportModel(self):
        return dict(self.weights)

    def evalQ(self, state, action):
        """
        Evaluate Q-function for a given (`state`, `action`)
        """
        score = 0
        for f, v in self.featureExtractor.dictExtractor(state, action):
            score += self.weights[f] * v
        return score


    def getAction(self, state):
        """
        The strategy implemented by this algorithm.
        With probability `explorationProb` take a random action.
        """
        self.numIters += 1
        if len(self.actions(state)) == 0:
            return None

        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.evalQ(state, action), action) for action in self.actions(state))[1]


    def getStepSize(self):
        """
        Get the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)


    def incorporateFeedback(self, state, action, reward, newState):
        if newState is None:
            return

        phi = self.featureExtractor.dictExtractor(state, action)
        pred = sum(self.weights[k] * v for k,v in phi)
        try:
            v_opt = max(self.evalQ(newState, new_a) for new_a in self.actions(newState))
        except:
            v_opt = 0.
        target = reward + self.discount * v_opt
        for k,v in phi:
            self.weights[k] = self.weights[k] - self.getStepSize() * (pred - target) * v
