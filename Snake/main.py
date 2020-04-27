import turtle
import time
import random
import winsound
import pygame
import yaml
import codecs

class Snake:
    def __init__(self, x, y, headcolor, trailcolor, bgcolor, foodcolor):
        self.x = x
        self.y = y
        self.headcolor = headcolor
        self.trailcolor = trailcolor
        self.bgcolor = bgcolor
        self.foodcolor = foodcolor

        self.food_x = x + 100
        self.food_y = 0

        self.high_score_save = {}
        with open("highscore.yml", "r") as hscore:
            high_score_save = yaml.load(hscore, Loader=yaml.FullLoader)

        self.high_score = int(high_score_save["highscore"])

        self.pause = 0.1

        self.score = 0
        self.game_started = False

        self.screen = turtle.Screen()
        self.screen.title("Snake Game | 24/04/2020 Project")
        self.screen.bgcolor(self.bgcolor)
        self.screen.setup(width=590, height=590)
    
        self.lead_snake = turtle.Turtle()
        self.lead_snake.speed(0)
        self.lead_snake.shape("square")
        self.lead_snake.shapesize(1)
        self.lead_snake.color(self.headcolor)
        self.lead_snake.penup()
        self.lead_snake.goto(self.x, self.y)
        self.lead_snake.direction = "right"
        self.lead_snake.hideturtle()
        
        self.snake_pieces = []

        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.shapesize(1)
        self.food.color(foodcolor)
        self.food.penup()
        self.food.goto(self.food_x, self.food_y)
        self.food.hideturtle()

        self.score_drawer = turtle.Turtle()
        self.score_drawer.speed(0)
        self.score_drawer.shape("square")
        self.score_drawer.color("white")
        self.score_drawer.penup()
        self.score_drawer.hideturtle()

        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")
        self.screen.onkeypress(self.start_game, "space")

        pygame.mixer.init()

        self.loading_screen()

    def start_game(self):
        if(self.game_started == False):
            self.game_started = True
            self.score_drawer.clear()
            self.score_drawer.goto(0, 260)
            self.food.showturtle()
            self.lead_snake.showturtle()
            self.score_drawer.write("Score: 0  High Score: {}".format(self.high_score), align="center", font=("Courier", 24, "normal"))
            self.run()
        

    def loading_screen(self):
        self.score_drawer.clear()
        self.score_drawer.goto(0, 0)
        self.score_drawer.write("PRESS SPACE TO START", align="center", font=("Courier", 24, "normal"))
        self.score_drawer.goto(0, 30)
        self.score_drawer.write("SNAKE", align="center", font=("Courier", 24, "normal"))
        self.screen.mainloop()

    def dead(self):
        self.high_score_save["highscore"] = self.high_score
        self.save()
        pygame.mixer.music.load("gameover.wav")
        pygame.mixer.music.play()
        time.sleep(1)
        self.x = 0
        self.y = 0

        self.lead_snake.goto(self.x, self.y)
        self.lead_snake.direction="stop"


        for piece in self.snake_pieces:
            piece.goto(1000,1000)

        self.snake_pieces.clear()

        self.score = 0
        self.pause = 0.1

        self.score_drawer.clear()
        self.score_drawer.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 24, "normal"))
    def run(self):
        while self.game_started:
            self.screen.update()
            print("X:", self.x)
            print("Y:", self.y)
            if(self.x >= 281 or self.x <= -281):
                print("DEAD")
                self.dead()
            elif(self.y >= 271 or self.y <= -271):
                self.dead()
            elif(self.lead_snake.distance(self.food) < 20):
                pygame.mixer.music.load("eat.mp3")
                pygame.mixer.music.play()

                self.food_x = random.randint(-10, 10) * 20
                self.food_y = random.randint(-10, 10) * 20
                self.food.goto(self.food_x, self.food_y)

                self.snake_piece = turtle.Turtle()
                self.snake_piece.speed(0)
                self.snake_piece.shape("square")
                self.snake_piece.shapesize(1)
                self.snake_piece.color(self.trailcolor)
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
                    self.dead()
                
            
            
            time.sleep(self.pause)
        self.screen.mainloop()

    def set_direction(self, direction):
        if(self.game_started):
            self.lead_snake.direction = direction
            winsound.Beep(1000, 75)

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

    def save(self):
        with open("highscore.yml", "w") as sfile:
            data = yaml.dump(self.high_score_save, sfile)

game = Snake(0, 0, "green", "green", "black", "red")