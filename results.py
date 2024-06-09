import json

from sklearn.metrics import mean_absolute_error

from iterations_results import plot_results

if __name__ == "__main__":
    with open("org_val.json", "r") as model_file:
        org_val = json.load(model_file)
    with open("best_iter_result.json", "r") as model_file:
        arr = json.load(model_file)
    print(mean_absolute_error(org_val, arr))
    plot_results()
