import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import time

start_time = time.time()

class SnakeGame:
	def __init__(self, board_size = (20, 60), first_to_move = 1):
		self.board_size = board_size
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

		food = [10, 20]

		win.addch(food[0], food[1], '*')                                   # Prints the food

		return (win,
				(agent_one_snake, agent_two_snake),
				(agent_one_key, agent_two_key),
				(agent_one_score, agent_two_score),
				food,
				self.first_to_move
		)

	def actions(self):
		return [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN]

	# We will assume the action here is legal
	def successor(self, state, action):
		key = action
		turn = state[5]

		snake = state[1][turn]

		snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

		new_state = list(state)

		new_state[1] = list(state[1])
		if snake[0][0] == 0: snake[0][0] = 18
		if snake[0][1] == 0: snake[0][1] = 58
		if snake[0][0] == 19: snake[0][0] = 1
		if snake[0][1] == 59: snake[0][1] = 1

		food = state[4]
		win = state[0]

		if snake[0] == food:                                            # When snake eats the food
			food = []
			#score += 100
			while food == []:
				food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
				if food in snake: food = []
			new_state[4] = food
		else:
			last = snake.pop()                                          # [1] If it does not eat the food, length decreases
			win.addch(last[0], last[1], ' ')

		new_state[1][turn] = snake

		new_state[2] = list(new_state[2])
		new_state[2][turn] = action
		if turn == 1:
			new_state[5] = 0
		else:
			new_state[5] = 1

		return tuple(new_state)
		#raise Exception('Not implemented yet')

	def is_end(self, state):
		return -1

	def print_board(self, state):
		win = state[0]
		win.border(0)
		win.addstr(0, 2, 'P1score: ' + str(state[3][0]) + '')
		#win.timeout(150 - (len(agent_one_snake)/5 + len(agent_one_snake)/10)%120)
		win.addstr(0, 2, 'P2score: ' + str(state[3][1]) + ' ')
		win.timeout(50)

		agent_one_snake = state[1][0]
		agent_two_snake = state[1][1]

		food = state[4]

		win.addch(food[0], food[1], '*')

		win.addch(agent_one_snake[0][0], agent_one_snake[0][1], '#')
		win.addch(agent_two_snake[0][0], agent_two_snake[0][1], '#')


		win.addstr(0, 45, ' Time : ' + str(int(time.time() - start_time)) + ' ')
