import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import time

class SnakeGame:
	def __init__(self, board_size = (20, 60), first_to_move = 1):
		self.board_size = boardsize
		self.first_to_move = first_to_move

	def start_state(self):
		curses.initscr()
		win = curses.newwin(self.board_size[0], self.board_size[1], 0, 0)
		win.keypad(1)
		curses.noecho()
		curses.curs_set(0)
		win.border(0)
		win.nodelay(1)

		agent_one_key = KEY_RIGHT
		agent_two_key = KEY_LEFT

		agent_one_score = 100
		agent_two_score = 100

		agent_one_snake = [[4,10], [4,9], [4, 8]]
		agent_two_snake = [[15, 8], [15, 9], [15, 10]]

		food_1 = [10, 20]
		food_2 = [20, 20]

		win.addch(food_1[0], food_1[1], '*')                                   # Prints the food
		win.addch(food_2[0], food_2[1], '*')                                   # Prints the food

		return (win,
			    (agent_one_snake, agent_two_snake), 
			    (agent_one_action, agent_two_action), 
			    (agent_one_score, agent_two_score), 
			    (food_1, food_2), 
			    self.first_to_move
		)

	def actions(self, state):
		return [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN]

	# We will assume the action here is legal
	def successor(self, state, action):
		

	def is_end(self, state):
		raise Exception('Not implemented yet')

	def print_board(self, state):
		win = state[0]
		win.border(0)
    	win.addstr(0, 2, ' P1score: ' + str(state[3][0]) + ' ')                # Printing 'Score' and
    	#win.timeout(150 - (len(agent_one_snake)/5 + len(agent_one_snake)/10)%120)          # Increases the speed of Snake as its length increases

    	win.addstr(self.board_size[0]-1, 2, ' P2score: ' + str(state[3][1]) + ' ')
    	win.timeout(150)


    	win.addstr(0, 45, ' Time : ' + str(int(time.time() - start_time)) + ' ')










