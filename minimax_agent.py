import random
from curses import *
from random import randint

def succ(state, action):
		new_state = list(state)
		key = action
		player = new_state[5]
		snake = new_state[1][player-1]
		snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

		list_snakes = list(new_state[1])
		list_snakes[player-1] = snake
		new_state[1] = tuple(list_snakes)

		list_keys = list(new_state[2])
		list_keys[player-1] = action
		new_state[2] = tuple(list_keys)

		list_scores = list(new_state[3])
		
		food = new_state[4]

		if snake[0] == food:                                            # When snake eats the food
			food = []
			list_scores[player-1] += 100

			while food == []:
				food = [randint(1, 20-2), randint(1, 60-2)]                 # Calculating next food's coordinates
				if food in snake: food = []
			new_state[4] = food
		else:	
			last = snake.pop()                                          # [1] If it does not eat the food, length decreases
			list_scores[player-1] -= 1

		new_state[3] = tuple(list_scores)

		if player == 1:
			new_state[5] = 2
		else:
			new_state[5] = 1

		return tuple(new_state)

def minimax_agent_first_index(game, state):
	return minimax_agent(game, state, 1, 5)


def minimax_agent_second_index(game, state):
	return minimax_agent(game, state, 2, 5)


def minimax_agent(game, state, agent_index, depth):
	win = state[0]



	
	actions = game.actions()
	
	current_dir = state[2][state[5]-1]


		
	
	scores = [minimax_value(game, succ(state, action), agent_index, 3 - agent_index, depth) for action in actions]
	best_score = max(scores)
	best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
	chosen_index = random.choice(best_indices)
	return actions[chosen_index]
	
	'''
	actions = [KEY_UP, KEY_RIGHT]
	return random.choice(actions)
	'''

def minimax_value(game, state, maximizing_agent, agent_index, depth):
	if game.is_end(state)[0]:
		winner = game.is_end(state)[1]
		if winner == 0:
			return 0
		elif winner == maximizing_agent:
			return float('inf')
		else:
			return -float('inf')
		

	#state[0].timeout(150)
	if depth == 0:
		food = state[4]
		snake = state[1][state[5]-1]

		return -((snake[0][0] - food[0])**2 + (snake[0][1] - food[1])**2) # No evaluation function as of now

	actions = game.actions()
	if state[5] == maximizing_agent:
		values = [minimax_value(game, succ(state, action), maximizing_agent, 3 - agent_index, depth - 1) for action in actions]
		return max(values)
	else:
		values = [minimax_value(game, succ(state, action), maximizing_agent, 3 - agent_index, depth - 1) for action in actions]
		return min(values)
