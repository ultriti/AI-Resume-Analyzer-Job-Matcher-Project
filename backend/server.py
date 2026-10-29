from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

import re
import pickle
from keras.models import load_model

from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


# ------
from backend.dependencies.Funtions import extract_information


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

class ResumeAnalysisResponse(BaseModel):
    job_title: Optional[str]
    skills: list[str]
    prediction_category: str
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
    return predict_category(text_input.text)


def predict_category(input_text: str) -> PredictionResponse:
    BiGRU_model = dl_model.get("BiGRU")
    tokenizer = dl_model.get("Tokenizer")

    if BiGRU_model is None or tokenizer is None:
        raise HTTPException(
            status_code=503, detail="Model not loaded yet. Please load the model."
        )

    text = preprocessed_text(input_text)
    tokenized_text = tokenizer.texts_to_sequences([text])
    padded_text = pad_sequences(
        tokenized_text, maxlen=max_seq_len, padding="post", truncating="post"
    )
    probabilities = BiGRU_model.predict(padded_text)[0]
    predicted_index = int(np.argmax(probabilities))

    return PredictionResponse(
        text=input_text,
        prediction_emotion=labels[predicted_index],
        confidence=float(probabilities[predicted_index]),
        all_probabilities={
            label: float(probability)
            for label, probability in zip(labels, probabilities)
        },
    )


@app.post("/analyze-resume", response_model=ResumeAnalysisResponse)
def analyze_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Upload a PDF resume.")

    profile = extract_information(file.file)
    if not profile["skills"]:
        raise HTTPException(
            status_code=422,
            detail="No supported skills were found in the uploaded resume.",
        )

    prediction_result = predict_category(profile["model_input"])
    return ResumeAnalysisResponse(
        job_title=profile["job_title"],
        skills=profile["skills"],
        prediction_category=prediction_result.prediction_emotion,
        confidence=prediction_result.confidence,
        all_probabilities=prediction_result.all_probabilities,
    )
