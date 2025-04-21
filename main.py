from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import tempfile
from pdf_reader import extract_text_from_pdf
from summarizer import summarize_text
from tts import generate_audio

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/output", exist_ok=True)

# AJOUTEZ CETTE ROUTE RACINE
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API VocaFile!"}

@app.post("/process/")
async def process_file(file: UploadFile = File(...), max_sentences: int = Form(5)):
    """Traite PDF, TXT, DOCX et génère un résumé + audio"""
    process_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1].lower()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        temp_file.write(await file.read())
        temp_file.close()
        # Extraction du texte selon le type de fichier
        if ext == '.pdf':
            text = extract_text_from_pdf(temp_file.name)
        elif ext == '.txt':
            with open(temp_file.name, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext in ['.docx', '.doc']:
            from docx import Document
            doc = Document(temp_file.name)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            os.remove(temp_file.name)
            return {"error": f"Format non supporté : {ext}"}
        # Générer le résumé
        summary = summarize_text(text, max_sentences=max_sentences)
        summary_path = f"static/output/summary_{process_id}.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        # Générer l'audio
        audio_path = f"static/output/audio_{process_id}.mp3"
        generate_audio(summary, output_path=audio_path)
        os.remove(temp_file.name)
        return {
            "summary": summary,
            "summary_file": summary_path,
            "audio_file": audio_path,
            "original_text": text[:1000] + "..." if len(text) > 1000 else text
        }
    except Exception as e:
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
        return {"error": f"Erreur lors du traitement: {str(e)}"}

@app.get("/download/{file_type}/{filename}")
def download_file(file_type: str, filename: str):
    base_dir = os.path.abspath("static/output")
    file_path = os.path.join(base_dir, filename)
    if not os.path.abspath(file_path).startswith(base_dir) or not os.path.isfile(file_path):
        return {"error": "Fichier non trouvé ou accès interdit"}
    if file_type == "audio":
        media_type = "audio/mpeg"
    elif file_type == "summary":
        media_type = "text/plain"
    else:
        return {"error": "Type de fichier non supporté"}
    return FileResponse(file_path, media_type=media_type)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
