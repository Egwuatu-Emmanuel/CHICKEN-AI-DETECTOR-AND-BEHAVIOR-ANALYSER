
import math
import time
from itertools import combinations


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

        distance = math.dist(
            self.previous_position,
            position
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

        chicken.update(position)

        if chicken.is_stationary():

            if chicken.stationary_since is None:
                chicken.stationary_since = time.time()

        else:
            chicken.stationary_since = None

        return chicken


class CrowdingAnalyzer:

    def __init__(self, crowding_threshold=50.0):
        self.crowding_threshold = crowding_threshold

    @staticmethod
    def get_center(bbox):
        x1, y1, x2, y2 = bbox

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        return center_x, center_y

    def analyze(self, bounding_boxes):

        chicken_centers = {
            chicken_id: self.get_center(bbox)
            for chicken_id, bbox in bounding_boxes.items()
        }

        crowded_pairs = []
        crowded_chickens = set()

        for (id_a, center_a), (id_b, center_b) in combinations(
            chicken_centers.items(), 2
        ):

            distance = math.dist(center_a, center_b)

            if distance < self.crowding_threshold:

                crowded_pairs.append({
                    "chicken_a": id_a,
                    "chicken_b": id_b,
                    "distance": distance
                })

                crowded_chickens.add(id_a)
                crowded_chickens.add(id_b)

        return {
            "is_crowded": len(crowded_pairs) > 0,
            "crowded_pairs": crowded_pairs,
            "crowded_chickens": list(crowded_chickens),
            "chicken_count": len(chicken_centers)
        }
