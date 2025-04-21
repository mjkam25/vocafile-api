from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os
import tempfile

def extract_audio_from_video(video_path):
    """Extrait l'audio d'une vidéo"""
    try:
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio.close()
        
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(temp_audio.name, codec='pcm_s16le')
        
        return temp_audio.name
    except Exception as e:
        print(f"[ERREUR EXTRACTION AUDIO] {e}")
        return None

def transcribe_audio(audio_path):
    """Transcrit l'audio en texte"""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="fr-FR")
            return text
    except Exception as e:
        print(f"[ERREUR TRANSCRIPTION] {e}")
        return ""
    finally:
        # Supprime le fichier temporaire
        if os.path.exists(audio_path):
            os.remove(audio_path)

def process_video(video_path):
    """Extrait le texte d'une vidéo"""
    try:
        audio_path = extract_audio_from_video(video_path)
        if not audio_path:
            return ""
        
        text = transcribe_audio(audio_path)
        return text
    except Exception as e:
        print(f"[ERREUR VIDÉO] {e}")
        return ""
