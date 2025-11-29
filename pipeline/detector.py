
import os

def load_model(path="model/best.pt"):
    """Load a YOLO model. Import ultralytics lazily so tests/CI can mock this function without installing heavy deps.

    If the local file doesn't exist or is suspiciously small, falls back to the pretrained `yolov8n.pt`.
    """
    try:
        # import inside function to avoid requiring ultralytics at module import time
        from ultralytics import YOLO
    except Exception:
        raise RuntimeError("ultralytics package is required to load models. Install it or mock `load_model` in tests.")

    # If the local file doesn't exist or is suspiciously small, fall back to a pretrained model
    try:
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            print(f"Local weights '{path}' missing or too small; falling back to 'yolov8n.pt' pretrained weights.")
            return YOLO("yolov8n.pt")
        return YOLO(path)
    except Exception as e:
        print(f"Failed to load local weights '{path}': {e}\nFalling back to 'yolov8n.pt'.")
        return YOLO("yolov8n.pt")

def run_inference(model, image_path):
    results = model.predict(image_path)
    return results