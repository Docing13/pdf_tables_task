import easyocr
from PIL import Image
import numpy as np
import re


class OcrExtractor:
    FILTER_CHARS = "$.(),:"
    
    def __init__(self,
                 img: Image,
                 langs=('en',)):
        
        self.reader = easyocr.Reader(langs)
        self.img = img
    
    def filter_text(self,
                    text: str):
        
        # remove digits
        text_filtered = re.sub(r"[0-9']+", "", text)
        
        translator = str.maketrans('', '', self.FILTER_CHARS)
        text_filtered = text_filtered.translate(translator)
        
        return text_filtered
    
    def extract_text_from_image(self) -> str:
        img_np = np.array(self.img)
        results = self.reader.readtext(img_np)
        text_res = ' '.join([item[1] for item in results]) if results else ''
        text_res = self.filter_text(text=text_res)
        
        return text_res