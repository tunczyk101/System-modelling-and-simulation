import subprocess
import numpy as np
from calculate_error import calculate_error
import time


def run_epanet_and_calculate_error(junctions,pipes, metric="mae"):
    """
    Runs EPANET model and calculates error metric based on the results.
    :param junctions: List of junctions.
    :param pipes: List of pipes.
    :param metric: Name of the error metric ('mae' by default).
    :return: error -- The value of the calculated error metric.
    """
    # Add [REPORT] section to the file
    with open('epanet_model/model.inp', 'r') as f:
        lines = f.readlines()
        report_section_start = lines.index('[REPORT]\n')
        report_section_end = lines.index('[END]\n')  # Zakładamy, że sekcja [REPORT] jest bezpośrednio przed sekcją [END]
        del lines[report_section_start:report_section_end]
        report_section = '\n[REPORT]\nNODES ' + ', '.join(junctions) + '\nLINKS ' + ', '.join(pipes) + '\nFLOW YES\nPRESSURE YES\n'
        lines.append(report_section)
    with open('epanet_model/model.inp', 'w') as f:
        f.writelines(lines)


    # run EPANET
    subprocess.run(['wine' , '/Users/judytabakowska/Desktop/epa/EPANET/build/bin/runepanet', 'epanet_model/model.inp', 'epanet_model/output.txt'],check=True)

    time.sleep(5)
    # Read results from the report
    with open('epanet_model/output.txt', 'r') as f:
        results = np.array([float(line.strip()) for line in f])

    error = calculate_error(results, metric)

    return error



