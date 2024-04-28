import numpy as np

def mean_absolute_error(y_true, y_pred):
    """
    Calculates the mean absolute error (MAE) between the actual y_true values and the predicted y_pred values.
    :param y_true: real values
    :param y_pred: predicted values
    :return: mean absolute error
    """
    mae = np.mean(np.abs(y_true - y_pred))
    return mae

def mean_squared_error(y_true, y_pred):
    """
    Calculates the mean square error (MSE) between the actual
    values of y_true and the predicted values of y_pred.
    :param y_true: real values
    :param y_pred: predicted values
    
    :return: mse - mean square error
    """
    mse = np.mean((y_true - y_pred) ** 2)
    return mse

def root_mean_squared_error(y_true, y_pred):
    """
    Calculates the root mean square error (RMSE) between the actual y_true values and the predicted y_pred values.
    :param y_true: real values
    :param y_pred: predicted values
    :return: rmse - root mean squared error
    """
    rmse = np.sqrt(mean_squared_error(y_true,y_pred))
    return rmse


def calculate_error(args, metric='mae'):
    """
    Calculates the selected error metric from the actual true_values 
    and predicted args values.
    :param *args: predicted values
    :param metric: name of the metric ('mae', 'rmse' or 'mse')
    :return: error -- the value of the error metric
    """
    true_val = np.array([1,2,3,4,5,6])
    
    if metric == 'mae':
        error = mean_absolute_error(true_val,args)
    elif metric == 'rmse':
        error =  root_mean_squared_error(true_val,args)
    elif metric == 'mse':
        error = mean_squared_error(true_val,args)
    else:
        raise ValueError("Unknown metric. Available metrics: 'mae', 'rmse', 'mse'.")
    
    return error


#example of use

predicted_val = np.array([1.5, 2.0, 2.5,4,4, 8])

print("MAE:", calculate_error(predicted_val, metric='mae'))
print("RMSE:", calculate_error(predicted_val, metric='rmse'))
print("MSE:", calculate_error(predicted_val, metric='mse'))
