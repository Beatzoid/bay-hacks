import numpy as np
from Networks import NeuralNetwork
from tqdm import tqdm

import sys
sys.path.insert(1, '/Users/christophermao/Documents/GitHub/bay-hacks/python/environment')

from traffic import intersection

env = intersection()
sum_of_sum_reward = 0

# Idea: Find most num of cars on a street and turn lights for that street
n_eps = 10000

total = 0
count = 0

for i in tqdm(range(n_eps)):
    obs, _ = env.reset()
    done = False
    sum_reward = 0
    while not done:
        # print(obs)

        # V1:
        # max = np.argmax(obs)
        # action = 0
        # if max % 2 == 0 and obs[-1] == 0:
        #     action = 1
        # elif obs[-1] == 1:
        #     action = 1
        
        # V2:
        # print(obs)
        if obs[0] >= 1 and obs[2] >= 1 and obs[-1] == 0:
            action = 1
        elif obs[1] >= 1 and obs[3] >= 1 and obs[-1] == 1:
            acition = -1
        else:
            count += 1
            max = np.argmax(obs)
            action = 0
            if max % 2 == 0 and obs[-1] == 0:
                action = 1
            elif obs[-1] == 1:
                action = 1
        total += 1

        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        sum_reward += reward


    # print(sum_reward/100)
    sum_of_sum_reward += sum_reward
print("final sum avg rew:", sum_of_sum_reward/(n_eps))
print(count / total)
print(1 - (count / total))
