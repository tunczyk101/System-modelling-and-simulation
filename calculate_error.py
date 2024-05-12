from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
)


def calculate_error(true_val, args, metric="mae"):
    """
    Calculates the selected error metric from the actual true_values
    and predicted args values.
    :param args: predicted values
    :param metric: name of the metric ('mae', 'rmse' or 'mse')
    :return: error -- the value of the error metric
    """

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
