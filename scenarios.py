
import networkx as nx
import random 

ms = 1/0.001
h = 1/3600
day = 1/86400
min15 = 1/900

class Scenario:
    def generate_scenario(self):
        print('Scenario undefined')
        exit(1)
    
class FacebookScenario(Scenario):
    def generate_scenario(self):
        facebook_scenario = nx.DiGraph()
        facebook_scenario.add_node('P1', type = 'producer')
        facebook_scenario.add_node('P2', type = 'producer')
        facebook_scenario.add_node('C1', type = 'consumer', deliveryGuarantee = 'atMost')
        facebook_scenario.add_node('C2', type = 'consumer', deliveryGuarantee = 'atMost')
        facebook_scenario.add_node('C3', type = 'consumer', deliveryGuarantee = 'atsMost')
        facebook_scenario.add_node('n1', type = 'processing', inputCardinality = 10, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        facebook_scenario.add_node('n2', type = 'merge', inputCardinality = 100, outputCardinality = 100, cc_func = 1, rc_func = 0.01)
        facebook_scenario.add_node('n3', type = 'processing', inputCardinality = 1, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        facebook_scenario.add_node('n4', type = 'processing', inputCardinality = 100, outputCardinality = 10, cc_func = 1, rc_func = 0.01)
        facebook_scenario.add_node('n5', type = 'processing', inputCardinality = 100, outputCardinality = 10, cc_func = 1, rc_func = 0.01)
        facebook_scenario.add_edge('P1', 'n1', f = ms)       
        facebook_scenario.add_edge('P2', 'n2', f = day)      
        facebook_scenario.add_edge('n1', 'n2', f = min15)    
        facebook_scenario.add_edge('n2', 'n3', f = ms)       
        facebook_scenario.add_edge('n2', 'n4', f = h)        
        facebook_scenario.add_edge('n2', 'n5', f = day)      
        facebook_scenario.add_edge('n3', 'C1', f = ms)       
        facebook_scenario.add_edge('n4', 'C2', f = h)        
        facebook_scenario.add_edge('n5', 'C3', f = day)   
        return facebook_scenario   

class DataLakeScenario(Scenario):
    def generate_scenario(self):
        data_lake_scenario = nx.DiGraph()
        data_lake_scenario.add_node('P1', type = 'producer')
        data_lake_scenario.add_node('P2', type = 'producer')
        data_lake_scenario.add_node('C1', type = 'consumer', deliveryGuarantee = 'atLeast')
        data_lake_scenario.add_node('C2', type = 'consumer', deliveryGuarantee = 'atLeast')
        data_lake_scenario.add_edge('P1', 'C1', f = ms)
        data_lake_scenario.add_edge('P2', 'C2', f = ms)
        return data_lake_scenario

class LambdaScenario(Scenario): 
    def generate_scenario(self):
        lambda_scenario = nx.DiGraph()
        lambda_scenario.add_node('P1', type = 'producer')
        lambda_scenario.add_node('P2', type = 'producer')
        lambda_scenario.add_node('C1', type = 'consumer', deliveryGuarantee = 'atMost')
        lambda_scenario.add_node('C2', type = 'consumer', deliveryGuarantee = 'atMost')
        lambda_scenario.add_node('n1', type = 'processing', inputCardinality = 1, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        lambda_scenario.add_node('n2', type = 'processing', inputCardinality = 100, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        lambda_scenario.add_node('n3', type = 'merge', inputCardinality = 100, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        lambda_scenario.add_edge('P1', 'n1', f = ms)
        lambda_scenario.add_edge('P2', 'n2', f = ms)
        lambda_scenario.add_edge('n1', 'n3', f = ms)
        lambda_scenario.add_edge('n2', 'n3', f = h)
        lambda_scenario.add_edge('n3', 'C1', f = ms)
        lambda_scenario.add_edge('n3', 'C2', f = h)
        return lambda_scenario     

class LiquidScenario(Scenario):
    def generate_scenario(self): 
        liquid_scenario = nx.DiGraph()
        liquid_scenario.add_node('P1', type = 'producer')
        liquid_scenario.add_node('P2', type = 'producer')
        liquid_scenario.add_node('C1', type = 'consumer', deliveryGuarantee = 'atLeast')
        liquid_scenario.add_node('n1', type = 'merge', inputCardinality = 10, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        liquid_scenario.add_edge('P1', 'n1', f = ms)
        liquid_scenario.add_edge('P2', 'n1', f = ms)
        liquid_scenario.add_edge('n1', 'C1', f = ms)
        return liquid_scenario
  
class KappaScenario(Scenario): 
    def generate_scenario(self):
        kappa_scenario = nx.DiGraph()
        kappa_scenario.add_node('P1', type = 'producer')
        kappa_scenario.add_node('P2', type = 'producer')
        kappa_scenario.add_node('C1', type = 'consumer', deliveryGuarantee = 'atMost')
        kappa_scenario.add_node('C2', type = 'consumer', deliveryGuarantee = 'atMost')
        kappa_scenario.add_node('n1', type = 'merge', inputCardinality = 100, outputCardinality = 1, cc_func = 1, rc_func = 0.01)
        kappa_scenario.add_edge('P1', 'n1', f = ms)
        kappa_scenario.add_edge('P2', 'n1', f = ms)
        kappa_scenario.add_edge('n1', 'C1', f = ms)
        kappa_scenario.add_edge('n1', 'C2', f = h)
        return kappa_scenario        


class SingleDataFlowScenario(Scenario):
    def __init__(self, number_of_nodes): 
        self.number_of_nodes = number_of_nodes

    def generate_scenario(self): 
        scenario = nx.DiGraph()
        cardinalities = [1, 10, 100, 1000, 10000]
        c_func = [0.001, 0.01, 0.1, 1, 10, 100]

        # add producer to graph
        scenario.add_node('P1', type = 'producer')

        # add consumer to graph
        # randomly choose guarantees
        deliveryGuarantee = random.choice(["atLeast", "atMost", "exactly"])
        scenario.add_node('C1', type = 'consumer', deliveryGuarantee = deliveryGuarantee)

        if (self.number_of_nodes == 2):
            f_edge =  f_edge = random.uniform(0.0001, 10000)
            scenario.add_edge('P1' , 'C1', f = f_edge)
        else:
        # add internal node
            for i in range(1, self.number_of_nodes - 1):
                if i!= 1:
                # randomly choose attributes
                    node_type = 'merge' if random.random() < 0.8 and i != 0 else 'processing'
                else: 
                    node_type = 'processing'
                ic = random.choice(cardinalities)
                uc = random.choice(cardinalities)
                cc = random.choice(c_func)
                cr = random.choice(c_func)
                scenario.add_node(f'n{i}', type = node_type, inputCardinality = ic, outputCardinality = uc, cc_func = cc, rc_func = cr)

            # add initial edge
            f_edge = random.uniform(0.0001, 10000)
            scenario.add_edge('P1', 'n1', f = f_edge)

            # add final edge
            f_edge = random.uniform(0.0001, 10000)
            scenario.add_edge(f'n{self.number_of_nodes - 2}', 'C1', f = f_edge)

            # add internal edges according to node type
            for i in range(2, self.number_of_nodes - 1):
                node = scenario.nodes[f'n{i}']
                if node['type'] == 'merge':
                    num_incoming_edges = random.randint(1,i)
                    incoming_edges = random.sample(range(0,i), num_incoming_edges)
                    for source_node in incoming_edges:
                        f_edge = random.uniform(0.0001, 10000) 
                        if source_node != 0:
                            scenario.add_edge(f'n{source_node}', f'n{i}', f = f_edge)
                        else: 
                            scenario.add_edge('P1', f'n{i}', f = f_edge)
                else:
                    f_edge = random.uniform(0.0001, 10000)
                    if i != 1:
                        scenario.add_edge(f'n{i-1}', f'n{i}', f = f_edge)
            
            #check at least one in and out
            for i in range(1, self.number_of_nodes-2): 
                if not(list(scenario.predecessors(f'n{i}'))):
                    f_edge = random.uniform(0.0001, 10000)
                    scenario.add_edge(f'n{i-1}' f'n{i}', f = f_edge)
                if not(list(scenario.successors(f'n{i}'))):
                    f_edge = random.uniform(0.0001, 10000)
                    scenario.add_edge(f'n{i}', f'n{i+1}', f = f_edge) 
        return scenario



class MultiDataFlowScenario(Scenario):
    def __init__(self, number_of_nodes, number_of_data_flows): 
        self.number_of_data_flows = number_of_data_flows
        self.number_of_nodes = number_of_nodes

    def generate_scenario(self):
        scenario = SingleDataFlowScenario(number_of_nodes=(self.number_of_nodes - self.number_of_data_flows + 1))
        scenario = scenario.generate_scenario()

        num_of_internal_nodes = scenario.number_of_nodes() - 2
        for i in range(2, self.number_of_data_flows + 1):
            node_id = random.randint(1, num_of_internal_nodes)
            f_edge = random.uniform(0.0001, 10000)
            deliveryGuarantee = random.choice(["atLeast", "atMost", "exactly"])
            scenario.add_node(f'C{i}', type = 'consumer', deliveryGuarantee = deliveryGuarantee)
            scenario.add_edge(f'n{node_id}', f'C{i}', f = f_edge)

        return scenario
