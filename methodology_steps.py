import networkx as nx
import pulp
from aux_log import *
from aux_graph import *

# split scenario in data flows
def scenario_decomposition(scenario):
    data_flows = []
    consumer_ids = find_consumers(scenario)
    for consumer_id in consumer_ids: 
        data_flow = nx.ancestors(scenario, consumer_id) | {consumer_id}
        data_flows.append(scenario.subgraph(data_flow))
    return data_flows


# identify optimal components for a data flow
def components_data_flow(data_flow):
    internal_nodes_ids = find_action_nodes(data_flow)
    consumer_id = find_consumers(data_flow)[0]

    # compute c_sc, c_dc_b, c_dc_s
    print_log_newline()
    print_log('Compute costs')
    for internal_node_id in internal_nodes_ids: 
        internal_node = data_flow.nodes[internal_node_id]
        
        in_cardinality = internal_node['inputCardinality']
        out_cardinality = internal_node['outputCardinality']
        cc = internal_node['cc_func']
        rc = internal_node['rc_func']
        
        f_in = find_f_in(data_flow, internal_node_id)
        f_out = find_f_out(data_flow, internal_node_id)

        c_sc = f_in * cc * in_cardinality + f_out * rc * out_cardinality
        c_dc_b = f_out * cc * in_cardinality
        c_dc_s = f_in * cc * out_cardinality

        internal_node['c_sc'] = c_sc
        internal_node['c_dc_b'] = c_dc_b
        internal_node['c_dc_s'] = c_dc_s

        print_log(f'{internal_node_id}: c_sc = {c_sc} c_dc_b = {c_dc_b} c_dc_s = {c_dc_s}')

    print_log_newline()

    # set optimization problem
    print_log('Optimize costs')
    prob = pulp.LpProblem("MinimizationProblem", pulp.LpMinimize)

    # decision variables
    X_dc_s = pulp.LpVariable.dicts("X_dc_s", internal_nodes_ids, cat=pulp.LpBinary)
    X_dc_b = pulp.LpVariable.dicts("X_dc_b", internal_nodes_ids, cat=pulp.LpBinary)
    X_sc = pulp.LpVariable.dicts("X_sc", internal_nodes_ids, cat=pulp.LpBinary)

    # objective function
    prob += pulp.lpSum(\
        X_dc_s[node_id] * (data_flow.nodes[node_id]['c_dc_s']) +\
        X_dc_b[node_id] * (data_flow.nodes[node_id]['c_dc_b']) +\
        X_sc[node_id] * (data_flow.nodes[node_id]['c_sc'])
        for node_id in internal_nodes_ids)

    # constraint
    for node_id in internal_nodes_ids:
        prob+=pulp.lpSum((X_dc_s[node_id] + X_dc_b[node_id] + X_sc[node_id]) ) == 1

    start_time = time.time()
    prob.solve(solver=pulp.PULP_CBC_CMD(msg=False))
    end_time = time.time()

    execution_time = end_time - start_time

    print_log(f'Optimization execution time: {execution_time} secondi')
    print_log(f'State: {pulp.LpStatus[prob.status]}')
    print_log(f'Optimal Value: {pulp.value(prob.objective)}')
    print_log_newline()

    # assign components that support nodes
    for node_id in internal_nodes_ids: 
        node = data_flow.nodes[node_id]
        print_log(f'Node {node_id}: X_dc_b = {pulp.value(X_dc_b[node_id])}  X_dc_s = {pulp.value(X_dc_s[node_id])}  X_sc = {pulp.value(X_sc[node_id])}')
        if (pulp.value(X_dc_s[node_id]) == 1):
            node[f'optimalType{consumer_id}'] = "data-centric-stream"
        elif (pulp.value(X_dc_b[node_id]) == 1):
            if(node['c_dc_s'] != node['c_dc_b']):
                node[f'optimalType{consumer_id}'] = "data-centric-batch"
            else: 
                node[f'optimalType{consumer_id}'] = "data-centric-stream"
        elif (pulp.value(X_sc[node_id]) == 1):
            node[f'optimalType{consumer_id}'] = "state-centric"
    print_log_newline()


# identify links for a data flow
def links_data_flow(data_flow): 
    consumer_id = find_consumers(data_flow)[0]
    consumer_guarantee = data_flow.nodes[consumer_id]['deliveryGuarantee']
    persistent = consumer_guarantee != 'atMost'

    for edge in data_flow.edges():
        upstream, downstream = edge
        if(persistent and data_flow.nodes[upstream]['type'] == 'producer'):
            data_flow.edges [edge][f'type{consumer_id}'] = 'persistent'
        else:
            data_flow.edges [edge][f'type{consumer_id}'] = 'volatile'


def integration_data_flows(scenario):
    internal_node_ids = find_action_nodes(scenario)
    consumer_ids = find_consumers(scenario)
    producer_ids = find_producers(scenario)

    #identify optimal components
    for node_id in internal_node_ids: 
        node = scenario.nodes[node_id]
        components = []
        for consumer_id in consumer_ids: 
            if f'optimalType{consumer_id}' in node: 
                component = node[f'optimalType{consumer_id}']
                components.append(component)

        components = set(components)
        if 'data-centric-batch' in components and 'data-centric-stream' in components: 
            components.remove('data-centric-batch')
        node['optimalTypes'] = components

    #identify optimal link
    for edge in scenario.edges():
        upstream, downstream = edge

        data_flow_types = []
        for consumer_id in consumer_ids:
            if f'type{consumer_id}' in scenario.edges [edge]:
                data_flow_types.append(scenario.edges [edge][f'type{consumer_id}'])
        
        if 'persistent' in data_flow_types: 
                scenario.edges [edge]['type'] = 'persistent'
        elif upstream in internal_node_ids and downstream in internal_node_ids:
            if 'data-centric-batch' in scenario.nodes[downstream]['optimalTypes'] and 'state-centric' not in scenario.nodes[upstream]['optimalTypes']:
                scenario.edges [edge]['type'] = 'persistent'
            else:
                scenario.edges [edge]['type'] = 'volatile'
        else:
            scenario.edges [edge]['type'] = 'volatile'
    


