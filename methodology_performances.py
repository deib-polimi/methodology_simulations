import os
from scenarios import * 
from methodology import methodology
from aux_simulation import create_graph
from datetime import datetime

# run number_of_simulations simulations on a graph componsed of number_of_nodes nodes
def stress_single_data_flow(number_of_nodes, number_of_simulations):
    times = []
    for i in range(number_of_simulations):
        scenario = SingleDataFlowScenario(number_of_nodes=number_of_nodes)
        scenario = scenario.generate_scenario()
        time_i = methodology(scenario)
        times.append(time_i)
    avg_time = sum(times) / len(times)
    return avg_time

# run number_of_simulations simulations with a graph composed of "number_of_data_flows" data flows
def stress_multi_data_flow(number_of_nodes, number_of_data_flows, number_of_simulations):
    times = []
    for i in range(number_of_simulations):
        scenario = MultiDataFlowScenario(number_of_nodes=number_of_nodes , number_of_data_flows=number_of_data_flows)
        scenario = scenario.generate_scenario()
    #scenario = create_multi_data_flow_graph(number_of_nodes, number_of_data_flows)
        time_i = methodology(scenario)
        times.append(time_i)
    avg_time = sum(times) / len(times)
    return avg_time


# Verify the performances for a single data flow scenario when number of nodes increases
def complexity_single_data_flow(nodes_range, max_num_of_nodes, num_of_simulations):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    simulation_name = f'single_{nodes_range}_{max_num_of_nodes}_{num_of_simulations}_{timestamp}'
    avg_times = []
    n_nodes_list = []

    folder_path = 'single_data_flow_simulations'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(os.path.join(folder_path, f'{simulation_name}_data.txt'), 'w') as f:
        f.write("tens_num_of_nodes,avg_time\n")
        
        for num_of_nodes in range(nodes_range, max_num_of_nodes + num_of_simulations, nodes_range):
            if num_of_nodes != 1: 
                n_nodes_list.append(num_of_nodes)
                avg_time = stress_single_data_flow(num_of_nodes, num_of_simulations)
                avg_times.append(avg_time)
                f.write(f"{num_of_nodes},{avg_time}\n")

    graph_folder = 'single_data_flow_graphs'
    create_graph(simulation_name, graph_folder, 'Number of number of nodes', n_nodes_list, 'Exec time [s]', avg_times)


# Verify performances when the number of data flows in a scenario with fixed number of nodes increases
def complexity_multi_data_flow(data_flows_range, max_num_of_data_flows, num_of_nodes, num_of_simulations):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    simulation_name = f'multi_{data_flows_range}_{max_num_of_data_flows}_{num_of_nodes}_{num_of_simulations}_{timestamp}'
    avg_times = []
    n_data_flows_list = []

    folder_path = 'multi_data_flow_simulations'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(os.path.join(folder_path, f'{simulation_name}_data.txt'), 'w') as f:
        f.write("num_of_data_flows,avg_time\n")

        for num_of_data_flows in range(data_flows_range, max_num_of_data_flows + data_flows_range, data_flows_range):
            if (num_of_nodes > num_of_data_flows + 1):
                n_data_flows_list.append(num_of_data_flows)
                avg_time = stress_multi_data_flow(num_of_nodes, num_of_data_flows, num_of_simulations)
                avg_times.append(avg_time)
                f.write(f"{num_of_data_flows},{avg_time}\n")

    graph_folder = 'multi_data_flow_graphs'
    create_graph(simulation_name, graph_folder,'Number of data flows', n_data_flows_list, 'Exec time [s]', avg_times)

