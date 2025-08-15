from utils.data_structs import PageTables
from PIL import Image
import torch
from ultralyticsplus import YOLO


def yolo_to_pagetables(results,
                       page_image: Image.Image) -> PageTables:

    page_tables = PageTables()
    
    # Tensor [N, 4]
    boxes_xyxy = results[0].boxes.xyxy.cpu()  
    
    for box in boxes_xyxy:
        x0, y0, x1, y1 = map(int, box.tolist())
        
        bbox = (x0, y0, x1, y1)

        crop_img = page_image.crop((x0, y0, x1, y1))
        page_tables.bboxes_imgs[bbox] = crop_img

    return page_tables


class YoloTablesDetector:
    """
    https://huggingface.co/keremberke/yolov8m-table-extraction
    """
    MDL_PATH = 'keremberke/yolov8m-table-extraction'
    
    def __init__(self):
        
        self.model = self.load_model()
        self.model_setup()
            
    def model_setup(self):
        self.model.overrides['conf'] = 0.2  # NMS confidence threshold
        self.model.overrides['iou'] = 0.3  # NMS IoU threshold
        self.model.overrides['agnostic_nms'] = False  # NMS class-agnostic
        self.model.overrides['max_det'] = 20  # maximum number of detections per image

    def load_model(self) -> torch.nn.Module:

        model = YOLO(self.MDL_PATH)
        return model
    
    def predict(self, img: Image)-> PageTables:
        
        with torch.no_grad():
            results = self.model.predict(img)
        
        yolo_pagetables = yolo_to_pagetables(results=results,
                                             page_image=img)
        return yolo_pagetables
            