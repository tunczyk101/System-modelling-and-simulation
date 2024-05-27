import json

from scipy.optimize import OptimizeResult
import matplotlib.pyplot as plt


RESULTS_FILE = "./results.txt"


def save_results(intermediate_result: OptimizeResult):
    print(f"Best: {intermediate_result.fun}")
    with open(RESULTS_FILE, "a") as result_file:
        result_file.write(f"{str(intermediate_result.fun)}\n")

    with open("./best_iter_result.txt", "w") as f:
        f.write(str(intermediate_result.x))

    try:
        with open("./best_iter_result.json", "w") as f:
            json.dump([float(i) for i in intermediate_result.x], f)
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

