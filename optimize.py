import random
import shutil

from deap import creator, base, tools

from iterations_results import save_single_results, RESULTS_FILE, plot_results
from optimize_epanet import optimize_epanet


def check_bounds(minimum, maximum):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in range(len(child)):
                    if child[i] > maximum:
                        child[i] = maximum
                    elif child[i] < minimum:
                        child[i] = minimum
            return offspring

        return wrapper

    return decorator


def main():
    def create_individual():
        return ([toolbox.attr_float() for _ in range(pipes_start, pipes_end)] +
                [toolbox.attr_float2() for _ in range(junctions_start, junctions_end)])

    original_model = "epanet_model/model_original.inp"
    open(RESULTS_FILE, "w").close()  # clean file with results

    with open(original_model) as model_file:
        lines = model_file.readlines()
        junctions_start = lines.index("[EMITTERS]\n") + 2
        junctions_end = lines.index("[QUALITY]\n") - 1
        pipes_start = lines.index("[PIPES]\n") + 2
        pipes_end = lines.index("[PUMPS]\n") - 1

    optimalize_model = "epanet_model/model_optimalize.inp"
    shutil.copyfile(original_model, optimalize_model)

    POPULATION = 10
    MAXITERATIONS = 10000000

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, 0, 6)  # For pipes
    toolbox.register("attr_float2", random.uniform, 0, 1)  # For junctions
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", optimize_epanet)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.5, low=0, up=6, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=5)

    toolbox.decorate("mate", check_bounds(0, 6))
    toolbox.decorate("mutate", check_bounds(0, 6))

    pop = toolbox.population(n=POPULATION)
    mate_probability = 0.5
    mutation_probability = 0.2
    best_offspring_results = 100

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    # Set fitnesses to individuals
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # loop for the number of generation we need
    for g in range(MAXITERATIONS):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < mate_probability:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_probability:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        best_offspring = min(pop, key=lambda x: x.fitness.values)
        save_single_results(best_offspring, best_offspring.fitness.values[0] < best_offspring_results)
        best_offspring_results = min(best_offspring.fitness.values[0], best_offspring_results)

    plot_results()


if __name__ == "__main__":
    main()
