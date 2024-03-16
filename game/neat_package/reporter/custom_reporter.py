import neat
import datetime
import os
import shutil

class CustomReporter(neat.reporting.BaseReporter):
    def __init__(self, directory_path, config_file_name, filename="fitness_stats.csv"):
        self.filename = os.path.join(directory_path, filename)
        self.generation = 0
        # Open the file and write the header line
        with open(self.filename, "w") as f:
            f.write("Generation,AverageFitness\n")

        # Copy the configuration file to the same directory
        config_base_name = os.path.basename(config_file_name)
        config_base_name = os.path.splitext(config_base_name)[0]
        destination_config_path = os.path.join(directory_path, config_base_name)
        shutil.copy(config_file_name, destination_config_path)

        # Save the directory path as an instance variable
        self.directory_path = directory_path
        
        # Create a subdirectory for checkpoints
        self.checkpoint_path = os.path.join(self.directory_path, "checkpoints")
        os.makedirs(self.checkpoint_path, exist_ok=True)

    def post_evaluate(self, config, population, species, best_genome):
        # Calculate average fitness
        avg_fitness = sum([c.fitness for c in population.values()]) / len(population)
        self.generation += 1
        # Append the stats to the file
        with open(self.filename, "a") as f:
            f.write(f"{self.generation},{avg_fitness}\n")