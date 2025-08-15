from dataclasses import dataclass, field
from PIL.Image import Image
import json


@dataclass
class PageTables:
    # x0, top, x1, bottom
    bboxes_imgs: dict[tuple[int, int, int, int], Image] = field(default_factory=dict)
    # strs
    labels: list[str] = field(default_factory=list)
    
    @property
    def labels_bboxes(self) -> dict[str, tuple[int, int, int, int]]:
        return {label: bbox for label, bbox in zip(self.labels, self.bboxes_imgs.keys())}
            

class JsonReportGenerator:
    INDENT = 4
    
    def __init__(self,
                 page_tables_data: PageTables):
        
        self.page_tables_data = page_tables_data    
        
    @property
    def to_json(self):
        # returns json with x
        json_string = json.dumps(self.page_tables_data.labels_bboxes,
                                 indent=self.INDENT)
        return json_string