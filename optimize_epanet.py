from scipy.optimize import differential_evolution
import subprocess
import shutil
from file_parser.parse_output_file import get_simulation_results
from calculate_error import calculate_error
import sys

junctions_to_adjust = [" SO/ZD ", " SW/SO ", " SW/RO ", " SD/GO1 ", " SW/AN ", " HP7 "]
pipes_to_adjust = [" p23", " p129", " p159"]


def update_epanet_file(filename, x):
    # read EPANET file
    with open(filename) as model_file:
        lines = model_file.readlines()

    junctions_index = lines.index("[JUNCTIONS]\n") + 2
    pipes_index = lines.index("[PIPES]\n") + 2

    # update junctions
    for i in range(len(junctions_to_adjust)):
        for j in range(junctions_index, pipes_index):
            if lines[j].startswith(junctions_to_adjust[i]):
                parts = lines[j].split()
                lines[j] = lines[j].replace("\t" + parts[2], "\t" + str(x[i]))
                break

    # update pipes
    for i in range(len(pipes_to_adjust)):
        for j in range(pipes_index, len(lines)):
            if lines[j].startswith(pipes_to_adjust[i]):
                parts = lines[j].split()
                lines[j] = lines[j].replace(
                    "\t" + parts[5], "\t" + str(x[i + len(junctions_to_adjust)])
                )
                break

    # write back to file
    with open(filename, "w") as model_file:
        model_file.writelines(lines)


def optimize_epanet(x):
    """
    Optimize EPANET model by adjusting junction and pipe values.
    :param x: Optimizer's variable.
    :return: Error value after running EPANET model with adjusted values.
    """
    update_epanet_file(optimalize_model, x)

    # Run EPANET and calculate error
    error = run_epanet_and_calculate_error(
        junctions_to_adjust, pipes_to_adjust, metric="mae"
    )

    if error > 0.001:
        print(error)
        sys.exit()
    return error


def add_report_section(original_model):
    with open(original_model, "r") as f:
        lines = f.readlines()
        report_section_start = lines.index("[REPORT]\n")
        report_section_end = lines.index("[END]\n")
        del lines[report_section_start : report_section_end + 1]
        report_section = (
            "[REPORT]\nNODES"
            + " ".join(junctions_to_adjust)
            + "\nLINKS"
            + " ".join(pipes_to_adjust)
            + "\nFLOW YES\nPRESSURE YES\n\n[END]\n"
        )
        lines.append(report_section)
    with open(original_model, "w") as f:
        f.writelines(lines)


def run_epanet_and_calculate_error(junctions, pipes, metric="mse"):
    """
    Runs EPANET model and calculates error metric based on the results.
    :param junctions: List of junctions.
    :param pipes: List of pipes.
    :param metric: Name of the error metric ('mae' by default).
    :return: error -- The value of the calculated error metric.
    """
    # run EPANET
    subprocess.run(
        [r"D:\EPANET 2.2\runepanet.exe", optimalize_model, optimalize_output],
        check=True,
    )

    # Read results from the report
    results_optimalize = get_simulation_results(optimalize_output)
    results_true = get_simulation_results(original_output)

    error = calculate_error(results_true, results_optimalize, metric)

    return error


def main():
    """
    Main function to optimize EPANET model parameters.
    """
    subprocess.run(
        [r"D:\EPANET 2.2\runepanet.exe", original_model, original_output], check=True
    )

    bounds = [(0, 0.26)] * len(junctions_to_adjust) + [(0, 5)] * len(pipes_to_adjust)

    differential_evolution(optimize_epanet, bounds)


# Copy model file
original_model = "epanet_model/model_original.inp"
add_report_section(original_model)

optimalize_model = "epanet_model/model_optimalize.inp"
shutil.copyfile(original_model, optimalize_model)
original_output = "epanet_model/output_true_values.txt"
optimalize_output = "epanet_model/output_optimalize_values.txt"

if __name__ == "__main__":
    main()
