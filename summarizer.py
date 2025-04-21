from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np

# Téléchargement unique du tokenizer
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from nltk.tokenize import sent_tokenize

def summarize_text(text, max_sentences=5):
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= max_sentences:
            return text
        vect = TfidfVectorizer().fit_transform(sentences)
        sim_matrix = cosine_similarity(vect)
        scores = sim_matrix.sum(axis=1)
        ranked_indices = np.argsort(scores)[-max_sentences:][::-1]
        ranked_sentences = [sentences[i] for i in sorted(ranked_indices)]
        summary = " ".join(ranked_sentences)
        return summary
    except Exception as e:
        print(f"[ERREUR Résumé] {e}")
        return ""
