import neat
import multiprocessing
from game_engine import GameEngine
from model.ai_players.random_player import RandomPlayer
from model.ai_players.nn_player import NeuralNetworkPlayer

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game_engine = GameEngine([NeuralNetworkPlayer("NN Player", net),RandomPlayer("Random Player 1"), RandomPlayer("Random Player 2"), RandomPlayer("Random Player 3")])
    fitness = game_engine.play_game()
    return fitness
    # # Initialize your game environment here
    # for _ in range(number_of_games_per_genome):
    #     # Reset your game environment and run a game with this genome
    #     # Use the neural network to make decisions based on the game state
    #     # Update fitness based on the outcome of the game
    #     return fitness


# def eval_genomes(genomes, config):
#     for genome_id, genome in genomes:
#         genome.fitness = eval_genome(genome, config)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = eval_genome(genome, config)
        
