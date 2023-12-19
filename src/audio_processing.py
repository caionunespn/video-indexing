import os
import moviepy.editor as mp
import speech_recognition as sr
from keywords_utils import filter_keywords, language_mapping

dir = os.path.dirname(os.path.dirname(__file__))

recognizer = sr.Recognizer()

chunks_folder = 'audio-chunks'

def transcribe_large_audio(path, language):
    keywords = []
    chunks_with_error = []

    audio = mp.AudioFileClip(path)
    total_duration = audio.duration
    segment_duration = 60

    for i in range(0, int(total_duration), segment_duration):
        start_time = i
        end_time = min(i + segment_duration, total_duration)
        
        segment = audio.subclip(start_time, end_time)
        segment_path = os.path.join(dir, chunks_folder, f"chunk{i // segment_duration}.wav")
        segment.write_audiofile(segment_path, verbose=False)

        with sr.AudioFile(segment_path) as source:
            audio_listened = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_listened, language=language)
                keywords += filter_keywords(text, language_mapping[language])
            except sr.UnknownValueError as e:
                chunks_with_error.append(str(i // segment_duration))
    
    if len(chunks_with_error) > 0:
        errors = ", ".join(chunks_with_error)
        print("There were errors in some parts of the audio, on chunks {}".format(errors))

    return list(set(keywords))