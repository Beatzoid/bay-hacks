from Networks import NeuralNetwork

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/Users/christophermao/Documents/GitHub/bay-hacks/python/environment')

from traffic import intersection

env = intersection()
env.reset()
sum_of_sum_reward = 0

for i in range(100):
    done = False
    sum_reward = 0
    timestep = 0
    while not done:
        timestep += 1
        if timestep % 5:
            observation, reward, done = env.step(1.0)
        else:
            observation, reward, done = env.step(0.0)
        sum_reward += reward
        # print(observation, reward, done)
        # print(sum_reward)

    print(sum_reward/100)
    sum_of_sum_reward += sum_reward
print("final sum avg rew:" sum_of_sum_reward/(100 * 100))

