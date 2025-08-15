from fastapi.responses import HTMLResponse

def index_response() -> HTMLResponse:
    html_content = """
    <html>
    <body>
        <h3>Upload PDF for tables detection [1 PAGE ONLY]</h3>
        <form action="/detect" enctype="multipart/form-data" method="post">
        <input name="file" type="file" accept="application/pdf">
        <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)