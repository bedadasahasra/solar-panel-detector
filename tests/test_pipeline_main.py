import os
from pipeline import main as pipeline_main


class DummyModel:
    def predict(self, image_path):
        # mimic ultralytics result (object with boxes attr)
        class Boxes:
            def __init__(self):
                self.xyxy = [[0, 0, 10, 10]]
                self.conf = [0.5]
                self.cls = [0]

        class Result:
            def __init__(self):
                self.boxes = Boxes()

        return [Result()]


def test_main_runs_with_mocked_model(tmp_path, monkeypatch):
    # copy sample image into pipeline/examples to ensure fetch_image will pick it
    sample_local = os.path.join(os.path.dirname(__import__('pipeline').__file__), 'examples', 'sample_satellite.jpg')
    assert os.path.exists(sample_local), "sample image required"

    # monkeypatch load_model to avoid ultralytics and heavy downloads
    monkeypatch.setattr('pipeline.detector.load_model', lambda path=None: DummyModel())

    # run pipeline main pointing to sample csv created earlier
    input_csv = os.path.join(os.getcwd(), 'input.csv')
    assert os.path.exists(input_csv), 'input.csv must exist for this test'

    # run pipeline
    pipeline_main.main(input_csv)

    # check predictions were written
    import glob
    preds = glob.glob('predictions/*.json')
    assert len(preds) >= 1
