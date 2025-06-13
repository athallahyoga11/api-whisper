from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
import librosa
import numpy as np
import io

app = FastAPI()

pipe = pipeline(
    "automatic-speech-recognition",
    model="Athallah11/whisper-small-javanese",
    device=-1  # Use -1 for CPU or 0 for CUDA
)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    try:
        # Read file content into memory
        audio_bytes = await file.read()
        
        # Use librosa to load audio from bytes
        # This doesn't require ffmpeg for most common formats
        audio_array, sample_rate = librosa.load(
            io.BytesIO(audio_bytes), 
            sr=16000  # Whisper expects 16kHz
        )
        
        # Convert to the format expected by the pipeline
        result = pipe(audio_array)

        return {"transcription": result["text"]}
    except Exception as e:
        return {"error": str(e)}
