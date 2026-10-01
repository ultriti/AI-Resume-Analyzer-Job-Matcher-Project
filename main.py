from fastapi import FastAPI, HTTPException
from pathlib import Path

import numpy as np
import pandas as pd



# load models and all other artifacts
BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "Artifacts"
STATIC_DIR = BASE_DIR / "static"


# model path
model_pah = ARTIFACTS_DIR / "BiGRU_Model.keras"
# tokenizer path
tokenizer_pah = ARTIFACTS_DIR / "tokenizer.pkl"

# Mx Seq Len
max_seq_len = 50


app = FastAPI()
