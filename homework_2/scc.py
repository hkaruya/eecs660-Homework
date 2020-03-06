import sys
import numpy as np

class Node:
    def __init__(self, new_label=''):
        self.label = new_label
        self._edges = []
    def __repr__(self):
        return 'Node(' + self.label + ')'
    def __str__(self):
        return 'Node()'
    def __eq__(self, other):
        return (self.label == other.label)
    def addEdge(self, new_edge):
        if isinstance(new_edge, Node):
            if new_edge not in self._edges:
                self._edges.append(new_edge)
    def getNextNode(self, index=0):
        if (not self.isEmpty()) and index < self.getNumberOfEdges():
            return self._edges[index]
    def getNumberOfEdges(self):
        return len(self._edges)
    def getLabel(self):
        return self.label
    def isEmpty(self):
        return (0 == self.getNumberOfEdges())

def generateGraph(filename):
    G = []
    G_transpose = []
    with open(filename, 'r') as reader:
        lines = reader.readlines()
        node_count = int(lines[0])

    destinations = lines[2:]
    while node_count != len(destinations):
        size_of_destinations = len(destinations)

        if node_count < size_of_destinations:
            destinations.pop()
        else:
            destinations.append('\n')

    G = [ Node(str(i+1)) for i in range(0, node_count) ]
    G_transpose = [ Node(str(i+1)) for i in range(0, node_count) ]

    for i in range(0, node_count):
        if '\n' == destinations[i]:
            destinations[i] = np.array([-1])
        else:
            destinations[i] = np.fromstring(destinations[i], dtype=int, sep=' ')

        _generateEdges((i + 1), destinations[i], G, G_transpose)

    return [node_count, G, G_transpose]

def _generateEdges(origin, destinations, graph, graph_transpose):
    number_of_destinations = len(destinations)
    if 1 == number_of_destinations and -1 == destinations[0]:
        return

    for i in range(0, number_of_destinations):
        destination = destinations[i]
        graph[origin - 1].addEdge(graph[destination - 1])
        graph_transpose[destination - 1].addEdge(graph_transpose[origin - 1])

def findSCC(node_count, graph, graph_transpose):
    last_discovered = _DFSLastDiscovered(node_count, graph_transpose)
    return _DFSPathTaken(node_count, last_discovered, graph)

def _DFSLastDiscovered(node_count, graph):
    time = 0
    undiscovered_nodes_count = node_count

    dfs_stack = []

    found_node_status = [ False for i in range(0, node_count) ]
    node_timer = [ ((i+1), time, time) for i in range(0, node_count) ]

    current_node = 0
    while (0 != len(dfs_stack)) or (0 != undiscovered_nodes_count):
        if not found_node_status[current_node]:
            found_node_status[current_node] = True

            time += 1
            undiscovered_nodes_count -=1

            node_timer[current_node] = ((current_node + 1), time, 0)

        potential_next = -1
        number_of_edges = graph[current_node].getNumberOfEdges()

        for i in range(0, number_of_edges):
            node_prime = graph[current_node].getNextNode(i)
            checker = int(node_prime.getLabel()) - 1

            if not found_node_status[checker]:
                potential_next = checker
                break

        if -1 != potential_next:
            dfs_stack.append(current_node)
            current_node = potential_next
        else:
            time +=1
            discovery_time = node_timer[current_node][1]
            node_timer[current_node] = ((current_node + 1), discovery_time, time)

            stack_size = len(dfs_stack)
            if 0 == stack_size:
                for i in range(0, node_count):
                    if not found_node_status[i]:
                        current_node = i
                        break
            else:
                current_node = dfs_stack.pop()
                if (0 == stack_size - 1) and (0 == undiscovered_nodes_count):
                    discovery_time = node_timer[current_node][1]
                    node_timer[current_node] = ((current_node + 1), discovery_time, (time + 1))

    sorted_times = sorted(node_timer, key=lambda x: x[2])

    return [sorted_times[i][0] for i in range(0, node_count)]


def _DFSPathTaken(node_count, stack, graph):
    if [] == stack:
        return []

    undiscovered_nodes_count = node_count

    dfs_stack = []
    visiting_queue = stack

    found_node_status = [ False for i in range(0, node_count) ]
    paths_taken = []

    current_node = visiting_queue.pop() - 1
    current_path = [current_node + 1]
    while (0 != len(dfs_stack)) or (0 != undiscovered_nodes_count):
        if not found_node_status[current_node]:
            found_node_status[current_node] = True
            undiscovered_nodes_count -=1

        potential_next = -1
        number_of_edges = graph[current_node].getNumberOfEdges()

        for i in range(0, number_of_edges):
            node_prime = graph[current_node].getNextNode(i)
            checker = int(node_prime.getLabel()) - 1

            if not found_node_status[checker]:
                potential_next = checker
                break

        if -1 != potential_next:
            dfs_stack.append(current_node)
            current_node = potential_next

            current_path.append(current_node + 1)
        else:
            stack_size = len(dfs_stack)
            if 0 == stack_size:
                current_path.sort()
                paths_taken.append(current_path)

                if 0 != len(visiting_queue):
                    next_in_queue = visiting_queue.pop() - 1
                    while found_node_status[next_in_queue]:
                        next_in_queue = visiting_queue.pop() - 1

                    current_node = next_in_queue
                    current_path = [current_node + 1]
            else:
                current_node = dfs_stack.pop()
                if (0 == stack_size - 1) and (0 == undiscovered_nodes_count):
                    current_path.sort()
                    paths_taken.append(current_path)

    return sorted(paths_taken, key=lambda x: x[0])

def formatForGrading(strongly_connected_components):
    for component_list in strongly_connected_components:
        number_of_scc = len(component_list)
        for i in range(0, number_of_scc):
            if i != (number_of_scc - 1):
                print(component_list[i], end=' ')
            else:
                print(component_list[i], end='\n')

number_of_args = len(sys.argv)
if 0 != number_of_args:
    for i in range(1, number_of_args):
        [number_of_nodes, G, G_t] = generateGraph(sys.argv[i])
        scc = findSCC(number_of_nodes, G, G_t)

        formatForGrading(scc)

