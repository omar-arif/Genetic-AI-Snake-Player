from tkinter import S
from snake_game import *
from copy import copy
import random
import copy
import torch.nn as nn


# Define a neural network architecture for a snake player
class SnakePlayer(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super(SnakePlayer, self).__init__()
        self.input_size = input_size
        self.lin1 = nn.Linear(self.input_size, hidden_size)
        self.lin2 = nn.Linear(hidden_size, hidden_size)
        self.lin3 = nn.Linear(hidden_size, output_size)
        self.tanh = nn.Tanh()
        self.sig = nn.Sigmoid()

        
    def forward(self, x):
        x = self.tanh(self.lin1(x))
        x = self.tanh(self.lin2(x))
        x = self.tanh(self.lin3(x))
        x = self.sig(x)
        #print(x)
        x = torch.argmax(x).item()
        return x

class GeneticPop:
    def __init__(self, pop_size, num_generations, player_size, view_window=5, mutation_prob=0.1, mutation_size=0.2):
        # size of the population
        self.pop_size = pop_size
        # number of generations to explore
        self.num_generations = num_generations
        # size of the window of view that the player has of the board (sould be an odd number)
        self.view_window = view_window
        # number of neurones in each hidden layer of a neural network (1 NN = 1 Player)
        self.player_size = player_size
        # probability of a mutation happening
        self.mutation_prob = mutation_prob
        # how large is the mutation
        self.mutation_size = mutation_size

        self.population = [self.generate_player() for i in range (self.pop_size)]

        self.current_player = None


    def generate_player(self):
        player = SnakePlayer(self.view_window**2, self.player_size, 4) #4 is the number of possible moves
        return player

    # reproduce a population
    def pop_step(self, best_quarter):
        new_gen = []
        # add best (fittest) quarter to the next generation
        for p in best_quarter:
            new_gen.append(p)

        # add a mutated (reproduced) version of the top quarter players
        for p in best_quarter:
            q = self.mutate(p)
            new_gen.append(q)
        
        # fill half of the next generation with randomly initialized players (to avoid local minimas)
        for i in range(self.pop_size//2):
            new_gen.append(self.generate_player)
    


    # mutate a gene (player)
    def mutate(self, player):
        mutated_player = copy.deepcopy(player)
        for k in mutated_player.lin1.weight.data:
            for w in k:
                # introduce a perturbation of mutation_size to the weight in case of a mutation
                if (random.uniform(0,1) < self.mutation_prob):
                    w += random.uniform(-1,1)*self.mutation_size
        return mutated_player

    # do a step for a generation (by calculating fitness which is player score and then reproducing)
    def gen_step(self):
        scores = []
        max_score = 0
        for i in range(self.pop_size):
            self.current_player = self.population[i]
            # create snake game
            game = SnakeGame()
            game.start()
            # compute player score
            score = game.play(self.current_player)
            scores.append(score)
            if score > max_score:
                max_score = score
        print("Max score of this generation is : {}".format(max_score))

        # select top quarter players
        top_index = list(np.argsort(scores))[3*self.pop_size//4:]
        top_quart = [self.population[i] for i in top_index]
        print("Top 25 percent scores:",[scores[i] for i in top_index])
        # update population
        self.pop = self.pop_step(top_quart)

    def evolve(self):
        for i in range(self.num_generations):
            print("Generation number {}".format(i))
            self.gen_step()

    
if __name__ == "__main__":
    population = GeneticPop(view_window=5, pop_size=100, num_generations=100, player_size=16)
    population.evolve()

