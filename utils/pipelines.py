from utils.pdf_utils import OnePagePdfManager
from utils.img_detection import YoloTablesDetector
from utils.data_structs import PageTables, JsonReportGenerator
from utils.generation import ImageLabelGenerator
from utils.draw import draw_pdfplumber_bboxes
import torch
import logging


# fix latests load issue
orig_torch_load = torch.load

def torch_wrapper(*args, **kwargs):
    logging.warning("[unsafe-torch] Patched `torch.load`.  The `weights_only` option of `torch.load` is forcibly disabled.")
    kwargs['weights_only'] = False

    return orig_torch_load(*args, **kwargs)


class TableDetectionPipeline:
    
    def __init__(self,
                 pdf_manger:OnePagePdfManager):

        self.pdf_manager = pdf_manger
        self.patch_load()
    
    @staticmethod
    def patch_load() -> None:
        # load error handle
        torch.load = torch_wrapper
        
    def get_bbox_imgs(self) -> PageTables:
        if self.pdf_manager.is_img:
            #process as img using ml
            img = self.pdf_manager.as_img
            detector = YoloTablesDetector()
            result = detector.predict(img=img)
            
        else:
            result = self.pdf_manager.tables

        return result
    
    def label_tables(self,
                     page_tables: PageTables) -> list[str]: 
        labels = []
        summarizator = ImageLabelGenerator()
        
        for img in page_tables.bboxes_imgs.values():
            label = summarizator.generate_summary(img=img)
            labels.append(label)
        return labels
        
    def run(self):
        # tables extraction
        bbox_imgs_data = self.get_bbox_imgs()        
        # tables Labeling
        labels = self.label_tables(bbox_imgs_data)
        bbox_imgs_data.labels = labels
        # json generation
        json_dump = JsonReportGenerator(bbox_imgs_data).to_json
        # render detected tables on image
        bboxes_img = draw_pdfplumber_bboxes(img=self.pdf_manager.as_img,
                                            bboxes=bbox_imgs_data.bboxes_imgs.keys())
        return json_dump, bboxes_img
        
        
        

            
        
        