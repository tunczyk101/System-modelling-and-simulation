# Algorithm for EPANET Calibration

We are going to optimize using Pressure for Junctions and/or Flow for pipes. These two are the same results of simulation that were used as Calibration Data for the original network.

## Prepare data

To analyze results, we need to add a `[REPORT]` section to the file and specify the nodes and pipes that will be checked during calibration. For example: SO/ZD, SW/SO, SW/RO, SD/GO1, SW/AN, HP7. Example for pipes: p23, p129, p159. 

Because we want to compare Pressure/Flow results:

```
[REPORT]

NODES SO/ZD, SW/SO, SW/RO, SD/GO1, SW/AN, HP7
LINKS p23, p129, p159
FLOW YES
PRESSURE YES
```

After running the original network, parse the output file to gather information about results for chosen junctions and pipes. Save this information to be used during optimization.

Example parameters values to optimize:
- **NODES**
  - [JUNCTIONS]: Demand, Elevation
  - [EMITTERS]: Emitter Coeff.
- **Pipe**
  - [PIPE]: Roughness, Loss Coeff.
  - [REACTIONS]: Bulk Coeff. (Add Wall Coeff. that is not used in the original project)


## Optimization solutions

We are going to use [scipy.optimize.differential_evolution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html#r108fc14fa019-3).

*Differential evolution is a stochastic population-based method that is useful for global optimization problems. At each pass through the population, the algorithm mutates each candidate solution by mixing with other candidate solutions to create a trial candidate.*

To use it, the function to be minimized must be defined, and bounds for variables must be provided.

- **variables**: values of a chosen parameter for all Nodes/Links in the network. (Candidates for solution)
- **bounds**: depend on a chosen variable, e.g., for roughness, bounds are adjusted according to those provided by manufacturers ± 0.1.
- **function**: we are going to minimize using one of the metrics: MAE or MSE. For every invocation, given variables will be written to the right places of the network file, then the `epanet` command line will be run using this network. Output of the simulation will be parsed to get the results and to compare them to the ones from the original network using the mentioned metrics.

The main part of the implementation is parsing input and output files for `runepanet`.