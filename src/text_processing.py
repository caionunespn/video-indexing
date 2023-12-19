import cv2
import pytesseract
import re
from keywords_utils import filter_keywords, language_mapping

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
regex = re.compile('[^a-zA-Z]')

def read_text_from_video(video_path, language):
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 1

    keywords = []

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % 180 == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray_frame)
            
            if len(text) > 0:
                words = text.split()
                for word in words:
                    word = regex.sub('', word)
                    if len(word) > 1:
                        keywords.append(word)
    
    keywords = list(set(keywords))
    keywords = filter_keywords(' '.join(keywords), language_mapping[language])

    video_capture.release()

    return keywords