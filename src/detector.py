from pathlib import Path

from huggingface_hub import hf_hub_download
from ultralytics import YOLO

from .config import (
    HF_REPO_ID,
    HF_MODEL_FILENAME,
)


class ChickenDetector:
    """
    Loads the chicken-specific YOLO model and
    provides a simple interface for inference.
    """

    def __init__(self):
        print("Downloading/loading chicken model...")

        model_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_MODEL_FILENAME
        )

        print(f"Model path: {model_path}")

        self.model = YOLO(model_path)

        print("Model loaded successfully.")

        print("Model classes:")
        print(self.model.names)

    def detect(self, frame, confidence=0.35):
        """
        Run chicken detection on a single image/frame.
        """

        results = self.model(
            frame,
            conf=confidence,
            verbose=False
        )

        return results