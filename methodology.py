from methodology_steps import *

def methodology(scenario):
    start_time = time.time()
    print_log('START')
    print_log(f'Scenario nodes: {scenario.nodes(data=True)}')
    print_log(f'Scenario edges: {scenario.edges(data=True)}')
    print_log_newline()

    # (1) scenario decomposition
    print_log('(1) SCENARIO DECOMPOSITION')
    data_flows = scenario_decomposition(scenario)
    i = 1
    for data_flow in data_flows:
         print_log(f'DATA FLOW {i} \n nodes = {data_flow.nodes()} \n edges = {data_flow.edges()} \n')
         i+=1
    print_log_newline()

    # (2) for each data flow 
    print_log('(2) FOR EACH DATA FLOW\n')
    for data_flow in data_flows:
        consumer = find_consumers(data_flow)[0]
        # (2.1) selection of components within single data flow
        print_log(f'(2.1) Selection of components for data flow {consumer}')
        components_data_flow(data_flow)
        print_log('Selected components')
        for data_flow_internal_node_id in find_action_nodes(data_flow):
            type = data_flow.nodes[data_flow_internal_node_id] [f'optimalType{consumer}']
            print_log(f'{data_flow_internal_node_id} for {consumer} = {type}')
        print_log_newline()
        # (2.2) selection of links within single data flow
        print_log(f'(2.1) Selection of links for data flow {consumer}')
        links_data_flow(data_flow)
        print_log('Selected links')
        for edge in data_flow.edges():
            type = data_flow.edges [edge][f'type{consumer}']
            print_log(f'edge {edge} = {type}')
        print_log_newline()
    print_log_newline()

    #(3) integration of data flows
    print_log('(3) DATA FLOW INTEGRATION')
    integration_data_flows(scenario)
    scenario_internal_node_ids = find_action_nodes(scenario)
    print_log('Architecture Result')
    print_log('Components')
    for node_id in scenario_internal_node_ids:
        components = scenario.nodes[node_id]['optimalTypes']
        print_log(f'optimal types for {node_id} = {components}')
    print_log('Links')
    for edge in scenario.edges():
        t = scenario.edges [edge]['type']
        print_log(f'edge {edge} type = {t}')

    end_time = time.time()
    execution_time = end_time - start_time
    print_log_newline()
    print_log_newline()
    print_log(f'First step execution time: {execution_time} seconds\n')
    
    return execution_time


