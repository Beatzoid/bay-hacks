import random
import numpy as np

class intersection():
    def __init__(self) -> None:
        pass

    def reset(self, seed=0):
        self.seed = seed
        self.num_cars = [0, 0, 0, 0, 0] # extra for lightvalue
        self.car_timers = [0.0, 0.0, 0.0, 0.0]
        self.light_value = 0 # 0 is green light one way and the reverse
        self.reward = 0
        self.timestep = 0
        self.done = False

        return np.array(self.num_cars), 0



    def step(self, action):
        self.reward = 0.5
        spawn_car = random.random() < 0.5
        if spawn_car:
            self.num_cars[random.randint(0, 3)] += random.randint(0, 4)
        
        # print(action)
        if action > 0.5: 
            self.light_value = 1 - self.light_value
        
        if self.light_value == 0: # Controling light values
            self.num_cars[1] -= 1
            self.num_cars[3] -= 1
        elif self.light_value == 1:
            self.num_cars[0] -= 1
            self.num_cars[2] -= 1
        else:
            print("uh oh")
        
        # make num cars not equal 0 and make sure that the light actually lets cars through and there wasn't no cars
        for i in range(len(self.num_cars)):
            if self.num_cars[i] < 0:
                self.reward -= 0.25
                self.num_cars[i] = 0

        # car timers for reward system
        for count, i in enumerate(self.num_cars):
            if count > 3:
                break
            if i != 0:
                self.car_timers[count] += .5 * self.num_cars[count]
            else:
                self.car_timers[count] = 0
        
        self.reward -= sum(self.car_timers)

        self.timestep += 1

        if self.timestep > 100:
            self.done = True
        
        self.num_cars[-1] = self.light_value
        return np.array(self.num_cars), self.reward, self.done, False, 0
        
    def render(self):
        pass

    def close(self):
        pass
