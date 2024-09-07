import random

class intersection():
    def __init__(self) -> None:
        pass

    def reset(self):
        self.num_cars = [0, 0, 0, 0]
        self.car_timers = [0.0, 0.0, 0.0, 0.0]
        self.light_value = 0 # 0 is green light one way and the reverse
        self.reward = 0
        self.timestep = 0
        self.done = False



    def step(self, action):
        self.reward = 0
        spawn_car = random.random() < 0.5
        if spawn_car:
            self.num_cars[random.randint(0, 3)] += random.randint(0, 2)
        
        if action: 
            self.light_value = 1 - self.light_value
        
        if self.light_value == 0: # Controling light values
            self.num_cars[1] -= 1
            self.num_cars[3] -= 1
            self.reward += .5
        else:
            self.num_cars[0] -= 1
            self.num_cars[2] -= 1
            self.reward += .5
        
        # make num cars not equal 0 and that the light actually let cars through
        for i in range(len(self.num_cars)):
            if self.num_cars[i] < 0:
                self.reward -= 0.25
                self.num_cars[i] = 0

        # car timers for reward system
        for count, i in enumerate(self.num_cars):
            if i != 0:
                self.car_timers[count] += .05 * self.num_cars[count]
            else:
                self.car_timers[count] = 0
        
        self.reward -= sum(self.car_timers)

        self.timestep += 1

        if self.timestep > 100:
            self.done = True
        
        return [self.num_cars, self.car_timers], self.reward, self.done
        

    def close(self):
        pass
