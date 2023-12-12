import cv2
from PIL import Image
from pytesseract import pytesseract
from gtts import gTTS

from datetime import datetime
import pygame

def capture_image():
    filename = f"captured_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    camera = cv2.VideoCapture(0)
    while True:
        _, image = camera.read()
        cv2.imshow('image', image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite(filename, image)
            break
        elif key == 27:  # Press 'Esc' to exit without capturing
            break
    camera.release()
    cv2.destroyAllWindows()
    return filename

def tesseract_ocr(image_path):
    path_to_tesseract = r"C:\Users\user\AppData\Local\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        print("Extracted Text:", text[:-1])
        return text
    except Exception as e:
        print("Error during OCR:", str(e))
        return None

def text_to_speech(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    return output_file

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    print("Press 's' to capture an image. Press 'Esc' to exit without capturing.")
    image_path = capture_image()
    
    if image_path:
        extracted_text = tesseract_ocr(image_path)
        
        if extracted_text:
            audio_file = text_to_speech(extracted_text)
            play_audio(audio_file)