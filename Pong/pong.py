import curses
import random
from time import sleep
dimx = 80
dimy = 24
lives = 2
win = None
score = 0

def updateBall(stdscr, ball, paddle, opaddle):
    global score
    target = None


    
    stdscr.addstr(0, dimx // 2 - 11,
		  "Lives: " + str(lives + 1) + "  Your Score: " + str(score))
    
    
    stdscr.addstr(1, 1,
                  '-' * (dimx - 2))
    stdscr.addstr(22, 1,
		  "-" * (dimx - 2))

    stdscr.addstr(ball['y'], ball['x'], ' ')
    ball['x'] += ball['dx']
    ball['y'] += ball['dy']

    if (ball['y'] == 1 or ball['y'] == dimy - 2):
        ball['dy'] = -ball['dy']
    if (ball['x'] == 1):
        if (ball['y'] in paddle['y']):
            ball['dx'] = -ball['dx']
            score += 1

    if (ball['x'] == (dimx - 3)):
        if (ball['y'] in opaddle['y']):
            ball['dx'] = -ball['dx']
    global win
    if (ball['x'] == 0):
            ball['inPlay'] = 0
            win = "bot"
    if (ball['x'] == (dimx - 2)):
            ball['inPlay'] = 0
            win = "player"
    if (ball['inPlay'] != 0):
        stdscr.addstr(ball['y'], ball['x'], 'O')
    
    updateOPaddle(stdscr, opaddle, ball)
     
    return ball


def updatePaddle(stdscr, paddle):
    oldPaddleY = paddle['y'][:]
    
    try:
        move = stdscr.getch()
        if (move == ord('j') and paddle['y'][0] < dimy - 2):
            for i in range(len(paddle['y'])):
                paddle['y'][i] += 1
        elif (move == ord('k') and paddle['y'][2] > 1):
            for i in range(len(paddle['y'])):
                paddle['y'][i] -= 1
        elif (move == ord('q')):
            quit()
        else:
            pass    
    except curses.error:
        pass
    
    for i in range(len(oldPaddleY)):
        stdscr.addstr(oldPaddleY[i], paddle['x'], " ")
    
    for i in range(len(paddle['y'])):
        stdscr.addstr(paddle['y'][i], paddle['x'], '#')

##########################################################################################
##########################################################################################


def updateOPaddle(stdscr, opaddle, ball):
    oldOPaddleY = opaddle['y'][:]
    
########## GET TARGET ###########
    target = 404
 
    ####  GOING UP  ####
    if ball['dx'] == 1 and ball['dy'] == -1:
        cross = ball['y'] - ((dimx - 3) - ball['x'])
        if cross > 0 and cross < dimy - 1:
            target = cross
        else:
            target = 404

            
####  GOING DOWN  ####
    if ball['dx'] == 1 and ball['dy'] == 1:
        cross = ball['y'] + ((dimx - 3) - ball['x'])
        if cross > 0 and cross < dimy - 1:
            target = cross
        else:
            target = 404


    
    
###########  MOVE  ##############

    if target != 404:

        # moves it down
        if (target > opaddle['y'][1] and opaddle['y'][0] < dimy - 2): 
            for i in range(len(opaddle['y'])):
                opaddle['y'][i] += 1

        #moves it up
        elif (target < opaddle['y'][1] and opaddle['y'][2] > 1):
            for i in range(len(opaddle['y'])):
                opaddle['y'][i] -= 1







    for i in range(len(oldOPaddleY)):
        stdscr.addstr(oldOPaddleY[i], opaddle['x'], " ")

    for i in range(len(opaddle['y'])):
        stdscr.addstr(opaddle['y'][i], opaddle['x'], '#')





def main(stdscr):
    stdscr.clear()
    curses.halfdelay(1)
    curses.curs_set(False) # Turn off the cursor, we won't be needing it.

    ball = {'x':0, 'y':0,                # A dict of attributes about the ball
            'dx':0, 'dy':0,
            'inPlay':0, 'score':0}
    ball['x'] = dimx // 2         # Ball's initial X position.
    ball['y'] = dimy // 2         # Starts at screen center.
    ball['dx'] = random.choice([-1, 1])  # The ball's slope components
    ball['dy'] = random.choice([-1, 1])
    ball['inPlay'] = 1                   # Status of game
    
    paddle = {'x':0, 'y':[0, 0, 0]}      # a dict of attributes about paddle
    paddle['x'] = 0                      # Starting x and y of the paddle
    paddle['y'] = [dimy // 2 + i for i in (1, 0, -1)]
                                         # lowest to highest, visually
    opaddle = {'x':0, 'y':[0,0,0]}
    opaddle['x'] = 78
    opaddle['y'] = [dimy // 2 + i for i in (1, 0, -1)]

    stdscr.addch(ball['y'], ball['x'], 'O')
    updatePaddle(stdscr, paddle)
    updateOPaddle(stdscr, paddle, ball)
    stdscr.refresh()

    while ball['inPlay']:
        ball = updateBall(stdscr, ball, paddle, opaddle)
        updatePaddle(stdscr, paddle)
        stdscr.refresh() 
    
    #global score
    #score = ball['score']
    stdscr.clear()
    curses.cbreak(True) 
    curses.flushinp()
    


def logic():
    global lives
    global win
    global score
    while lives >= 0:
        curses.wrapper(main)
        if win == "bot":
            lives -= 1
    
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 4, "Game Over")
    stdscr.refresh()
    sleep(2)
    stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 7, "Your Score Was: " + str(score))
    stdscr.refresh()
    sleep(1)
    stdscr.addstr(curses.LINES // 2 + 2, curses.COLS // 2 - 20,
            "Press q to quit or any other key to play again")
    stdscr.refresh()
    sleep(1)   
    curses.cbreak(True) 
    curses.flushinp()
    choice = stdscr.getch()
    if choice == ord('q'):
        curses.cbreak(True)
        curses.flushinp()
        curses.endwin()
        quit()
    else:
        score = 0
        lives = 2



while True:
    logic()
    
    
    
    
    	
