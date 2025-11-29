import os
import shutil
from pipeline import image_fetcher
from pathlib import Path


def test_fetch_uses_local_sample(tmp_path):
    # ensure sample exists
    sample_local = Path(image_fetcher.__file__).parent / "examples" / "sample_satellite.jpg"
    assert sample_local.exists(), "sample_satellite.jpg must exist for offline tests"

    out = tmp_path / "out.jpg"
    image_fetcher.fetch_image(0, 0, str(out))
    assert out.exists()
    assert out.stat().st_size > 0

    # cleanup
    out.unlink()
