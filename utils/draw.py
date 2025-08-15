from PIL import Image, ImageDraw

def draw_pdfplumber_bboxes(img: Image.Image,
                           bboxes: list,
                           color="red",
                           width=4):

    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)

    for bbox in bboxes:
        if len(bbox) != 4:
            raise ValueError(f"Wrong bbox: {bbox}")
        
        x0, top, x1, bottom = bbox
        draw.rectangle([x0, top, x1, bottom], outline=color, width=width)

    return img_copy