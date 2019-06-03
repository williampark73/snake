from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def manhattan_agent(game, state):
	turn = state[5]
	snake = state[1][turn]
	food = state[4]

	key = None

	if snake[0][0] != food[0]:
		if snake[0][0] > food[0]:
			key = KEY_UP
		else:
			key = KEY_DOWN
	else:
		if snake[0][1] > food[1]:
			key = KEY_LEFT
		elif snake[0][1] < food[1]:
			key = KEY_RIGHT

	return key
