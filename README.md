# Semi-Automated Design of Data-Intensive Architectures

 ## Overview
This repository contains Python script code designed to to execute simulations of the first step of our methodology on various scenarios, particularly those described in the "Evaluation" section of our paper. These scenarios include the reference architectures (data lake, lambda, liquid, kappa) as well as Facebook. 

### Usage

To run the script, use the following command:

```bash
python main.py <function> [arguments...]
```

  
1. **Functions**:
- `methodology`: Executes the methodology for a specified scenario. Valid scenarios include 'facebook', 'data_lake', 'lambda', 'liquid', and 'kappa'.
- `analyze_complexity_single_data_flow`: Analyzes the complexity of a single data flow scenario based on the provided parameters.
- `analyze_complexity_multi_data_flow`: Analyzes the complexity of a multi data flow scenario based on the provided parameters.

2. **Arguments**:
- For `methodology`:
  - Specify the scenario as an argument. Possible options are `facebook`, `data-lake`, `lambda` `liquid` and `kappa`.

- For `analyze_complexity_single_data_flow` provide as arguments.:
  - `nodes_range` (i.e., the number of nodes that is increased with each simulation)
  - `max_num_of_nodes`(i.e., the maximum number of nodes to be simulated)
  - `num_of_simulations` (i.e. the number of simulations to be carried out with the same number of nodes)

- For `analyze_complexity_multi_data_flow` provide as arguments:
  - `data_flows_range`  (i.e., the number of data flows that is increased with each simulation)
  - `max_num_of_data_flows` (i.e., the maximum number of data flows to be simulated)
  - `num_of_nodes` (i.e., the number of nodes composing the scenarios
  - `num_of_simulations`  (i.e. the number of simulations to be carried out with the same number of nodes).

4. **Diagram Generation**:
The script generates PDF graphs of the simulations performed in `single_data_flow_simulations` and `multi_data_flow_simulations` folders

## Example Usage
1. To execute methodology for the a scenario (e.g., Lambda): `main.py methodology lambda`
2. To analyze the complexity of scenarios with a single data flow when the number of nodes increases: `main.py analyze_complexity_single_data_flow 50 600 3`
3. To analyze the complexity of scenarios for a fixed number of node when the number of dataflows increases: `main.py analyze_complexity_multi_data_flow 10 50 300 3`


## Defining New Scenarios
Users have the flexibility to define new scenarios by subclassing the `Scenario` class. This approach allows for the extension of the framework to support a wide range of scenarios beyond those already provided.

### How to Define New Scenarios
In file `scenario.py`
1. **Create a Subclass of `Scenario`**: Start by creating a new subclass of the `Scenario` class for the desired scenario.

2. **Implement `generate_scenario()` Method**: Within the subclass, implement the `generate_scenario()` method. This method should define the structure of the scenario graph and specify the properties of nodes and edges.

4. **Return the Scenario Graph**: Ensure that the `generate_scenario()` method returns a NetworkX graph representing the scenario.

In file `main.py` add the input parameter for the created scenario



## Logging
The script utilizes logging functionality to output execution logs in `logs` that can be found in `log`folder.
