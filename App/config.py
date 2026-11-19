from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "Data"
PREPROCESSED_DIR = DATA_DIR / "preprocessed"
ASSETS_DIR = ROOT_DIR / "App" / "Assets"
MODEL_PATH = ROOT_DIR / "Models" / "model1.joblib"