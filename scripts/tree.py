from graphviz import Digraph
import networkx as nx


'''
Tree class
- each node is (action(str), level)
- root node is ('Initial state', 0)
'''


class Tree:
    def __init__(self, root_node):
        self.G = nx.MultiDiGraph()  # Create a directed graph with multiple edges allowed
        self.root = root_node
        self.G.add_node(self.root, visits=1, win=0)
        self.filtered_nodes = []

    def add_node(self, parent_node, child_node, action, weight, indices, visits, win, threshold=0.0):
        # if the seq probability is below the threshold, discard the node
        if weight < threshold:
            self.filtered_nodes.append((parent_node, child_node, weight))
            return None

        '''
        if len(list(self.G.successors(parent_node))) >= k:
            print(f"Cannot add more than {k} children to this node.")
            return None
        '''
        self.G.add_node(child_node, key=indices, visits=visits, win=win)  # indices = [plan_idx, state_idx(node level)]
        self.G.add_edge(parent_node, child_node, key=action, weight=weight)
        return child_node


    def get_heaviest_path(self):
        current_node = self.root
        states_path = [current_node]
        actions_path = []

        while True:
            successors = list(self.G.successors(current_node))
            if not successors:
                break

            max_weight = -float('inf')
            next_node = None
            action_key = None

            for successor in successors:
                for u, v, key, data in self.G.edges(current_node, data=True, keys=True):
                    if v == successor:
                        weight = data['weight']
                        if weight > max_weight:
                            max_weight = weight
                            next_node = successor
                            action_key = key

            if next_node is None:
                break

            states_path.append(next_node)
            actions_path.append(action_key)
            current_node = next_node

        return states_path, actions_path


    def get_previous_actions(self, node):
        previous_actions = []
        current_node = node
        if node == self.root:
            previous_actions = [node]
        else:
            previous_actions = [node]
            while current_node != self.root:
                parent_nodes = list(self.G.predecessors(current_node))
                if parent_nodes:
                    parent_node = parent_nodes[0]
                    previous_actions.append(parent_node)
                    current_node = parent_node
                else:
                    break

            previous_actions.reverse()  # Reverse the list to get root to node order

        return previous_actions


    def visualize_tree(self, states_path, actions_path, planning_time, image_f):
        dot = Digraph()

        # Add all nodes to the graph
        for node in self.G.nodes:
            visits = self.G.nodes[node]['visits']
            win = self.G.nodes[node]['win']
            dot.node(str(node), label=f"Visits: {visits}\n Wins: {win:.6f}", color='black')

        # Add all edges to the graph
        for u, v, key, data in self.G.edges(data=True, keys=True):
            weight = data['weight']
            action = key

            # Highlight the result path in red
            is_in_path = False
            for i in range(len(states_path) - 1):
                if u == states_path[i] and v == states_path[i + 1] and key == actions_path[i]:
                    is_in_path = True
                    break

            if is_in_path:
                dot.edge(str(u), str(v), label=f"{action}\nWeight: {weight:.4f}", color='red', penwidth='2')
            else:
                dot.edge(str(u), str(v), label=f"{action}\nWeight: {weight:.4f}", color='black')

        # Add filtered nodes and edges to the graph with gray color
        for parent_node, child_node, weight in self.filtered_nodes:
            dot.node(str(child_node), label=str(node)[:10]+" ...", color='gray')
            dot.edge(str(parent_node), str(child_node), label=f"{weight:.4f}", color='gray')

        dot.attr(label=f"Planning time: {planning_time:.4f} seconds", fontsize='12', loc='bottom')

        dot.render(image_f, format='png', cleanup=True)
