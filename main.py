from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from pydantic import BaseModel, Field

import re
import pickle
from keras.models import load_model

from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# ------------------------------------------
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

labels = [
    "Business",
    "Cloud & Infrastructure",
    "Data & AI",
    "Design",
    "Marketing",
    "Product & Management",
    "Software Engineering",
]


# --------------------------------------
#  input schema -----------------------
class TextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="the sentence to analyze",
        json_schema_extra={"example": "i am so much happy for this"},
    )


class PredictionResponse(BaseModel):
    text: str
    prediction_emotion: str
    confidence: float
    all_probabilities: dict[str, float]


class HealthRepsonse(BaseModel):
    status: str
    model_loaded: bool


# -------------------------------------
# main file server --------------------


# ------------------------
# load the model ---------

dl_model = {}  # { 1. BiGRU model 2. Tokenizer } -> true if both loaded , {} -> false


@asynccontextmanager
async def LifeSpan(app: FastAPI):
    print("Loading the model ....")
    dl_model["BiGRU"] = load_model(model_pah)

    with open(tokenizer_pah, "rb") as file:
        dl_model["Tokenizer"] = pickle.load(file)

    print("models are loaded successfully UL..")

    # to puase or stop the code or flow we use yeild

    yield  # model is paused but server is running and this point mdoel wait for request

    dl_model.clear()


app = FastAPI(lifespan=LifeSpan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


def preprocessed_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"'", "", text)  # replace ' with empty str
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # remove punct
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces

    return text


# --------------------------------
# main forntend file
@app.get("/")
def server_ui():
    return FileResponse(STATIC_DIR / "index.html")


# -----------------------------------
# health check up


@app.get("/health", response_model=HealthRepsonse)
def health_check():
    return HealthRepsonse(status="server is running UL !", model_loaded=bool(dl_model))


# ----------------------------------
# model predict


@app.post("/predict", response_model=PredictionResponse)
def prediction(text_input: TextInput):

    BiGRU_model = dl_model.get("BiGRU")
    tokenizer = dl_model.get("Tokenizer")

    if BiGRU_model is None or tokenizer is None:
        raise HTTPException(
            status_code=503, detail="Model not loaded yet. Please load the model."
        )

    # ------ filtering the input
    print("---------------------------------------------------------\n",text_input.text)
    text = preprocessed_text(text_input.text)

    print(text)

    # -------- tokanize the text
    tokanized_text = tokenizer.texts_to_sequences([text])

    # -------- padding text
    padded_text = pad_sequences(
        tokanized_text, maxlen=max_seq_len, padding="post", truncating="post"
    )

    print("-=-=-=-=-=-=-=\n",padded_text)
    probabilities = BiGRU_model.predict(padded_text)[0]

    predicted_index = int(np.argmax(probabilities))

    all_probabilities = {
        label: float(prob) for label, prob in zip(labels, probabilities)
    }
    
    predicted_label = labels[predicted_index]

    return PredictionResponse(
        text=text_input.text,
        prediction_emotion=predicted_label,
        confidence=float(probabilities[predicted_index]),
        all_probabilities=all_probabilities,
    )
