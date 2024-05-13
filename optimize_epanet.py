from scipy.optimize import differential_evolution
import subprocess
import shutil
from file_parser.parse_output_file import get_simulation_results
from calculate_error import calculate_error
import sys

JUNCTIONS_TO_ADJUST = [' SO/ZD', ' SW/SO', ' SW/RO', ' SD/GO1', ' SW/AN', ' HP7']
PIPES_TO_ADJUST = [' p23', ' p129', ' p159']
runepanet = r"D:\EPANET 2.2\runepanet.exe"


def update_epanet_file(filename, x):
    # read EPANET file
    with open(filename) as model_file:
        lines = model_file.readlines()
    
    # update junctions
    #for j in range(junctions_start, junctions_end):
    #    parts = lines[j].split()
    #    lines[j] = lines[j].replace('\t' + parts[2], '\t'+str(x[j-5]))

    # update pipes
    for i in range(pipes_start, pipes_end):
        parts = lines[i].split()
        lines[i] = lines[i].replace('\t' + parts[5]+" ", '\t'+str(x[i-pipes_start]))

    # write back to file
    with open(filename, 'w') as model_file:
        model_file.writelines(lines)



def optimize_epanet(x):
    """
    Optimize EPANET model by adjusting junction and pipe values.
    :param x: Optimizer's variable.
    :return: Error value after running EPANET model with adjusted values.
    """
    update_epanet_file(optimalize_model, x)

    # Run EPANET and calculate error
    error = run_epanet_and_calculate_error(metric="mae")
    
    return error

def add_report_section(original_model):
    with open(original_model, 'r') as f:
        lines = f.readlines()
        lines.reverse() 
        report_line = None
        end_line = None
        report_line_number = None
        end_line_number = None
        nodes  = "NODES"
        pipes = "LINKS"
        for i, line in enumerate(lines):
            if '[END]' in line and end_line is None:
                end_line = line
                end_line_number = len(lines) - i 
            if '[REPORT]' in line and report_line is None:
                report_line = line
                report_line_number = len(lines) - i  
            if report_line_number != None and end_line_number != None:
                lines.reverse()
                del lines[report_line_number:end_line_number+1]
                for j in JUNCTIONS_TO_ADJUST:    
                    nodes  += j
                for n in PIPES_TO_ADJUST:
                    pipes += n
                text = [nodes,"\n",pipes,'\nFLOW YES','\nPRESSURE YES',"\n",'[END]']
                for input in text:    
                    lines.append(input)
                break
                
    with open(original_model, 'w') as f:
        f.writelines(lines)
        

def run_epanet_and_calculate_error(metric="mse"):
    """
    Runs EPANET model and calculates error metric based on the results.
    :param junctions: List of junctions.
    :param pipes: List of pipes.
    :param metric: Name of the error metric ('mae' by default).
    :return: error -- The value of the calculated error metric.
    """
    subprocess.run([runepanet, optimalize_model, optimalize_output],check=True)

    # Read results from the report
    results_optimalize = get_simulation_results(optimalize_output)
    results_true =  get_simulation_results(original_output)

    error = calculate_error(results_true, results_optimalize, metric)
    print(error)
    if error < 0.05:
        sys.exit()
    return error


def main():
    """
    Main function to optimize EPANET model parameters.
    """
    subprocess.run([runepanet, original_model, original_output],check=True)


    bounds = [(0,5)] * (pipes_end-pipes_start)
    
    differential_evolution(optimize_epanet, bounds,mutation=(0.5,1),recombination=0.7)


# Copy model file
original_model = 'epanet_model/model_original.inp'
add_report_section(original_model)

with open(original_model) as model_file:
    lines = model_file.readlines()
    junctions_start = lines.index('[JUNCTIONS]\n') +2
    junctions_end = lines.index('[RESERVOIRS]\n') -1
    pipes_start = lines.index('[PIPES]\n') +2
    pipes_end = lines.index('[PUMPS]\n') -1

optimalize_model = 'epanet_model/model_optimalize.inp'
shutil.copyfile(original_model, optimalize_model)
original_output = 'epanet_model/output_true_values.txt'
optimalize_output = 'epanet_model/output_optimalize_values.txt'

if __name__ == "__main__":
    main()