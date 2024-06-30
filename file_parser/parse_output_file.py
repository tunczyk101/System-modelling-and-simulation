NODES_METRIC = "Pressure"
LINKS_METRIC = "Flow"


def find_metric_id(line: str, metric: str) -> int:
    """
    Finds the id/number of the given metric in the line.

    :param line: A string representing a line with columns separated by whitespace.
    :param metric: The name of the metric to search for.
    :return: The id of the searched column (columns numbers start from 1).
    """
    for i, col in enumerate(line.split()):
        if col == metric:
            return i + 1

    raise ValueError(f"Metric {metric} not found")


def get_simulation_results(filename: str) -> list[float]:
    """
    Returns Pressure and Flow results for given file with EPANET output

    :param filename: name of a file with EPANET results
    :return: list with Pressure and Flow results from given file
    """
    results = []
    nodes_metric_id = None
    links_metric_id = None

    with open(filename) as output_file:
        lines = output_file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].split()
            if len(line) > 0:
                metric_id = None
                match line[0]:
                    case "Node":  # Set metric_id for Nodes (Pressure)
                        if (
                            nodes_metric_id is None
                        ):  # if we do not know in which col is Nodes metric - find it
                            nodes_metric_id = find_metric_id(lines[i + 2], NODES_METRIC)
                        metric_id = nodes_metric_id
                    case "Link":  # Set metric_id for Links (Flow)
                        if (
                            links_metric_id is None
                        ):  # if we do not know in which col is Links metric - find it
                            links_metric_id = find_metric_id(lines[i + 2], LINKS_METRIC)
                        metric_id = links_metric_id

                if metric_id is not None:  # read all Nodes/Links metrics values
                    i += 5  # Skip metadata lines
                    node_line = lines[i].split()
                    while len(node_line) > 0:
                        results.append(node_line[metric_id])
                        i += 1
                        node_line = lines[i].split()
                    continue  # End of metrics for Nodes/Links

            i += 1

    return results


if __name__ == "__main__":
    print(get_simulation_results("../epanet_model/output.txt"))
