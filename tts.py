from gtts import gTTS
import os

def generate_audio(text, output_path="static/output/audio_resume.mp3", lang="fr"):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        print(f"[✅ AUDIO] Audio généré ici : {output_path}")
        return output_path
    except Exception as e:
        print(f"[ERREUR AUDIO] {e}")
        return None
