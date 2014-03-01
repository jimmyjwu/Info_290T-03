"""
Utilities to calculate errors and new weights in the neural network
from lecture.
"""

# Constants
LEARNING_RATE = 10
OUTPUT_NODE = 6
HIDDEN_NODES = [3, 4, 5]

actual_output_for_node = {
	1: 1.0,
	2: 2.0,
	3: 0.7311,
	4: 0.0179,
	5: 0.9933,
	6: 0.8387,
}

expected_output_for_node = {
	6: 0.0,
}

weight_between_nodes = {
	(1, 3): -3.0,
	(1, 4): 2.0,
	(1, 5): 4.0,
	(2, 3): 2.0,
	(2, 4): -3.0,
	(2, 5): 0.5,
	(3, 6): 0.2,
	(4, 6): 0.7,
	(5, 6): 1.5,
}

error_for_node = {}


# Utility functions
def output_error():
	"""
	Calculates the error in a node's output.
	Intuitively, error is
		[y - f(x)]f'(x) = [y - f(x)][1 - f(x)]f(x)
	where
		y := expected output
		f(x) := actual output of logistic/sigmoid function on input x
	"""
	actual = actual_output_for_node[OUTPUT_NODE]
	expected = expected_output_for_node[OUTPUT_NODE]
	return (expected - actual) * (1 - actual) * actual

def hidden_node_error(node_i, nodes_j):
	"""
	Calculates the error of a node i in a hidden layer
	that has directed edges to nodes j.
	"""
	output_i = actual_output_for_node[node_i]
	return output_i * (1 - output_i) * sum([error_for_node[j] * weight_between_nodes[(node_i, j)] for j in nodes_j])

def new_weight(i, j):
	"""
	Calculates the new weight for edge (i, j).
	"""
	return weight_between_nodes[(i, j)] + LEARNING_RATE * error_for_node[j] * actual_output_for_node[i]


# Calculate output and hidden node errors
error_for_node[OUTPUT_NODE] = output_error()
[error_for_node.setdefault(node, hidden_node_error(node, [OUTPUT_NODE])) for node in HIDDEN_NODES]

# Calculate new weights
new_hidden_weights = {(i, j): new_weight(i, j) for i, j in weight_between_nodes.keys()}


# Print results
for node in HIDDEN_NODES + [OUTPUT_NODE]:
	print 'Error for node ' + str(node) + ': ' + str(error_for_node[node])











