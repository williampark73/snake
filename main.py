from snake_game import SnakeGame
from human_agent import human_agent
from manhattan_agent import manhattan_agent

def play_snake_game(agent_one, agent_two):
	game = SnakeGame(board_size = (20, 60))
	state = game.start_state()
	game.print_board(state)

	while True:
		action = agent_one(game, state)
		state = game.successor(state, action)
		game.print_board(state)
		if game.is_end(state)[0] == True:
			break

		action = agent_two(game, state)
		state = game.successor(state, action)
		game.print_board(state)
		if game.is_end(state)[0] == True:
			break

	result = game.is_end(state)
	if result[1] == 0:
		print("Tie game")
	elif result[1] == 1:
		print("Agent 2 wins")
	else:
		print("Agent 1 wins")
	if state[5] == 0:
		print("Agent 1 score: " + str(result[2]))
		print("Agent 2 score: " + str(result[3]))
	else:
		print("Agent 1 score: " + str(result[3]))
		print("Agent 2 score: " + str(result[2]))
	print("Agent 1 score: " + str(state[3][0]))
	print("Agent 2 score: " + str(state[3][1]))


play_snake_game(manhattan_agent, human_agent)
