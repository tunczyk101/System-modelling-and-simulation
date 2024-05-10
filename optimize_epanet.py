import numpy as np
from scipy.optimize import differential_evolution
from epanet_end_error import run_epanet_and_calculate_error


junctions_to_adjust = [' SO/ZD', ' SW/SO', ' SW/RO', ' SD/GO1', ' SW/AN', ' HP7']
pipes_to_adjust = [' p23', ' p129', ' p159']

def update_epanet_file(junctions_values, pipes_values):
    """
    Update EPANET model file with new junction and pipe values.
    :param junctions_values: List of updated values for junctions.
    :param pipes_values: List of updated values for pipes.
    """
    # read EPANET file
    with open('epanet_model/model.inp', 'r') as f:
        lines = f.readlines()

    # Find indices of [JUNCTIONS] and [PIPES] sections
    junctions_index = lines.index('[JUNCTIONS]\n')
    pipes_index = lines.index('[PIPES]\n')

    # Update values for junctions
    for i, junction in enumerate(junctions_to_adjust):
        for j, line in enumerate(lines[junctions_index:pipes_index]):  # Przeszukaj tylko sekcję [JUNCTIONS]
            if line.startswith('['):  # Zakończ przeszukiwanie po napotkaniu '['
                break
            if line.startswith(junction):
                parts = line.split()
                parts[2] = str(junctions_values[i])  # Zaktualizuj popyt
                lines[j + junctions_index] = '    '.join(parts) + '\n'  # Dodaj junctions_index, aby uwzględnić przesunięcie

    # Update values for pipes
    for i, pipe in enumerate(pipes_to_adjust):
        for j, line in enumerate(lines[pipes_index:]):  # Przeszukaj tylko sekcję [PIPES]
            if line.startswith('['):  # Zakończ przeszukiwanie po napotkaniu '['
                break
            if line.startswith(pipe):
                parts = line.split()
                parts[1] = str(pipes_values[i])  # Zaktualizuj szorstkość
                lines[j + pipes_index] = '    '.join(parts) + '\n'  # Dodaj pipes_index, aby uwzględnić przesunięcie


    # Save updated EPANET file
    with open('epanet_model/model.inp', 'w') as f:
        f.writelines(lines)

def reset_params_to_zero():
    """
    Reset junction and pipe values to zero.
    """
    junctions_values = [0] * len(junctions_to_adjust)
    pipes_values = [0] * len(pipes_to_adjust)
    update_epanet_file(junctions_values, pipes_values)

def optimize_epanet(x):
    """
    Optimize EPANET model by adjusting junction and pipe values.
    :param x: Optimizer's variable.
    :return: Error value after running EPANET model with adjusted values.
    """
    junctions_values = x[:len(junctions_to_adjust)]
    pipes_values = x[len(junctions_to_adjust):]
    update_epanet_file(junctions_values, pipes_values)

    # Run EPANET and calculate error
    error = run_epanet_and_calculate_error(junctions_to_adjust,pipes_to_adjust)

    return error

def main():
    """
    Main function to optimize EPANET model parameters.
    """
    # Call reset function
    reset_params_to_zero()

    desired_error = 0.01
    bounds = [(0,0.26)] * len(junctions_to_adjust) + [(0,5)] * len(pipes_to_adjust)
    
    result = differential_evolution(optimize_epanet, bounds)

    # If results are not satisfactory, start another round of optimization
    if result.fun > desired_error:
        result = differential_evolution(optimize_epanet, bounds, x0=result.x)

if __name__ == "__main__":
    main()
