import math
import time


class ChickenState:

    def __init__(self, chicken_id):
        self.chicken_id = chicken_id

        self.previous_position = None

        self.total_distance = 0.0

        self.current_speed = 0.0

        self.last_seen = time.time()

        self.stationary_since = None

    def update(self, position):
        now = time.time()

        self.last_seen = now

        if self.previous_position is None:
            self.previous_position = position
            return

        previous_x, previous_y = self.previous_position
        current_x, current_y = position

        distance = math.sqrt(
            (current_x - previous_x) ** 2 +
            (current_y - previous_y) ** 2
        )

        self.total_distance += distance

        self.current_speed = distance

        self.previous_position = position

    def is_stationary(self, threshold=20.0):

        return self.current_speed < threshold

    def stationary_duration(self):

        if self.stationary_since is None:
            return 0.0

        return time.time() - self.stationary_since


class BehaviorAnalyzer:

    def __init__(self):
        self.chickens = {}

    def update_chicken(self, chicken_id, position):

        if chicken_id not in self.chickens:

            self.chickens[chicken_id] = ChickenState(
                chicken_id
            )

        chicken = self.chickens[chicken_id]

        was_stationary = chicken.is_stationary()

        chicken.update(position)

        is_stationary = chicken.is_stationary()

        if is_stationary:

            if chicken.stationary_since is None:
                chicken.stationary_since = time.time()

        else:

            chicken.stationary_since = None

        return chicken