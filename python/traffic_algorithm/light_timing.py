from Networks import NeuralNetwork
from tqdm import tqdm
import sys
sys.path.insert(1, '/Users/christophermao/Documents/GitHub/bay-hacks/python/environment')

from traffic import intersection

env = intersection()
env.reset()
sum_of_sum_reward = 0
n_eps = 100000
for i in tqdm(range(n_eps)):
    done = False
    sum_reward = 0
    timestep = 0
    while not done:
        timestep += 1
        if timestep % 100:
            observation, reward, terminated, truncated, _ = env.step(1.0)
        else:
            observation, reward, terminated, truncated, _ = env.step(0.0)
        sum_reward += reward
        done = terminated or truncated

    sum_of_sum_reward += sum_reward
print("final sum avg rew:", sum_of_sum_reward/(n_eps))

