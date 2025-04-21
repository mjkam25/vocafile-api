import speech_recognition as sr

def transcribe_audio_file(audio_path):
    """Transcrit un fichier audio en texte"""
    try:
        recognizer = sr.Recognizer()
        
        # Déterminer le type de fichier audio
        if audio_path.endswith(('.wav')):
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="fr-FR")
                return text
        else:
            # Pour les autres formats, utiliser un autre mécanisme
            return "Format audio non supporté directement. Convertissez en WAV."
    except Exception as e:
        print(f"[ERREUR AUDIO] {e}")
        return ""
