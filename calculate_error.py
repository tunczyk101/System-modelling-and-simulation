import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
)


def calculate_error(args, metric="mae"):
    """
    Calculates the selected error metric from the actual true_values
    and predicted args values.
    :param args: predicted values
    :param metric: name of the metric ('mae', 'rmse' or 'mse')
    :return: error -- the value of the error metric
    """
    true_val = np.array([1, 2, 3, 4, 5, 6])

    match metric:
        case "mae":
            error = mean_absolute_error(true_val, args)
        case "rmse":
            error = root_mean_squared_error(true_val, args)
        case "mse":
            error = mean_squared_error(true_val, args)
        case _:
            raise ValueError("Unknown metric. Available metrics: 'mae', 'rmse', 'mse'.")

    return error


# example of use

predicted_val = np.array([1, 2.0, 2.5, 4, 5, 8])

print("MAE:", calculate_error(predicted_val, metric="mae"))
print("RMSE:", calculate_error(predicted_val, metric="rmse"))
print("MSE:", calculate_error(predicted_val, metric="mse"))
