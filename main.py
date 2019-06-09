from snake_game import SnakeGame
from human_agent import human_agent
from manhattan_agent import manhattan_agent
from minimax_agent import *
import curses


def play_snake_game(agent_one, agent_two):

	states = []
	game = SnakeGame(board_size = (20, 40))
	state = game.start_state()
	states.append(state)

	game.print_board(state)

	while True:
		action = agent_one(game, state)
		state = game.successor(state, action, True)
		states.append(state)

		if game.is_end(state)[0] == True:
			break
		game.print_board(state)

		action = agent_two(game, state)
		state = game.successor(state, action, True)
		states.append(state)
		if game.is_end(state)[0] == True:
			break
		game.print_board(state)

	result = game.is_end(state)
	curses.endwin()
	if result[1] == 0:
		print("Tie game")
	elif result[1] == 1:
		print("Agent 2 wins")
	else:
		print("Agent 1 wins")
	if state[5] == 1:
		print("Agent 1 score: " + str(result[2]))
		print("Agent 2 score: " + str(result[3]))
	else:
		print("Agent 1 score: " + str(result[3]))
		print("Agent 2 score: " + str(result[2]))
	'''
	for s in states:
		print(s)
	'''
'''
win1 = 0
for i in range(100):
	win1 += play_snake_game(manhattan_agent, minimax_agent_second_index)
	print(i)

print(win1)
print(win1/500)
'''
play_snake_game(minimax_agent_first_index, minimax_agent_second_index)

