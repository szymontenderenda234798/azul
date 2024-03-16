import neat
import multiprocessing
import sys
import os
import datetime
from neat.parallel import ParallelEvaluator
from neat_package.reporter.custom_reporter import CustomReporter
from game_engine import GameEngine
from model.ai_players.random_player import RandomPlayer
from model.ai_players.nn_player import NeuralNetworkPlayer
from logs.dual_logger import DualLogger

def run(config_file, logging_path):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    custom_reporter = CustomReporter(config_file_name=config_file, directory_path=logging_path)
    p.add_reporter(custom_reporter)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    checkpoint_prefix = os.path.join(custom_reporter.checkpoint_path, "neat-checkpoint-")
    p.add_reporter(neat.Checkpointer(generation_interval=100, time_interval_seconds=None, filename_prefix=checkpoint_prefix))


    num_workers = multiprocessing.cpu_count()
    pe = ParallelEvaluator(num_workers, eval_genome)

    # Run for up to 300 generations.
    winner = p.run(pe.evaluate, 10000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


def run_with_logging(config_file_name):
    now = datetime.datetime.now()
    formatted_now = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    formatted_now = formatted_now.replace(":", "-")
    logging_path = 'C:\\Users\\tende\\Desktop\\azul\\game\\logs'
        
    directory_path = f'{logging_path}\\{formatted_now}'
    os.makedirs(directory_path, exist_ok=True)  # exist_ok=True will not raise an error if the directory already exists
    sys.stdout = DualLogger(directory_path + '\\console_output.txt', mode='w')
    config_path = os.path.join('C:\\Users\\tende\\Desktop\\azul\\game\\neat_package\\config\\', config_file_name)
    try:
        run(config_path, directory_path)
    finally:
        # Reset stdout to its original value
        sys.stdout = sys.__stdout__



def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    number_of_games = 10
    total_fitness = 0
    for _ in range(number_of_games):
        game_engine = GameEngine([NeuralNetworkPlayer("NN Player", net),RandomPlayer("Random Player 1"), RandomPlayer("Random Player 2"), RandomPlayer("Random Player 3")])
        fitness = game_engine.play_game()
        total_fitness += fitness
    average_fitness = total_fitness / number_of_games
    return average_fitness