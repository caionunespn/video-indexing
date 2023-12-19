from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

language_mapping = {
    'pt-BR': 'portuguese',
    'en-US': 'english',
    'es-ES': 'spanish',
    'ar': 'arabic',
}

def filter_keywords(text, language='portuguese'):
    stop_words = set(stopwords.words(language))
    words = word_tokenize(text)
    filtered = [word.lower() for word in words if word.lower() not in stop_words]
    return filtered