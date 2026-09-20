from pathlib import Path


# ---------------------------------------------------------
# PROJECT DIRECTORIES
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

RECORDINGS_DIR = DATA_DIR / "recordings"
DATABASE_DIR = DATA_DIR / "database"


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------

HF_REPO_ID = "IceKhoffi/chicken-object-detection-yolov11s"
HF_MODEL_FILENAME = "yolov11s.pt"


# ---------------------------------------------------------
# CAMERA
# ---------------------------------------------------------

CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720


# ---------------------------------------------------------
# DETECTION
# ---------------------------------------------------------

CONFIDENCE_THRESHOLD = 0.35


# ---------------------------------------------------------
# TRACKING
# ---------------------------------------------------------

TRACKER_CONFIG = "bytetrack.yaml"


# ---------------------------------------------------------
# BEHAVIOR
# ---------------------------------------------------------

STATIONARY_SPEED_THRESHOLD = 20.0

STATIONARY_TIME_THRESHOLD = 10.0


# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

WINDOW_NAME = "Poultry AI Monitor"


# ---------------------------------------------------------
# CREATE REQUIRED DIRECTORIES
# ---------------------------------------------------------

MODEL_DIR.mkdir(parents=True, exist_ok=True)

RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_DIR.mkdir(parents=True, exist_ok=True)