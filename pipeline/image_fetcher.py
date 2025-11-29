import os
import time
import requests
from typing import Optional

try:
    from PIL import Image
except Exception:
    Image = None

# Candidate sample images to try when no API key/provider is configured
SAMPLE_IMAGE_URLS = [
    "https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57730/world.topo.bathy.200412.3x5400x2700.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/60/Blue_Marble_2002.png",
]


def _download_with_retries(url: str, retries: int = 3, backoff: float = 1.0) -> Optional[bytes]:
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.content
            else:
                print(f"Download failed (status {resp.status_code}) for {url}")
        except Exception as e:
            print(f"Attempt {attempt} failed for {url}: {e}")
        time.sleep(backoff * attempt)
    return None


def _write_placeholder_image(path: str, size=(512, 512)):
    if Image is None:
        # If PIL isn't available, write an empty file to signal failure
        open(path, "wb").close()
        return
    img = Image.new("RGB", size, color=(200, 200, 200))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def fetch_image(lat, lon, output_path):
    """Fetch a satellite image for the given lat/lon.

    Behavior:
    - If `SAT_API_PROVIDER` and `SAT_API_KEY` are provided, attempt to use the provider (currently supports 'mapbox').
    - Otherwise try a list of free sample images.
    - If all downloads fail, write a placeholder image so the pipeline can continue.
    """
    provider = os.environ.get("SAT_API_PROVIDER")
    api_key = os.environ.get("SAT_API_KEY")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if provider == "mapbox" and api_key:
        # Mapbox Static Tiles API (satellite-v9)
        try:
            zoom = 16
            width = 512
            height = 512
            url = (
                f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
                f"{lon},{lat},{zoom}/{width}x{height}?access_token={api_key}"
            )
            print(f"Fetching image from Mapbox for {lat},{lon}...")
            data = _download_with_retries(url)
            if data:
                with open(output_path, "wb") as f:
                    f.write(data)
                print(f"Image saved to {output_path}")
                return
            else:
                print("Mapbox download failed, falling back to sample images.")
        except Exception as e:
            print(f"Mapbox fetch error: {e}")

    print("No provider/API configured or provider failed. Trying sample images...")
    # If an offline sample image exists in pipeline/examples, use it directly (deterministic offline mode)
    sample_local = os.path.join(os.path.dirname(__file__), "examples", "sample_satellite.jpg")
    if os.path.exists(sample_local):
        print(f"Using local sample image {sample_local} for {lat},{lon}")
        with open(sample_local, "rb") as src, open(output_path, "wb") as dst:
            dst.write(src.read())
        print(f"Image saved to {output_path}")
        return

    for url in SAMPLE_IMAGE_URLS:
        data = _download_with_retries(url)
        if data:
            with open(output_path, "wb") as f:
                f.write(data)
            print(f"Image saved to {output_path}")
            return

    print("All downloads failed — writing placeholder image so pipeline can continue.")
    _write_placeholder_image(output_path)