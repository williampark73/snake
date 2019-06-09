import random
from curses import *
from random import randint


def minimax_agent_first_index(game, state):
	return minimax_agent(game, state, 1, 5)


def minimax_agent_second_index(game, state):
	return minimax_agent(game, state, 2, 5)


def minimax_agent(game, state, agent_index, depth):
	win = state[0]

	actions = game.actions()

	current_dir = state[2][state[5]-1]
	scores = [minimax_value(game, game.successor(state, action, False), agent_index, 3 - agent_index, depth) for action in actions]
	best_score = max(scores)
	best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
	chosen_index = random.choice(best_indices)

	chosen_index = 2

	return random.choice(actions)

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

	#actions = [action for action in game.actions() if game.is_end(game.successor(state, action, False))[0] == False]
	actions = game.actions()
	save_state = state
	if state[5] == maximizing_agent:
		values = [minimax_value(game, game.successor(state, action, False), maximizing_agent, 3 - agent_index, depth - 1) for action in actions]
		state = save_state
		return max(values)
	else:
		values = [minimax_value(game, game.successor(state, action, False), maximizing_agent, 3 - agent_index, depth - 1) for action in actions]
		state = save_state
		return min(values)
