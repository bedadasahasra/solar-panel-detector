import json
import os


def save_output(sample_id, lat, lon, results):
    os.makedirs("predictions", exist_ok=True)

    has_solar = len(results[0].boxes) > 0

    if has_solar:
        confidence = float(results[0].boxes.conf.max().item())
        area_est_sqm = 10.0   # placeholder, okay for prototype
        bbox = results[0].boxes.xyxy.tolist()
    else:
        confidence = 0.0
        area_est_sqm = 0.0
        bbox = []

    data = {
        "sample_id": int(sample_id),
        "lat": float(lat),
        "lon": float(lon),
        "has_solar": has_solar,
        "confidence": confidence,
        "pv_area_sqm_est": area_est_sqm,
        "buffer_radius_sqft": 1200,
        "qc_status": "VERIFIABLE",
        "bbox_or_mask": json.dumps(bbox),
        "image_metadata": {
            "source": "Google Static Maps",
            "capture_date": "unknown"
        }
    }

    with open(f"predictions/{sample_id}.json", "w") as f:
        json.dump(data, f, indent=4)