# resume-parser-python
attempts to read PDF and DOCX files and parse it into common resume sections in a JSON file

## Setup
```
python3 -m venv venv; 
source venv/bin/activate; 
python3 -m pip install --upgrade pip; 
python3 -m pip install -r requirements.txt;
```

### use anthropic claude to extract json structure from a pdf file
```python resume_parser.py inputs/proj-mngr.pdf outputs/proj-mngr-pdf.json```

### use anthropic claude to extract json structure from a docx file
```python resume_parser.py inputs/proj-mngr.docx outputs/proj-mngr-docx.json```

### verify that the extracted json files are -nearly- identical  
```diff outputs/proj-mngr-pdf.json outputs/proj-mngr-docx.json```

### compute the json-schema of the json file from the pdf json file
```python compute_json_schema.py outputs/proj-mngr-pdf.json outputs/proj-mngr-pdf-schema.json```

### compute the json-schema of the json file from the docx json file
```python compute_json_schema.py outputs/proj-mngr-docx.json outputs/proj-mngr-docx-schema.json```

### verify that the json-schema files are -nearly- identical
```diff outputs/proj-mngr-pdf-schema.json outputs/proj-mngr-docx-schema.json```

## validate the proj-mngr-pdf.json data object against the resume schema
```python validate_data_object.py outputs/resume-pdf.json inputs/resume-schema.json```

## validate the proj-mngr-docx.json data object against the resume schema
```python validate_data_object.py outputs/resume-docx.json inputs/resume-schema.json ```