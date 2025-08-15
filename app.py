from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import io
import uvicorn
import base64
from utils.views import index_response
from utils.pdf_utils import OnePagePdfManager, PDFValidator
from utils.pipelines import TableDetectionPipeline


app = FastAPI(title="PDF Table Detector")


@app.get("/")
def index():
    response = index_response()
    return response


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are supported")

    content = await file.read()
    
    try:
        manager = OnePagePdfManager(pdf_bytes=content)
        validator = PDFValidator(pdf_manager=manager)
        validator.validate_pages()
    
    except Exception as e: 
        raise HTTPException(400, f"Wrong pages count or PDF is broken: {e}")

    pipeline = TableDetectionPipeline(pdf_manger=manager)
    
    try:
        # json dump and img
        result_dict, img = pipeline.run() 
    
    except Exception as e:
        raise HTTPException(400, f"Something went wrong: {e}")

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode("utf-8")

    return JSONResponse(content={
        "tables": result_dict,
        "image_base64": img_base64
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)