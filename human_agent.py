from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def human_agent(game, state):
	actions = game.actions()

	win = state[0]
	turn = state[5]

	key = state[2][turn]

	event = win.getch()
	key = key if event == -1 else event                        # Controls key press

	if key in actions:
		return key

	return state[2][turn]
