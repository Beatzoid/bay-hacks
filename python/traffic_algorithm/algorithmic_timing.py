import numpy as np
from Networks import NeuralNetwork
from tqdm import tqdm

import sys
sys.path.insert(1, '/Users/christophermao/Documents/GitHub/bay-hacks/python/environment')

from traffic import intersection

env = intersection()
obs, _ = env.reset()
sum_of_sum_reward = 0

# Idea: Find most num of cars on a street and turn lights for that street

for i in tqdm(range(100)):
    done = False
    sum_reward = 0
    while not done:
        # print(obs)
        max = np.argmax(obs)
        action = 0
        if max % 2 == 0 and obs[-1] == 0:
            action = 1
        elif obs[-1] == 1:
            action = 1
        
        observation, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        sum_reward += reward


    # print(sum_reward/100)
    sum_of_sum_reward += sum_reward
print("final sum avg rew:", sum_of_sum_reward/(100 * 100))

