from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
import torchaudio
import tempfile
import numpy as np

app = FastAPI()

pipe = pipeline(
    "automatic-speech-recognition",
    model="Athallah11/whisper-small-javanese",
    device=-1 
)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        waveform, sample_rate = torchaudio.load(temp_audio_path)
        waveform = torchaudio.functional.resample(waveform, orig_freq=sample_rate, new_freq=16000)
        waveform = waveform.mean(dim=0).numpy()  

        result = pipe(waveform)  

        return {"transcription": result["text"]}
    except Exception as e:
        return {"error": str(e)}
