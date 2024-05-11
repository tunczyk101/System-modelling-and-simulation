def get_simulation_results(filename, as_dictionary=False):
    nodes = {}
    links = {}

    with open(filename) as output_file:
        lines = output_file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].split()
            if len(line) > 0:
                match line[0]:
                    case "Node":
                        # get hour
                        nodes[line[3]] = {}
                        i += 5
                        node_line = lines[i].split()
                        while len(node_line) > 0:
                            # for each id collect pressure
                            nodes[line[3]][node_line[0]] = node_line[4]
                            i += 1
                            node_line = lines[i].split()
                        continue
                    case "Link":
                        # get hour
                        links[line[3]] = {}
                        i += 5
                        link_line = lines[i].split()
                        while len(link_line) > 0:
                            # for each id collect flow
                            links[line[3]][link_line[0]] = link_line[1]
                            i += 1
                            link_line = lines[i].split()
                        continue

            i += 1

    if as_dictionary:
        return {
            "nodes": nodes,
            "links": links
        }

    results = [value for h in nodes.values() for value in h.values()]
    results += [value for h in links.values() for value in h.values()]
    return results


if __name__ == "__main__":
    print(get_simulation_results("../epanet_model/output.txt"))
    print(get_simulation_results("../epanet_model/output.txt", as_dictionary=True))
