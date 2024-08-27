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
```python resume_parser.py resume-inputs/proj-mngr.pdf resume-outputs/proj-mngr-pdf.json```

### use anthropic claude to extract json structure from a docx file
```python resume_parser.py resume-inputs/proj-mngr.docx resume-outputs/proj-mngr-docx.json```

### verify that the extracted json files are -nearly- identical  
```diff resume-outputs/proj-mngr-pdf.json resume-outputs/proj-mngr-docx.json```

### compute the json-schema of the json file from the pdf file
```python compute_json_schema.py resume-outputs/proj-mngr-pdf.json resume-outputs/proj-mngr-pdf-schema.json```

### compute the json-schema of the json file from the docx file
```python compute_json_schema.py resume-outputs/proj-mngr-docx.json resume-outputs/proj-mngr-docx-schema.json```

### verify that the json-schema files are -nearly- identical
```diff resume-outputs/proj-mngr-pdf-schema.json resume-outputs/proj-mngr-docx-schema.json```

