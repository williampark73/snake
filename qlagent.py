from snake_game import SnakeGame
from human_agent import human_agent
from manhattan_agent import manhattan_agent
from minimax_agent import *
import math
import curses
import collections

numIters = 0

explorationProb = 0.2
weights = [0, 0]
discount = 1
stepSize = 0.001

def get_valid(current_dir, actions):
	if current_dir == KEY_RIGHT:
		remove = KEY_LEFT
	elif current_dir == KEY_LEFT:
		remove = KEY_RIGHT
	elif current_dir == KEY_UP:
		remove = KEY_DOWN
	elif current_dir == KEY_DOWN:
		remove = KEY_UP
	actions.remove(remove)
	return actions

def evaluation(game, state, action):
		score = 0

		phi = featureExtractor(game, state, action)
		for i in range(2):
			score += weights[i] * phi[i][0]
		return score

def get_QL_Action(game, state, actions):
	global numIters
	numIters += 1

	if random.random() < explorationProb:
		return random.choice(actions)
	else:
		return max((evaluation(game, state, action), action) for action in actions)[1]

def featureExtractor(game, state, action):

	player = state[5]
	snake = state[1][player-1]

	nextState = game.successor(state, action, False)

	snake = nextState[1][1]
	food = state[4]

	features = []
	x_dist = snake[0][0] - food[0]
	y_dist = snake[0][1] - food[1]
	score = state[3][player - 1]

	features.append((x_dist, 1.))
	features.append((y_dist, 1.))
	features.append((score, 1.))

	return features


def incorporateFeedback(game, state, action, reward, newState):
	if newState is None:
		return

	phi = featureExtractor(game, state, action)

	pred = 0

	for i in range(2):
		pred += weights[i] * phi[i][0]

	'''try:
		current_dir = newState[2][newState[5]-1]
		actions = get_valid(current_dir, game.actions())
<<<<<<< HEAD
		v_opt = max(evaluation(newState, new_action) for new_action in get_QL_action(newState, actions))
=======
		v_opt = evaluation(game, newState, get_QL_action(game, newState, actions))
>>>>>>> 66bac6dd2e64a262dfaa19b987e2df48d0764d94
	except:
		v_opt = 0.'''

	target = reward #+ discount * v_opt

	for i in range(2):
		weights[i] = weights[i] - stepSize * (pred - target) * phi[i][0]


def train(num_trials=100, max_iter=1000):
	for trial in range(num_trials):

		game = SnakeGame(board_size = (20, 25))
		state = game.start_state()
		game.print_board(state)

		while True:
			action = minimax_agent_first_index(game, state)
			state = game.successor(state, action, True)

			if game.is_end(state)[0] == True:
				break
			game.print_board(state)

			current_dir = state[2][state[5]-1]
			actions = get_valid(current_dir, game.actions())

			action = get_QL_Action(game, state, actions)

			succ = game.successor(state, action)

			snake = succ[1][1]
			food = state[4]

			reward = (snake[0][0] - food[0])**2 + (snake[0][1] - food[1])**2

			state[0].addstr(0, 10, ' Weights: ' + str(weights) + '')

			incorporateFeedback(game, state, action, reward, succ)

			state = succ
			'''
			if game.is_end(state)[0] == True:
				break
			game.print_board(state)
			'''

#play_snake_game(minimax_agent_first_index, minimax_agent_second_index)
train()
