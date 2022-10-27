import random
from time import sleep
from turtle import Screen, Turtle, onkey, onkeypress


SCORE_FILE = r"score.txt"

COLORS = [(255, 26, 26),(0, 172, 230),(0, 179, 0),(255, 255, 0),(255, 102, 0),(255, 26, 102),(204, 102, 255),(0, 0, 255),(255, 153, 102),(153, 255, 153),(77, 166, 255),(255, 153, 153),(204, 0, 204)]

POSITIONS = [[-275, 60], [-275, 100], [-275, 140], [-275, 180], [-275, 220], [-185, 60], [-185, 100], [-185, 140], [-185, 180], [-185, 220], [-95, 60], [-95, 100], [-95, 140], [-95, 180], [-95, 220], [-5, 60], [-5, 100], [-5, 140], [-5, 180], [-5, 220], [85, 60], [85, 100], [85,140], [85, 180], [85, 220], [175, 60], [175, 100], [175, 140], [175, 180], [175, 220],[265, 60], [265, 100], [265, 140], [265, 180], [265, 220]]

print(len(POSITIONS))

BLOCK_HEIGHT = 14
BLOCK_WIDTH = 100
START_X = -275
START_Y = 10
END_Y = 240
BLOCK_WIDTH = 90

#********************************* PADDLE *****************************************#
class Paddle(Turtle):
    def __init__(self) :
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=0.7,stretch_len=5)
        self.color("white")
        self.goto(x=0,y=-230)
        self.chances = 5

    #for moving paddle left
    def goleft(self):
        if(self.xcor()>=-255):
            new_x = self.xcor()-20
            self.goto(y=self.ycor(),x=new_x)
    
    #for moving paddle right
    def goright(self):
        if(self.xcor()<=255):
            new_x = self.xcor()+20
            self.goto(y=self.ycor(),x=new_x)
    


#********************************* SCORE-BOARD *****************************************#
class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.highscore = 0
        self.score = 0
        self.lifes = 5
        self.penup()
        self.color(153, 255, 204)
        self.hideturtle()
        self.update()

    # when ball misses paddle
    def death(self):
        self.lifes -= 1
        self.update()

    def nextlevel(self):
        self.lifes += 1
        self.update()

    # for writing score
    def update(self):
        self.highscore = int(open(SCORE_FILE,mode="r").read())
        self.clear()
        self.goto(0,-100)
        self.write(f"HS:{self.highscore}   LIVES:{self.lifes}  SCORE:{self.score}",align="center",font=("Courier",20,"normal"))

    # for increase score
    def increase(self):
        self.score += 5
        if(self.score>self.highscore):
            with open(SCORE_FILE,mode="w") as file:
                file.write(str(self.score))
        self.update()

    # for refreshing scoreboard
    def refresh(self):
        self.score = 0
        self.lifes = 5
        self.update()


#********************************* BALL *****************************************#
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.ymove = -10
        self.xmove = 10
        self.movespeed = 0.09
        self.goto(0,0)
    
    # for moving ball
    def move(self):
        sleep(self.movespeed)
        self.goto(self.xcor()+self.xmove,self.ycor()+self.ymove)

    def bouncex(self):
        self.xmove *= -1 
    def bouncey(self):
        self.ymove *=-1
    
    def increasespeed(self):
        self.movespeed *= 0.9

    #refresh ball
    def refresh(self):
        self.goto(0,0)
        self.setheading(-45)


#********************************* BLOCK *****************************************#
class Block(Turtle):
    def __init__(self,position):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=0.9,stretch_len=4)
        self.color(random.choice(COLORS))
        self.goto(x=position[0],y=position[1])

    # deleting block
    def destroy(self):
        self.goto(900,900)


#********************************* MULTIPLE_BLOCKS *****************************************#
class Blocks():
    def __init__(self):
        self.numblocks = random.randint(21,35)
        self.positions = random.choices(POSITIONS,weights=[1 for i in POSITIONS],k=self.numblocks)
        self.blocks = []
        self.create()

    #creating blocks
    def create(self):
        for i in self.positions:
            b1 = Block(i)
            self.blocks.append(b1)
        
    #refreshing blocks
    def refresh(self):
        self.numblocks = random.randint(25,35)
        self.positions = random.choices(POSITIONS,weights=[1 for i in POSITIONS],k=self.numblocks)
        self.blocks = []
        self.create()


#********************************* MAIN *****************************************#

# setting up screen
screen = Screen()
screen.setup(width=650,height=500)
screen.bgcolor("black")
screen.title("BreakOut Game")
screen.tracer(0)
screen.colormode(255)

# setting up turtles
padddle = Paddle()
ball = Ball()
blocks = Blocks()
sb = ScoreBoard()


isgameon = True

while isgameon:
    screen.update()
    ball.move()
    
    
    # if all lives lost
    if(sb.lifes==0):
        what = screen.textinput("GAME OVER","Enter c to continue q to quit",)
        if(what.lower()=="q"):
            isgameon=False
            quit()
        else:
            sb.refresh()
            ball.refresh()
            ball.movespeed = 0.08

    screen.listen()
    onkeypress(padddle.goleft,"Left")
    onkeypress(padddle.goright,"Right")


    # when ball collide with block
    if(len(blocks.blocks)!=0):
        for block in blocks.blocks:
            if(abs(block.xcor()-ball.xcor())<=40 and abs(block.ycor()-ball.ycor())<=20):
                ball.bouncey()
                block.destroy()
                blocks.blocks.remove(block)
                sb.increase()    

    # all balls destroyed       
    else:
        sleep(1)
        blocks.refresh()
        ball.refresh()
        ball.increasespeed()
        sb.nextlevel()

    # when hits vertical walls
    if(ball.xcor()>=305 or ball.xcor()<-308):
        ball.bouncex()

    #when hit upper wall
    if(ball.ycor()>=205):
        ball.bouncey()
    if(ball.ycor()>=225):
        ball.refresh()
    
    #when missed by paddle
    if(ball.ycor()<-235):
        sleep(0.5)
        ball.refresh()
        sb.death()
 
    # when hit paddle
    if(ball.ycor()<=-210 and ball.distance(padddle)<50):
        ball.bouncey()

screen.exitonclick()