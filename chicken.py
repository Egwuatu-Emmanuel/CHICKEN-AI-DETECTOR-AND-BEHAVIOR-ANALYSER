from huggingface_hub import hf_hub_download
from ultralytics import YOLO

# Hugging Face repository
repo_id = "IceKhoffi/chicken-object-detection-yolov11s"
filename = "yolov11s.pt"

# Download model
model_path = hf_hub_download(
    repo_id=repo_id,
    filename=filename
)

print("Model downloaded to:")
print(model_path)

# Load model
model = YOLO(model_path)

# Show what classes the model knows
print("\nModel classes:")
print(model.names)

# Run inference
results = model(
    "chicken.jpg",
    conf=0.25,
    save=True
)

# Examine detections
for result in results:

    print("\nDetections:")

    if result.boxes is None:
        print("No detections.")
        continue

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        print(
            f"Class: {class_id} "
            f"({model.names[class_id]}) "
            f"Confidence: {confidence:.3f}"
        )