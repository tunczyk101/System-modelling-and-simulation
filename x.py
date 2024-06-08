import json
from results import ORG_VAL

from sklearn.metrics import mean_absolute_error

if __name__ == "__main__":
    with open("org_val.json", "r") as model_file:
        arr = json.load(model_file)
    print(mean_absolute_error(ORG_VAL, arr))
    # todo: WYKRES, alg na dłużej, porównć z org
