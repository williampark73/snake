from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def human_agent(game, state):
	actions = game.actions()

	win = state[0]
	player = state[5]

	prevKey = state[2][player-1]
	key = state[2][player-1]

	event = win.getch()
	key = key if event == -1 else event                        # Controls key press

	if key in actions:
		if key == KEY_RIGHT and prevKey == KEY_LEFT:
			return prevKey
		if key == KEY_LEFT and prevKey == KEY_RIGHT:
			return prevKey
		if key == KEY_UP and prevKey == KEY_DOWN:
			return prevKey
		if key == KEY_DOWN and prevKey == KEY_UP:
			return prevKey
		return key

	return state[2][player-1]
