import io
import pdfplumber
from PIL import Image
from utils.data_structs import PageTables
    
class OnePagePdfManager:
    IMG_DUMP_RESOLUTION = 200
    
    def __init__(self,
                 pdf_bytes,
                 page_number = 0
                 ):

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            self.pdf = pdf

        self.page_number = page_number
        
    @property
    def pages_count(self) -> int:
        return self.pdf.pages
    
    @property
    def page(self) -> None:
        return self.pdf.pages[self.page_number]
    
    @property
    def is_img(self) -> bool:
        # naive check
        return False if len(self.page.chars) == 0 and len(self.page.images) > 0 else True

    @property
    def tables(self) -> PageTables:
        tables = self.page.find_tables()
        bboxes_imgs = {}
        
        for t in tables:
            # pdfplumber bbox: (x0, top, x1, bottom) where top < bottom (y increases down)
            if hasattr(t, "bbox"):
                table_bbox = t.bbox
                img = self.page.crop(table_bbox).to_image()

                bboxes_imgs[tuple(table_bbox)] = img
        
        result = PageTables(bboxes_imgs=bboxes_imgs)
        
        return result
    
    @property
    def as_img(self) -> Image:
        img = self.page.to_image(resolution=self.IMG_DUMP_RESOLUTION).original  # PIL.Image
        return img
    
    
class PDFValidator:
    def __init__(self, pdf_manager: OnePagePdfManager):
        self.pdf_manager = pdf_manager
    
    def validate_pages(self) -> None:
        if len(self.pdf_manager.pages_count) != 1:
            raise Exception("Wrong page count")
    