import time


class AlertManager:

    def __init__(self, stationary_threshold=10.0):

        self.stationary_threshold = stationary_threshold

        self.last_alerts = {}

        self.alert_cooldown = 30.0

    def check_chicken(self, chicken):

        duration = chicken.stationary_duration()

        if duration < self.stationary_threshold:
            return None

        last_alert = self.last_alerts.get(
            chicken.chicken_id
        )

        now = time.time()

        if last_alert is not None:

            if now - last_alert < self.alert_cooldown:
                return None

        self.last_alerts[chicken.chicken_id] = now

        return (
            f"Unusual inactivity detected for "
            f"Chicken #{chicken.chicken_id}"
        )