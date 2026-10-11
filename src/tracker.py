class ChickenTracker:

    def __init__(self, detector):
        self.detector = detector

    def track(self, frame, confidence=0.75):
        """
        Run detection + object tracking on the frame.
        """

        results = self.detector.model.track(
            source=frame,
            # conf=confidence,
            # persist=True,
           
            verbose=False,
            # source="poultry_cam.mp4",
             tracker="bytetrack.yaml",  # Explicitly switch from default BoT-SORT to ByteTrack
             conf=0.10,                 # Drop the initial check low to catch occluded chickens
             iou=0.5,                   # Slightly tighter NMS threshold to handle overlapping birds
             persist=True
        )

        return results