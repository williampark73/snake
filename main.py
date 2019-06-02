from snake_game import SnakeGame

def play_snake_game(agent_one, agent_two):
	game = SnakeGame(board_size = (40, 60))
	print("New Game")
	state = game.start_state()
	game.print_board(state)

	while True:
		action = agent_one(game, state)
		state = game.successor(state, action)
		game.print_board(state)
		if game.is_end(state)[0]:
			break

		action = agent_two(game, state)
		state = game.successor(state, action)
		game.print_board(state)
		if game.is_end(state)[0]:
			break

	result = game.is_end(state)[1]
	if result == 0:
		print("Tie game")
	elif result == 1:
		print("Player 1 wins")
	else:
		print("Player 2 wins")




play_snake_game(human_agent, manhattan_agent)