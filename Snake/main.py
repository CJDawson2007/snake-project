import turtle
import time
import random

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.food_x = x + 100
        self.food_y = 0

        self.pause = 0.1

        self.score = 0
        self.high_score = 0

        self.screen = turtle.Screen()
        self.screen.title("Snake Game | 24/04/2020 Project")
        self.screen.bgcolor("black")
        self.screen.setup(width=590, height=590)
    
        self.lead_snake = turtle.Turtle()
        self.lead_snake.speed(0)
        self.lead_snake.shape("square")
        self.lead_snake.shapesize(1)
        self.lead_snake.color("green")
        self.lead_snake.penup()
        self.lead_snake.goto(self.x, self.y)
        self.lead_snake.direction = "right"
        
        self.snake_pieces = []

        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.shapesize(1)
        self.food.color("red")
        self.food.penup()
        self.food.goto(self.food_x, self.food_y)

        self.score_drawer = turtle.Turtle()
        self.score_drawer.speed(0)
        self.score_drawer.shape("square")
        self.score_drawer.color("white")
        self.score_drawer.penup()
        self.score_drawer.hideturtle()
        self.score_drawer.goto(0, 260)
        self.score_drawer.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")

        self.run()
    def run(self):
        while True:
            self.screen.update()
            print("X:", self.x)
            print("Y:", self.y)
            if(self.x >= 271 or self.x <= -281):
                print("DEAD")
                exit()
            elif(self.y >= 271 or self.y <= -271):
                print("DEAD")
                exit()
            elif(self.lead_snake.distance(self.food) < 20):
                print("NOM!")
                self.food_x = random.randint(-270, 260)
                self.food_y = random.randint(-260, 260)
                self.food.goto(self.food_x, self.food_y)

                self.snake_piece = turtle.Turtle()
                self.snake_piece.speed(0)
                self.snake_piece.shape("square")
                self.snake_piece.shapesize(1)
                self.snake_piece.color("red")
                self.snake_piece.penup()

                self.snake_pieces.append(self.snake_piece)

                self.pause -= 0.001

                self.score += 1

                if self.score > self.high_score:
                    self.high_score = self.score
                
                self.score_drawer.clear()
                self.score_drawer.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 24, "normal")) 

            for i in range(len(self.snake_pieces)-1, 0, -1):
                self.pieces_x = self.snake_pieces[i-1].xcor()
                self.pieces_y = self.snake_pieces[i-1].ycor()
                self.snake_pieces[i].goto(self.pieces_x, self.pieces_y)

            if len(self.snake_pieces) > 0:
                self.pieces_x = self.lead_snake.xcor()
                self.pieces_y = self.lead_snake.ycor()
                self.snake_pieces[0].goto(self.pieces_x,self.pieces_y)

            self.move()

            for piece in self.snake_pieces:
                if piece.distance(self.lead_snake) < 20:
                    time.sleep(1)
                    self.lead_snake.goto(0,0)
                    self.lead_snake.direction="stop"

                    for piece in self.snake_pieces:
                        piece.goto(1000,1000)
                    
                    self.snake_pieces.clear()

                    self.score = 0
                    self.pause = 0.1

                    self.score_drawer.clear()
                    self.score_drawer.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 24, "normal"))
                
            
            
            time.sleep(self.pause)
        self.screen.mainloop()

    def set_direction(self, direction):
        self.lead_snake.direction = direction

    def move(self):
        if self.lead_snake.direction == "up":
            self.y = self.lead_snake.ycor()
            self.lead_snake.sety(self.y+20)
        elif self.lead_snake.direction == "down":
            self.y = self.lead_snake.ycor()
            self.lead_snake.sety(self.y-20)
        elif self.lead_snake.direction == "left":
            self.x = self.lead_snake.xcor()
            self.lead_snake.setx(self.x-20)
        elif self.lead_snake.direction == "right":
            self.x = self.lead_snake.xcor()
            self.lead_snake.setx(self.x+20)

game = Snake(0, 0)