import sys

from aux_log import create_log, print_log
from aux_graph import produce_graph
from methodology import methodology
from methodology_performances import complexity_single_data_flow, complexity_multi_data_flow
from scenarios import *



def analyze_complexity_single_data_flow(nodes_range, max_num_of_nodes, num_of_simulations):
    print_log(f'ANALZIZE SINGLE DATA FLOW COMPLEXITY \n nodes_range = {nodes_range} max_num_nodes = {max_num_of_nodes} num_of_simulations = {num_of_simulations}')
    complexity_single_data_flow(nodes_range, max_num_of_nodes, num_of_simulations)

def analize_complexity_multi_data_flow(data_flows_range, max_num_of_data_flows, num_of_nodes, num_of_simulations):
    print_log(f'ANALZIZE MULTI DATA FLOW COMPLEXITY \n data_flows_range = {data_flows_range} max_num_of_data_flows = {max_num_of_data_flows} num_of_nodes = {num_of_nodes} num_of_simulations = {num_of_simulations}')    
    complexity_multi_data_flow(data_flows_range, max_num_of_data_flows, num_of_nodes, num_of_simulations)


def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <function> [arguments...]")
        sys.exit(1)
    function_name = sys.argv[1]
    args = sys.argv[2:]
    execution_log  = create_log()
    if function_name == 'methodology': 
        if len(args) != 1:
            print ("Usage main.py methodology scenario")
            sys.exit(1)
        else: 
            arg = args[0]
            if arg == 'facebook':
                print_log('FACEBOOK EXECUTION')
                scenario = FacebookScenario()
            elif arg == 'data_lake': 
                print_log('DATA LAKE EXECUTION')
                scenario = DataLakeScenario()
            elif arg == 'lambda':
                print_log('LAMBDA METHODOLOGY EXECUTION')
                scenario = LambdaScenario()
            elif arg == 'liquid':
                print_log('LIQUID METHODOLOGY EXECUTION')
                scenario = LiquidScenario()
            elif arg == 'kappa':
                print_log('KAPPA METHODOLOGY EXECUTION')
                scenario = KappaScenario()
            else:
                print("Invalid scenario\nValid scenarios: facebook , data_lake , lambda , liquid , kappa")
                sys.exit(1)
            scenario = scenario.generate_scenario()
            methodology(scenario)

    elif function_name == 'analyze_complexity_single_data_flow': 
        if len(args) != 3:
            print ("Usage main.py analyze_complexity_single_data_flow nodes_range num_of_nodes num_of_simulations")
            sys.exit(1)
        args = list(map(int, args))
        analyze_complexity_single_data_flow(*args)
    
    elif function_name == 'analyze_complexity_multi_data_flow':
        if len(args) != 4:
            print("Usage main.py analyze_complexity_multi_data_flow data_flows_range max_num_of_data_flows num_of_nodes num_of_simulations ")
            sys.exit(1)
        args = list(map(int, args))
        analize_complexity_multi_data_flow(*args)
    
    elif function_name == 'plot_single_data_flow':
        produce_graph('single_data_flow_simulations/single_50_600_3_2024-12-18_15-20-53_data.txt', 
                      'single_plot_0', 
                      'single_data_flow_graphs', 
                      'Number of nodes', 
                      'Exec time [s]' )
    
    elif function_name == 'plot_multi_data_flows':
        produce_graph('multi_data_flow_simulations/multi_10_50_300_3_2024-12-18_15-20-16_data.txt',
                      'multi_plot_0',
                      'multi_data_flow_graphs',
                      'Number of data flows',
                      'Exec time [s]'
                      )

    else:
        print("Invalid function.")
        sys.exit(1)
    

if __name__ == "__main__":
    main()