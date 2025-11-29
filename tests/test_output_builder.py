import json
import os
from pipeline.output_builder import save_output


class DummyBoxes:
    def __init__(self):
        # single box [x1,y1,x2,y2]
        self.xyxy = [[10, 10, 50, 30]]
        self.conf = [0.9]
        self.cls = [0]


class DummyResult:
    def __init__(self):
        self.boxes = DummyBoxes()


def test_save_output_creates_json(tmp_path, monkeypatch):
    out_dir = tmp_path / "predictions"
    # monkeypatch predictions folder location by changing cwd
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        save_output('test1', 1.0, 2.0, [DummyResult()])
        f = out_dir / "test1.json"
        assert f.exists()
        data = json.loads(f.read_text())
        assert data["sample_id"] == "test1"
        assert data["has_solar"] is True
        assert "detections" in data
        assert len(data["detections"]) == 1
    finally:
        os.chdir(cwd)
