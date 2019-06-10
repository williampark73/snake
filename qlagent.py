from snake_game import SnakeGame
from human_agent import human_agent
from manhattan_agent import manhattan_agent
from minimax_agent import *
import math
import curses
import collections

numIters = 1

explorationProb = 0.5
numFeatures = 6
weights = [0 for _ in range(numFeatures)]
discount = 1
stepSize = 1e-3/float(numIters)

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
	if loc[0] == 0 or loc[0] == game.board_size[0] - 1 or loc[1] == 0 or loc[1] == game.board_size[1] - 1:
		return 1

	# If snake runs into itself
	if loc in snake[1:]:
		return 1

	# If snake runs into the other snake
	if loc in other_snake[1:]:
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
	#state[0].addstr(24, 2, ' Coords: ' + str([up, down, right, left]) + '')
	#state[0].addstr(25, 2, ' Snake: ' + str(snake) + '')
	#state[0].addstr(26, 2, ' Other Snake: ' + str(other_snake) + '')
	state[0].addstr(23, 2, ' F: ' + str(features) + '')
	state[0].addstr(24, 2, ' W: ' + str(weights) + '')

	#features.append((score, 1.))

	return features


def incorporateFeedback(game, state, action, reward, newState):
	if newState is None:
		return

	phi = featureExtractor(game, state, action)

	pred = 0
	for i in range(numFeatures):
		pred += weights[i] * phi[i]

	'''try:
	'''
	current_dir = newState[2][newState[5]-1]
	actions = get_valid(current_dir, game.actions())
	'''
<<<<<<< HEAD
		v_opt = max(evaluation(newState, new_action) for new_action in get_QL_action(newState, actions))
=======
		v_opt = evaluation(game, newState, get_QL_action(game, newState, actions))
>>>>>>> 66bac6dd2e64a262dfaa19b987e2df48d0764d94
	except:
		v_opt = 0.'''

	#v_opt = evaluation(game, newState, get_QL_Action(game, newState, actions))
	#v_opt = 0
	
	v_opt = -float('inf')
	for new_action in actions:
		total = 0
		for i in range(numFeatures):
			total += weights[i] * phi[i]
		if total > v_opt:
			v_opt = total
	
	target = reward + discount * v_opt
	state[0].addstr(31, 10, ' Diff: ' + str(pred - target) + '    ')

	for i in range(numFeatures):
		weights[i] -= stepSize * (pred - target) * phi[i]


def train(num_trials=100, test_runs=10):

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
				state[0].addstr(39, 10, ' Hi: ' + str(reward) + '     ')
				while True:
					x = 3
				break
			game.print_board(state)

			current_dir = state[2][1]
			actions = get_valid(current_dir, game.actions())

			action = get_QL_Action(game, state, actions)

			succ = game.successor(state, action)

			snake = succ[1][1]
			food = state[4]

			reward = succ[3][1] - state[3][1]
			result = game.is_end(succ)
			if result[0] == True:
				while True:
					x = 3
				reward = result[2] - state[3][1]
				#reward = -(abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1]))
				state[0].addstr(39, 10, ' Reward: ' + str(reward) + '     ')
			#reward = 10
			state[0].addstr(28, 10, ' Reward: ' + str(reward) + '     ')
			state[0].addstr(29, 10, ' ScoreNow: ' + str(succ[3][1]) + '     ')
			state[0].addstr(30, 10, ' ScorePrev: ' + str(state[3][1]) + '    ')

			incorporateFeedback(game, state, action, reward, succ)

			game.print_board(state)
			
			if game.is_end(succ)[0] == True:
				game.print_board(state)

				break

			state = succ

		global explorationProb
		explorationProb = explorationProb/2


	explorationProb = 0
	for trial in range(test_runs):
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

			reward = succ[3][1] - state[3][1]

			state = succ
			if game.is_end(state)[0] == True:
				break
			#game.print_board(state)

		score1 += state[3][0]
		score2 += state[3][1]

		result = game.is_end(state)

		if result[1] == 0:
			print("Tie game")
		elif result[1] == 1:
			#print("Agent 2 wins")
			player2 += 1
		else:
			#print("Agent 1 wins")
			player1 +=1


	curses.endwin()
	print("Minimax avg score: " + str(score1/test_runs))
	print("DQN avg score: " + str(score2/test_runs))
	print("Minimax wins: " + str(player1))
	print("DQN wins: " + str(player2))
	'''
#play_snake_game(minimax_agent_first_index, minimax_agent_second_index)
'''
train()
