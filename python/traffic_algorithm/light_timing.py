from Networks import NeuralNetwork
from tqdm import tqdm
import sys
sys.path.insert(1, '/Users/christophermao/Documents/GitHub/bay-hacks/python/environment')

from traffic import intersection

env = intersection()
sum_of_sum_reward = 0
n_eps = 10000
total = 0
change = 0
for i in tqdm(range(n_eps)):
    done = False
    sum_reward = 0
    timestep = 0
    env.reset()
    while not done:
        if timestep % 10 == 0:
            observation, reward, terminated, truncated, _ = env.step(1.0)
            change += 1
        else:
            observation, reward, terminated, truncated, _ = env.step(0.0)
        total += 1
        sum_reward += reward
        timestep += 1
        done = terminated or truncated

    sum_of_sum_reward += sum_reward
print("final sum avg rew:", sum_of_sum_reward/(n_eps))
print(change / total)

