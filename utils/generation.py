from transformers import pipeline
from utils.ocr import OcrExtractor
from PIL import Image


class ImageLabelGenerator:
    TASK = "text2text-generation"
    MODEL_TYPE = "google/flan-t5-small"
    
    MAX_NEW_TOKENS = 6
    NUM_BEAMS = 6
    DO_SAMPLE = False
    CLEAN_UP = True
    
    def __init__(self,
                 max_length=10):
        
        self.max_lenght = max_length
        self.label_gen_model = pipeline(self.TASK,
                                   model=self.MODEL_TYPE)
        
        
    def generate_summary(self,
                         img: Image) -> str:
        
        ocr_extractor = OcrExtractor(img=img)
        text = ocr_extractor.extract_text_from_image()
        
        prompt = f"Generate ONE short label word for the following text:\n{text}"
        result = self.label_gen_model(prompt.lower(),
                                      max_new_tokens=self.MAX_NEW_TOKENS,         
                                      num_beams=self.NUM_BEAMS,              
                                      do_sample=self.DO_SAMPLE,          
                                      clean_up_tokenization_spaces=self.CLEAN_UP)
        
        label = result[0]['generated_text'] + ' table'
        return label
