class TrackingEnemy():
    def __init__(self):
        self.killed = 0
    def count(self):
        self.killed += 1
    def reset(self):
        self.killed = 0