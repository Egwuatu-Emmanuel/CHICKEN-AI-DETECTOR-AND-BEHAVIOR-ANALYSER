
import time


class AlertManager:

    def __init__(
        self,
        stationary_threshold=10.0,
        alert_cooldown=30.0
    ):

        self.stationary_threshold = stationary_threshold

        self.alert_cooldown = alert_cooldown

        self.last_alerts = {}

    def check_chicken(self, chicken):

        duration = chicken.stationary_duration()

        if duration < self.stationary_threshold:
            return None

        alert_key = ("stationary", chicken.chicken_id)

        now = time.time()

        last_alert = self.last_alerts.get(alert_key)

        if last_alert is not None:
            if now - last_alert < self.alert_cooldown:
                return None

        self.last_alerts[alert_key] = now

        return (
            f"Unusual inactivity detected for "
            f"Chicken #{chicken.chicken_id}"
        )

    def check_crowding(self, crowding_result):

        if not crowding_result["is_crowded"]:
            return None

        now = time.time()

        alert_key = ("crowding", "group")

        last_alert = self.last_alerts.get(alert_key)

        if last_alert is not None:
            if now - last_alert < self.alert_cooldown:
                return None

        self.last_alerts[alert_key] = now

        alerts = []

        for pair in crowding_result["crowded_pairs"]:

            chicken_a = pair["chicken_a"]
            chicken_b = pair["chicken_b"]
            distance = pair["distance"]

            alerts.append(
                f"Chickens #{chicken_a} and #{chicken_b} "
                f"are crowded together "
                f"(distance: {distance:.2f} pixels)"
            )

        return alerts
