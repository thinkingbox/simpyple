import simpy


class Line(object):
    # y = s * x + k
    # s = (y1 - yo) / (x1 - x0)
    # k = y0 - s * x0
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.slope = (self.y1 - self.y0) / (self.x1 - self.x0)
        self.displacement = self.y0 - self.slope * self.x0
        
    def value(self, x):     
        return self.slope * x + self.displacement


class Schedule(object):
    def __init__(self, ramp_quantity, full_load_quantity, slow_rate, fast_rate):
        self.ramp_quantity = ramp_quantity
        self.full_load_quantity = full_load_quantity
        self.slow_rate = slow_rate
        self.fast_rate = fast_rate
        self.time = 0

    def next(self, index):
        if 0 <= index and index < self.ramp_quantity:
            delay = Line(0, self.slow_rate, self.ramp_quantity - 1, self.fast_rate).value(index)
            self.ramp_up = self.time + delay
        elif self.ramp_quantity <= index and index < self.ramp_quantity + self.full_load_quantity:
            delay = self.fast_rate
            self.full_load = self.time + delay
        else:
            delay = Line(self.ramp_quantity + self.full_load_quantity, self.fast_rate, self.ramp_quantity * 2 + self.full_load_quantity, self.slow_rate).value(index)
            self.ramp_down = self.time + delay
        self.time += delay
        return self.time
    
