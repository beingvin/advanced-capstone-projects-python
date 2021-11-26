from turtle import *
import keyboard, random, math
from time import sleep

############################# CONSTANT VARIABLES  ####

BLOCK_COLOR_ROW_LEN = 0
BLOCK_PLACE_X = 0 
BLOCK_PLACE_Y = 0 
BLOCKS = 0
LIVES = 3
ALIVE_BLOCKES_INT = 0
RESET = 0
PREV_X = 0
PREV_Y = 0
NEW_X = 0
NEW_Y = 0
BALL_X = 0

PADDLE_DIR = 135
PADDLE_X_RIGHT = 0
PADDLE_X_LEFT = 0

BLOCK_POS = [(-350,250), (-250,250), (-150,250), (-50,250), (50,250), (150,250), (250,250), (350,250),
             (-350,210), (-250,210), (-150,210), (-50,210), (50,210), (150,210), (250,210), (350,210),
             (-350,170), (-250,170), (-150,170), (-50,170), (50,170), (150,170), (250,170), (350,170),
             (-350,130), (-250,130), (-150,130), (-50,130), (50,130), (150,130), (250,130), (350,130),
             (-350,90), (-250,90), (-150,90), (-50,90), (50,90), (150,90), (250,90), (350,90)]

BLOCK_DEFULT = [True, True, True, True, True, True, True, True,
                 True, True, True, True, True, True, True, True,
                 True, True, True, True, True, True, True, True,
                 True, True, True, True, True, True, True, True,
                 True, True, True, True, True, True, True, True]

BLOCK_Y = [250, 250, 250, 250, 250, 250, 250, 250,
           210, 210, 210, 210, 210, 210, 210, 210,
           170, 170, 170, 170, 170, 170, 170, 170,
           130, 130, 130, 130, 130, 130, 130, 130,
           90, 90, 90, 90, 90, 90, 90, 90]

BLOCK_X = [-350, -250, -150, -50, 50, 150, 250, 350,
           -350, -250, -150, -50, 50, 150, 250, 350,
           -350, -250, -150, -50, 50, 150, 250, 350,
           -350, -250, -150, -50, 50, 150, 250, 350,
           -350, -250, -150, -50, 50, 150, 250, 350]

BLOCK_COLOR_ROW = [8, 8, 8, 8, 8]
BLOCK_COLOR = ['red', 'orange', 'yellow', 'green', 'blue']
BLOCK_COLOR_CUR = []
BLOCK_ALIVE = []

BLOCKS = len(BLOCK_POS)


############################# SETUP SCREEN ####

ht()
screen = Screen()
screen.setup(800, 700)
screen.bgcolor("black")
screen.title("Breakout | Game")


############################# FUNCTION ####

def block(Turtle, Color):
    Block_place_X = Turtle.xcor() - 40
    BLock_place_Y = Turtle.ycor() - 10

    Turtle.goto(Block_place_X, BLock_place_Y)
    Turtle.color(Color)
    Turtle.begin_fill()
    Turtle.pd()

    Turtle.goto(Block_place_X, BLock_place_Y + 20)
    Turtle.goto(Block_place_X + 80, BLock_place_Y + 20)
    Turtle.goto(Block_place_X + 80, BLock_place_Y)
    Turtle.goto(Block_place_X, BLock_place_Y)

    Turtle.end_fill()
    Turtle.pu()
    Turtle.goto(Block_place_X + (Block_place_X / 2), BLock_place_Y + (BLock_place_Y/2))

def New(Turtle):
    global BLOCK_POS, block, BLOCK_COLOR, BLOCK_COLOR_ROW_LEN, BLOCK_COLOR_CUR, BLOCK_DEFULT, BLOCK_ALIVE, BLOCKS

    Turtle.clear()

    BLOCK_COLOR_ROW_LEN = len(BLOCK_COLOR_ROW)
    BLOCK_COLOR_CUR = []
    BLOCK_ALIVE = BLOCK_DEFULT

    for i in range(BLOCK_COLOR_ROW_LEN):
        for x in range(BLOCK_COLOR_ROW[i]):
            BLOCK_COLOR_CUR.append(BLOCK_COLOR[i])
    
    for i in range(BLOCKS):
        Turtle.goto(BLOCK_POS[i])
        block(Turtle, BLOCK_COLOR_CUR[i])
    
block_creator = Turtle()
block_creator.color('black')
block_creator.pu()
block_creator.speed(1000)
block_creator.goto(0, 0)
block_creator.hideturtle()

paddle = Turtle()
paddle.color('grey')
paddle.pu()
paddle.speed(1000)
paddle.goto(0, -300)
paddle.shape('square')
paddle.shapesize(stretch_wid=1, stretch_len=8, outline=None)

ball = Turtle()
ball.color('white')
ball.pu()
ball.speed(1000)
ball.goto(0, 0)
ball.shape("circle")

New(block_creator)

ball.setheading(270)

while True:
    PREV_X = round(ball.xcor())
    PREV_Y = round(ball.ycor())

    ball.fd(8)

    NEW_X = round(ball.xcor())
    NEW_Y = round(ball.ycor())

    if keyboard.is_pressed('a') or keyboard.is_pressed('left') and not paddle.xcor() < -350:
        paddle.bk(8)
    elif keyboard.is_pressed('d') or keyboard.is_pressed('right') and paddle.xcor() < -340:
        paddle.fd(8)
    if keyboard.is_pressed('d') or keyboard.is_pressed('right') and not paddle.xcor() > 350:
        paddle.fd(8)
    elif keyboard.is_pressed('a') or keyboard.is_pressed('left') and paddle.xcor() > 340:  
        paddle.bk(8)

    if keyboard.is_pressed('Esc'):
        bye()
        break

    if keyboard.is_pressed('space'):
        ball.goto(random.choice(BLOCK_POS))

    if (round(ball.ycor()) <= paddle.ycor() and round(ball.ycor()) >= paddle.ycor() - 4):
        PADDLE_X_RIGHT = round(paddle.xcor())
        PADDLE_X_RIGHT += 90

        PADDLE_X_LEFT = round(paddle.xcor())
        PADDLE_X_LEFT -= 90

        BALL_X = round(ball.xcor())
    
        PADDLE_DIR = 135

        for i in range(PADDLE_X_LEFT, PADDLE_X_RIGHT):

            PADDLE_DIR -= .5

            if (int(round(BALL_X)) == int(round(i))):
                ball.setheading(PADDLE_DIR + 0.5)
                break

    if (round(ball.ycor()) >= 80 ):
        for i in range(BLOCKS):
            for a in range (BLOCK_X[i] - 50, BLOCK_X[i] + 50):
                if (round(ball.xcor()) == a):
                    for f in range(BLOCK_Y[i] - 25, BLOCK_Y[i] + 25):
                        if(round(ball.ycor()) == f):
                            if(BLOCK_ALIVE[i] == True):
                                BLOCK_ALIVE[i] = False
                                block_creator.goto(BLOCK_POS[i])
                                block(block_creator, 'black')
                                ball.sety(ball.ycor() + 0.01)
                                ball.sety(ball.ycor() - 0.01)
                                ball.seth(-ball.heading())
    
    if(ball.ycor() < -370):
        if (LIVES >= 1 and LIVES != 0):
            LIVES -= 1 
            ball.seth(270)
            ball.goto(0, 0)
            paddle.setx(0)
            for i in range(3):
                ball.color('red')
                sleep(0.2)
                ball.color('white')
                sleep(0.2)

        if (LIVES == 0):
            ball.seth(270)
            ball.goto(0, 0)
            paddle.setx(0)
            ball.color('red')
            sleep(2)

    if (LIVES <= 0 or RESET > 3):
        bye()
        break


    if (round(ball.ycor()) >= 330):
        ball.seth(-ball.heading())

    if (round(ball.xcor()) >= 400 or round(ball.xcor()) <= -400):
        ball.seth(-ball.heading() + 180)
    
    ALIVE_BLOCKES_INT = 0

    for i in range(BLOCKS):
        if(BLOCK_ALIVE[i] == False):
            ALIVE_BLOCKES_INT +=1
    
    if(ALIVE_BLOCKES_INT == 40):
        RESET += 1 
        New(block_creator)
        ball.goto(0, 0)
        ball.seth(270)
        paddle.setx(0)
        BLOCK_ALIVE = BLOCK_DEFULT
    










# ############################# exit screen ####
# screen.exitonclick()

