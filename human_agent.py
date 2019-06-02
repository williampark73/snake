"""
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def human_agent(game, state):
	actions = game.actions(state)
	action = None
	player = state[5]
	previous_action = state[2][player-1]
	while action not in actions:
		event = state[0].getch()
		action = previous_action if event == -1 else event
	return action
"""

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def human_agent(game, state):
	actions = game.actions(state)

	win = state[0]

	key = state[2][1]

	event = win.getch()
	key = key if event == -1 else event                            # Controls key press

	if key in actions:
		return key

	return KEY_RIGHT
	