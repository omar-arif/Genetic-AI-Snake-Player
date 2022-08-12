# -*- coding: utf-8 -*-
import torch
import numpy as np
from random import randint

class SnakeGame:
    def __init__(self,max_steps=5000, board_width = 12, board_height = 12, gui = False):
        self.score = 0
        self.max_steps = max_steps
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: self.render_init()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0,1) == 0
        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food



    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if self.done == True: print("Over")#self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
        self.check_collisions()
        if self.gui: self.render()
        return self.generate_observations()

    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 0:
            new_point[0] -= 1
        elif key == 1:
            new_point[1] += 1
        elif key == 2:
            new_point[0] += 1
        elif key == 3:
            new_point[1] -= 1
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food


    def end_game(self):
        print("Game Over, Score: ".format(self.score))
        return 
    

    #####################################################################
    #################           added functions          ################
    #####################################################################

    # process a game board to create input por neural network
    def process_input(self, w_size):
        # position of the head of the snake
        head = self.snake[0]
        # coordinates of the positions within the window
        input = [[(head[0]-(w_size//2)+i, head[1]-(w_size//2)+j) for i in range(w_size)] for j in range(w_size)]
        
        for i in range(len(input)):
            # in case a part of the snake's body is in pos
            if (input[i][0]==0) or (input[i][1] == 0) or (input[i][0] == self.board["width"] + 1) or (input[i][1] == self.board["height"] + 1) or (input[i] in self.snake[1:-1]):
                input[i] = -1
            # in case food is in input[i]
            elif input[i] == self.food:
                input[i] = 1
            else:
                input[i] = 0
        return torch.as_tensor(np.array(input), dtype=torch.float32)
    
    def play(self, player):
        num_steps = 0
        while (self.done == False) or (num_steps > self.max_steps):
            state = self.process_input(player.input_size)
            self.step(player(state))
            num_steps += 1
        return self.score
