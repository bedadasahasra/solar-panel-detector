Solar-Panel-Detector — quick usage

This repository contains a small pipeline to fetch satellite images for coordinates and run a YOLO detector to detect solar panels.

Quick start

1. Generate `input.xlsx` from the provided `input.csv` (script included):

   PowerShell:

   ```powershell
   python scripts\generate_input_xlsx.py
   ```

   If you see an error about missing Excel engines, install `openpyxl`:

   ```powershell
   python -m pip install openpyxl
   ```

2. Run the pipeline using the Excel input (or pass `--input` to point to a CSV/Excel file):

   ```powershell
   python pipeline\main.py --input input.xlsx
   ```

Environment variables (optional)

- `SAT_API_PROVIDER`: If set to `mapbox`, the `SAT_API_KEY` will be used to fetch Mapbox static satellite tiles.
- `SAT_API_KEY`: API key for the configured provider.

Example: using Mapbox (PowerShell):

```powershell
$env:SAT_API_PROVIDER = 'mapbox'
$env:SAT_API_KEY = '<your_mapbox_token>'
python pipeline\main.py --input input.xlsx
```

Notes

- If a local `model/best.pt` is missing or invalid the pipeline will fall back to the pretrained `yolov8n.pt` and download it automatically.
- The pipeline writes JSON predictions to the `predictions/` folder named `{sample_id}.json`.
- If image downloads fail, a placeholder image is written so the pipeline can continue (useful for offline testing).

If you want, I can also add an example `input.xlsx` directly to the repo instead of generating it from `input.csv`. Let me know.