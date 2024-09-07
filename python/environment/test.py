from traffic import intersection
import random

env = intersection()
env.reset()
done = False
sum_reward = 0
while not done:
    observation, reward, done, term, inf = env.step(random.randint(0, 1))
    observation = observation / 10
    print(observation, reward, done)
    sum_reward += reward
    print(sum_reward)

print(sum_reward/100)