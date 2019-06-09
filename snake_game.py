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

		agent_one_snake = ([4,10], [4,9], [4, 8])
		agent_two_snake = ([15, 8], [15, 9], [15, 10])

		food = [randint(1, self.board_size[0]-2), randint(1, self.board_size[1]-2)]

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
	def successor(self, state, action, updateWindow = True):
		                                     # [1] If it does not eat the food, length decreases
		new_state = list(state)
		key = action
		player = new_state[5]
		snake = list(new_state[1][player-1])
		snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

		list_keys = list(new_state[2])
		list_keys[player-1] = action
		new_state[2] = tuple(list_keys)

		list_scores = list(new_state[3])

		food = new_state[4]

		if snake[0] == food:                                            # When snake eats the food
			food = []
			list_scores[player-1] += 100
			while food == []:
				food = [randint(1, self.board_size[0]-2), randint(1, self.board_size[1]-2)]                 # Calculating next food's coordinates
				if food in snake: food = []
			new_state[4] = food
		else:
			last = snake.pop()
			list_scores[player-1] -= 1
			if updateWindow == True:
				win = new_state[0]
				win.addch(last[0], last[1], ' ')

		new_state[3] = tuple(list_scores)

		list_snakes = list(new_state[1])
		list_snakes[player-1] = tuple(snake)
		new_state[1] = tuple(list_snakes)

		if player == 1:
			new_state[5] = 2
		else:
			new_state[5] = 1

		return tuple(new_state)


	def is_end(self, state):
		player = state[5]
		snake = state[1][player-1]
		other_player = 2 if player == 1 else 1
		other_snake = state[1][other_player-1]

		# If snake runs into a boundary
		if snake[0][0] == 0 or snake[0][0] == self.board_size[0] - 1 or snake[0][1] == 0 or snake[0][1] == self.board_size[1] - 1:
			score = state[3][player-1] - 1000
			other_score = state[3][other_player-1]
			if score > other_score:
				return (True, other_player, score, other_score)
			if score < other_score:
				return (True, player, score, other_score)
			else:
				return (True, 0, score, other_score)


		# If snake runs into itself
		if snake[0] in snake[1:]:
			score = state[3][player-1] - 1000
			other_score = state[3][other_player-1]
			if score > other_score:
				return (True, other_player, score, other_score)
			if score < other_score:
				return (True, player, score, other_score)
			else:
				return (True, 0, score, other_score)

		# If snake runs into the other snake
		if snake[0] in other_snake[1:]:
			score = state[3][player-1] - 500
			other_score = state[3][other_player-1]
			if score > other_score:
				return (True, other_player, score, other_score)
			if score < other_score:
				return (True, player, score, other_score)
			else:
				return (True, 0, score, other_score)

		return (False, 0)

	def print_board(self, state):
		win = state[0]
		win.border(0)
		win.addstr(0, 2, ' P1 score: ' + str(state[3][0]) + '')
		#win.timeout(150 - (len(agent_one_snake)/5 + len(agent_one_snake)/10)%120)
		win.addstr(self.board_size[0]-1, 2, ' P2 score: ' + str(state[3][1]) + ' ')
		win.timeout(5)

		agent_one_snake = state[1][0]
		agent_two_snake = state[1][1]

		food = state[4]

		win.addch(food[0], food[1], '*')

		win.addch(agent_one_snake[0][0], agent_one_snake[0][1], '$')
		win.addch(agent_two_snake[0][0], agent_two_snake[0][1], '#')


		win.addstr(0, self.board_size[1] - 12, ' Time : ' + str(int(time.time() - start_time)) + ' ')
