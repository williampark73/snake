from snake_game import SnakeGame
from human_agent import human_agent
from manhattan_agent import manhattan_agent
from minimax_agent import *
import math
import curses
import collections

numIters = 1

explorationProb = 0.5
numFeatures = 12
weights = [0 for _ in range(numFeatures)]

discount = 1
stepSize = 1e-3

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
		for i in range(numFeatures):
			score += weights[i] * phi[i]
		return score

def get_QL_Action(game, state, actions):
	global numIters
	numIters += 1

	if random.random() < explorationProb:
		return random.choice(actions)
	else:
		return max((evaluation(game, state, action), action) for action in actions)[1]

def isInBounds(game, loc, snake, other_snake):
	# If snake runs into a boundary
	if loc[0] == 1 or loc[0] == game.board_size[0] - 1 or loc[1] == 1 or loc[1] == game.board_size[1] - 1:
		return 1

	# If snake runs into itself
	
	if loc in snake[2:]:
		return 1
	
	# If snake runs into the other snake
	if loc in other_snake[1:]:
		return 1
	return 0

def isInSnake(game, loc, snake, other_snake):
	# If snake runs into the other snake
	if loc in other_snake[1:]:
		return 1
	return 0

def isFood(state, snake):
	food = state[4]
	if snake[0] == food:
		return 1
	return 0

def nearFood(state, snake):
	food = state[4]
	if abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1]) < 4:
		return 1
	return 0

def nearerFood(state, snake):
	food = state[4]
	if abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1]) < 2:
		return 1
	return 0

def featureExtractor(game, state, action):

	nextState = game.successor(state, action, False)

	snake = nextState[1][1]
	food = state[4]
	other_snake = nextState[1][0]

	features = []
	x_dist = abs(snake[0][0] - food[0])
	y_dist = abs(snake[0][1] - food[1])
	score = state[3][1]

	features.append(x_dist)
	features.append(y_dist)

	up = [snake[0][0] - 1, snake[0][1]]
	down = [snake[0][0] + 1, snake[0][1]]
	right = [snake[0][0], snake[0][1] + 1]
	left = [snake[0][0], snake[0][1] - 1]

	features.append(isInBounds(game, up, snake, other_snake))
	features.append(isInBounds(game, down, snake, other_snake))
	features.append(isInBounds(game, right, snake, other_snake))
	features.append(isInBounds(game, left, snake, other_snake))

	features.append(isInSnake(game, up, snake, other_snake))
	features.append(isInSnake(game, down, snake, other_snake))
	features.append(isInSnake(game, right, snake, other_snake))
	features.append(isInSnake(game, left, snake, other_snake))

	features.append(isFood(state, snake))
	features.append(nearFood(state, snake))

	#features.append(nearerFood(state, snake))


	state[0].addstr(23, 2, ' F: ' + str(features) + '')
	state[0].addstr(24, 2, ' W: ' + str(weights) + '')

	return features


def incorporateFeedback(game, state, action, reward, newState):
	if newState is None:
		return

	phi = featureExtractor(game, state, action)

	pred = 0
	for i in range(numFeatures):
		pred += weights[i] * phi[i]

	current_dir = newState[2][newState[5]-1]
	actions = get_valid(current_dir, game.actions())


	#v_opt = evaluation(game, newState, get_QL_Action(game, newState, actions))
	v_opt = 0
	'''
	v_opt = -float('inf')
	for new_action in actions:
		total = 0
		for i in range(numFeatures):
			total += weights[i] * phi[i]
		if total > v_opt:
			v_opt = total
	'''
	target = reward + discount * v_opt
	state[0].addstr(31, 10, ' Diff: ' + str(pred - target) + '    ')

	for i in range(numFeatures):
		weights[i] -= stepSize * (pred - target) * phi[i]



def train(num_trials=40):

	score1 = 0
	score2 = 0
	player1 = 0
	player2 = 0

	for trial in range(num_trials):

		game = SnakeGame(board_size = (20, 25))
		state = game.start_state()
		game.print_board(state)

		while True:
			action = minimax_agent_first_index(game, state)
			state = game.successor(state, action, True)

			if game.is_end(state)[0] == True:

				reward = game.is_end(state)[2] - state[3][1]
				incorporateFeedback(game, state, action, reward, succ)

				break
			game.print_board(state)

			current_dir = state[2][1]
			actions = get_valid(current_dir, game.actions())

			action = get_QL_Action(game, state, actions)

			succ = game.successor(state, action)

			snake = succ[1][1]
			food = state[4]

			reward = succ[3][1] - state[3][1]
			#reward = 100*(succ[3][1]- state[3][1]) -((snake[0][0] - food[0])**2 + (snake[0][1] - food[1])**2)

			result = game.is_end(succ)

			state[0].addstr(28, 10, ' Reward: ' + str(reward) + '     ')
			state[0].addstr(29, 10, ' ScoreNow: ' + str(succ[3][1]) + '     ')
			state[0].addstr(30, 10, ' ScorePrev: ' + str(state[3][1]) + '    ')

			incorporateFeedback(game, state, action, reward, succ)

			game.print_board(state)
			state = succ

			if game.is_end(state)[0] == True:
				break


		global explorationProb
		explorationProb = explorationProb/2



	curses.endwin()

	'''
'''
train()
