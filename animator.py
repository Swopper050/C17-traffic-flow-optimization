class Animator:
    def __init__(self, fig, ax, G, n_cars=1):
        self.fig = fig
        self.ax = ax
        self.G = G
        self.n_cars = n_cars
        self.init()

    def init(self):
        self.cars = [Car() for _ in range(n_cars)]


