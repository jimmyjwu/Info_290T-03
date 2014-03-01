"""
Utilities to calculate errors and new weights in the neural network
from lecture.
"""

# Constants
LEARNING_RATE = 10
OUTPUT_NODE = 6
HIDDEN_NODES = [3, 4, 5]

actual_output_for_node = {
	# 1: 1,
	# 2: 2,
	3: 0.7311,
	4: 0.0179,
	5: 0.9933,
	6: 0.8387,
}

expected_output_for_node = {
	6: 0,
}

weight_between_nodes = {
	(1, 3): -3,
	(1, 4): 2,
	(1, 5): 4,
	(2, 3): 2,
	(2, 4): -3,
	(2, 5): 0.5,
	(3, 6): 0.2,
	(4, 6): 0.7,
	(5, 6): 1.5,
}

def output_error(actual, expected):
	"""
	Calculates the error in a node's output.
	Intuitively, error is
		[y - f(x)]f'(x) = [y - f(x)][1 - f(x)]f(x)
	where
		y := expected output
		f(x) := actual output of logistic/sigmoid function on input x
	"""
	actual, expected = float(actual), float(expected)
	return (expected - actual) * (1 - actual) * actual

def hidden_layer_error(output_j, errors_k_and_weights_jk):
	"""
	Calculates the error of a node in a hidden layer
	that has directed edges to nodes k.
	"""
	return output_j * (1 - output_j) * sum([error_k * weight_jk for error_k, weight_jk in errors_k_and_weights_jk])

def new_weight(weight_ij, error_j, output_i):
	"""
	Calculates the new weight for edge (i, j).
	"""
	return weight_ij + LEARNING_RATE * error_j * output_i


# Calculate output and hidden node errors
output_node_error = output_error(actual_output_for_node[OUTPUT_NODE], expected_output_for_node[OUTPUT_NODE])
error_for_hidden_node = {node: hidden_layer_error(actual_output_for_node[node], [(output_node_error, weight_between_nodes[(node, OUTPUT_NODE)])]) for node in HIDDEN_NODES}



# Print results
print 'Error for node ' + str(OUTPUT_NODE) + ': ' + str(output_node_error)

for node in HIDDEN_NODES:
	print 'Error for node ' + str(node) + ': ' + str(error_for_hidden_node[node])











