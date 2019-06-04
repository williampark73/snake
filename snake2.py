# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import time

#max_score = 0
#NUM_ITERATIONS = 1000

#for i in range(NUM_ITERATIONS):
curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                                    # Initializing values
score = 100
start_time = time.time()
prev_time = start_time

manhattan = False
baseline = True

snake = [[1,3], [1,2], [1,1]]                                     # Initial snake co-ordinates
food = [10,20]                                                     # First food co-ordinates

state = 0
counter = 55
height = 0
right = True

win.addch(food[0], food[1], '@')                                   # Prints the food

cur_time = 0

while key != 27:                                                   # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
    win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
    #win.timeout(50 - (len(snake)/5 + len(snake)/10)%120)          # Increases the speed of Snake as its length increases
    if score < -40000:
        win.timeout(50)

    '''
    cur_time = int(time.time() - start_time)
    if cur_time != prev_time:
        prev_time = cur_time
        score -= 1

    '''
    score -= 1

    cur_time += 1

    win.addstr(0, 45, ' Time : ' + str(cur_time) + ' ')

    prevKey = key                                                  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event


    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
        key = prevKey

    if manhattan:
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
    elif baseline:
        if state == 0:
            if right:
                key = KEY_RIGHT
            else:
                key = KEY_LEFT
            counter -= 1
            if counter == 0:
                right = (right == False)
                state = 1
                if height == 17:
                    state = 2
                counter = 57
        elif state == 1:
            height += 1
            key = KEY_DOWN
            state = 0
        else:
            key = KEY_UP
            height -= 1
            if height == 0:
                state = 0


    # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
    # This is taken care of later at [1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

    # Exit if snake crosses the boundaries (Uncomment to enable)
    #if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

    # If snake runs over itself
    if snake[0] in snake[1:]: break


    if snake[0] == food:                                            # When snake eats the food
        food = []
        score += 100
        while food == []:
            food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
            if food in snake: food = []
        win.addch(food[0], food[1], '@')
    else:
        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')
    win.addch(snake[0][0], snake[0][1], 'X')

curses.endwin()
#max_score += score

print("Score: " + str(score) + " Snake length: " + str(len(snake)))
#print("Average Score: " + str(max_score/NUM_ITERATIONS))
