from Networks import NeuralNetwork

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'python/environment/')

from traffic import intersection

network = NeuralNetwork(4, 0.001)
env = intersection()

