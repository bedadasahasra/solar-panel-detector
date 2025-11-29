import argparse
import os
import pandas as pd
from detector import load_model, run_inference
from image_fetcher import fetch_image
from output_builder import save_output


def main(input_path: str):
    # If the provided path doesn't exist, try a few common fallbacks
    if not os.path.exists(input_path):
        fallbacks = ["input.xlsx", "input code.xlsx", "input.csv"]
        found = None
        for f in fallbacks:
            if os.path.exists(f):
                found = f
                break
        if found:
            input_path = found
            print(f"Using fallback input file: {input_path}")
        else:
            raise FileNotFoundError(
                f"Input file not found. Tried '{input_path}' and fallbacks: {', '.join(fallbacks)}.\n"
                "Create one or pass --input <path> to the script."
            )

    # Load spreadsheet or CSV depending on extension
    if input_path.lower().endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    model = load_model("model/best.pt")

    # Normalize column names to help tolerate input variations
    cols = {c: c.lower().strip() for c in df.columns}
    df = df.rename(columns=cols)

    # Find best matching column names for required fields
    def find_col(key_parts):
        for c in df.columns:
            for part in key_parts:
                if part in c:
                    return c
        return None

    sample_col = find_col(["sample", "sampl", "id"])
    lat_col = find_col(["lat"])
    lon_col = find_col(["lon", "lng", "long"])

    if not sample_col or not lat_col or not lon_col:
        raise ValueError(f"Required columns not found. Found columns: {list(df.columns)}.\n"
                         f"Expected something like 'sample_id', 'latitude', 'longitude'.")

    for _, row in df.iterrows():
        sample_id = row.get(sample_col)
        lat = row.get(lat_col)
        lon = row.get(lon_col)

        if pd.isna(sample_id) or pd.isna(lat) or pd.isna(lon):
            print(f"Skipping row due to missing fields: {row.to_dict()}")
            continue

        image_path = f"artifacts/{sample_id}_image.jpg"
        fetch_image(lat, lon, image_path)

        if not os.path.exists(image_path):
            print(f"Image for sample {sample_id} not available, skipping.")
            continue

        results = run_inference(model, image_path)

        save_output(sample_id, lat, lon, results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline using an input spreadsheet (Excel or CSV).")
    parser.add_argument("--input", "-i", default="input.xlsx", help="Path to input Excel/CSV file (default: input.xlsx)")
    args = parser.parse_args()
    main(args.input)