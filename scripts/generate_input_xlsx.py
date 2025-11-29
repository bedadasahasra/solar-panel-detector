import pandas as pd
import sys

csv_path = "input.csv"
xlsx_path = "input.xlsx"

try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Failed to read {csv_path}: {e}")
    sys.exit(1)

try:
    df.to_excel(xlsx_path, index=False)
    print(f"Created {xlsx_path} from {csv_path}")
except Exception as e:
    print(f"Failed to write {xlsx_path}: {e}")
    print("If this is an engine error, try installing 'openpyxl' with: python -m pip install openpyxl")
    sys.exit(1)
