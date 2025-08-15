# pdf_tables_task

### Build (in project root):
```
docker build -t pdf-table-detector .
```

### Run:
```
docker run --gpus device=0 -p 8000:8000 pdf-table-detector
```

### Testing:
Open in browser and upload pdf document
```
in browser http://localhost:8000/
```
### Limitations:
Only one page pdfs
