from snake_game import SnakeGame
from human_agent import human_agent
from manhattan_agent import manhattan_agent
from minimax_agent import *
import math
import curses
import collections

numIters = 1

explorationProb = 0.2
numFeatures = 2
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
	other_snake = nextState[1][0]

	features = []
	x_dist = abs(snake[0][0] - food[0])
	y_dist = abs(snake[0][1] - food[1])
	score = state[3][1]

	features.append((x_dist, 1.))
	features.append((y_dist, 1.))
	#features.append((score, 1.))

	return features


def incorporateFeedback(game, state, action, reward, newState):
	if newState is None:
		return

	phi = featureExtractor(game, state, action)

	pred = 0
	for i in range(numFeatures):
		pred += weights[i] * phi[i][0]

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
	v_opt = 0
	'''
	v_opt = -float('inf')
	for new_action in actions:
		total = 0
		for i in range(numFeatures):
			total += weights[i] * phi[i][0]
		if total > v_opt:
			v_opt = total
	'''
	target = reward + discount * v_opt

	for i in range(numFeatures):
		weights[i] -= stepSize * (pred - target) * phi[i][0]


def train(num_trials=100, max_iter=1000):

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
				break
			game.print_board(state)

			current_dir = state[2][state[5]-1]
			actions = get_valid(current_dir, game.actions())

			action = get_QL_Action(game, state, actions)

			succ = game.successor(state, action)

			snake = succ[1][1]
			food = state[4]
			
			reward = succ[3][1] - state[3][1]
				#reward = -(abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1]))
			#reward = 10
			state[0].addstr(0, 10, ' Weights: ' + str(weights) + '')

			incorporateFeedback(game, state, action, reward, succ)

			state = succ
			'''
			if game.is_end(state)[0] == True:
				break
			game.print_board(state)
		
			'''
		'''
		result = game.is_end(state)
		if result[1] == 0:
			print("Tie game")
		elif result[1] == 1:
			#print("Agent 2 wins")
			player2 += 1
		else:
			#print("Agent 1 wins")
			player1 +=1
	
	print("Minimax wins: " + str(player1))
	print("DQN wins: " + str(player2))
	'''
#play_snake_game(minimax_agent_first_index, minimax_agent_second_index)
train()
