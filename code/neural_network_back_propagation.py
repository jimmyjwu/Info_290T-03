"""
Utilities to calculate errors and new weights in the neural network
from lecture.
"""

# Learning rate
l = 10

nodes_and_outputs = [
	# (1, 1),
	# (2, 2),
	(3, 0.7311),
	(4, 0.0179),
	(5, 0.9933),
	(6, 0.8387),
]
output_for_node = {node: output for node, output in nodes_and_outputs}

weights_between_nodes = {
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

def error(actual, expected):
	"""
	Calculates the error in a node's output.
	Intuitively, error is
		Δf(x)f'(x) = [y - f(x)][1 - f(x)]f(x)
	where
		y := expected output
		f(x) := actual output of logistic/sigmoid function on input x
	"""
	actual, expected = float(actual), float(expected)
	return (expected - actual) * (1 - actual) * actual

def new_weight(weight_ij, error_j, output_i, learning_rate=l):
	"""
	Calculates the new weight for edge (i, j).
	"""
	return weight_ij + learning_rate * error_j * output_i














