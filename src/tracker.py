class ChickenTracker:

    def __init__(self, detector):
        self.detector = detector

    def track(self, frame, confidence=0.35):
        """
        Run detection + object tracking on the frame.
        """

        results = self.detector.model.track(
            source=frame,
            conf=confidence,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        return results