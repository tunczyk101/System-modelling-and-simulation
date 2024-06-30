import json

import deap
#from scipy.optimize import OptimizeResult
import matplotlib.pyplot as plt
from deap import tools


RESULTS_FILE = "./results.txt"


def save_results(population,):
    best_ind = tools.selBest(population, k=1)[0]
    print(f"Best: {best_ind.fitness.values[0]}")
    with open(RESULTS_FILE, "a") as result_file:
        result_file.write(f"{str(best_ind.fitness.values[0])}\n")

    with open("./best_iter_result.txt", "w") as f:
        f.write(str(best_ind))

    try:
        with open("./best_iter_result.json", "w") as f:
            json.dump([float(i) for i in best_ind], f)
    except:
        pass


def save_single_results(best_offspring, save):
    best = best_offspring.fitness.values[0]
    best_genom = list(best_offspring)
    print(f"Best: {best}")
    with open(RESULTS_FILE, "a") as result_file:
        result_file.write(f"{str(best)}\n")

    if save:
        with open("./best_iter_result.txt", "w") as f:
            f.write(str(best_genom))
        try:
            with open("./best_iter_result.json", "w") as f:
                json.dump([float(i) for i in best_genom], f)
        except:
            pass


def plot_results(metric="mae"):
    results_array = []

    with open(RESULTS_FILE) as results_file:
        for line in results_file.readlines():
            if len(line) == 0:
                continue
            results_array.append(float(line.split()[0]))

    plt.plot([i for i in range(len(results_array))], results_array)
    plt.xlabel("Iteration")
    plt.ylabel(metric.upper())
    plt.title("Results")
    plt.savefig("results.png")
    plt.show()

