import neat
import multiprocessing
from neat_package.eval import eval_genome, eval_genomes


def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Use the multiprocessing Python library to parallelize evaluation and speed up training
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genomes)
    winner = p.run(pe.evaluate, n=100)  # n is the number of generations

    # Display the winning genome
    print('\nBest genome:\n{!s}'.format(winner))


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(20))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 1000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))