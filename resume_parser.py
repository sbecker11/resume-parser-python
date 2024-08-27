import time
import pdfplumber
import sys
import anthropic
import json
import os
from dotenv import load_dotenv
from docx import Document

resume_schema_path = './inputs/resume-schema.json'
 
# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf_with_formatting(resume_pdf_path):
    text = ""
    with pdfplumber.open(resume_pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx_with_formatting(resume_input_docx_path):
    text = ""
    doc = Document(resume_input_docx_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def get_resume_schema_string():
    with open(resume_schema_path,'r') as f:
        return f.read()

def get_resume_schema():
    return json.loads(get_resume_schema_string())

def main():
    if len(sys.argv) != 3:
        print("Usage: python resume_parser.py <path_to_input_resume.pdf|docx> <path_to_output_resume.json>")
        return

    resume_input_path = sys.argv[1]
    resume_input_pdf_path = resume_input_path if resume_input_path.lower().endswith('.pdf') else None
    resume_input_docx_path = resume_input_path if resume_input_path.lower().endswith('.docx') else None
    resume_output_json_path = sys.argv[2]
    resume_schema_string = get_resume_schema_string()
    
    # get resume_input text from either pdf file or docx file
    resume_input_text = None
    start_time = time.time()
    if resume_input_pdf_path:
        if not os.path.exists(resume_input_pdf_path):
            print(f"pdf file not found: {resume_input_pdf_path}")
            return
        resume_input_text = extract_text_from_pdf_with_formatting(resume_input_pdf_path)
    elif resume_input_docx_path:
        if not os.path.exists(resume_input_docx_path):
            print(f"docx file not found: {resume_input_docx_path}")
            return
        resume_input_text = extract_text_from_docx_with_formatting(resume_input_docx_path)
    else:
        print("Invalid input resume file format. Only PDF and DOCX files are supported.")
        return
    
    elapsed_time = time.time() - start_time
    print(f"text extraction completed in {elapsed_time:.2f} seconds")

    # Prompt text for the model
    prompt_text =f"""
        Please convert the following resume text 
        into a JSON object that conforms to the 
        provided resume schema.

        The resume text starts here:
        {resume_input_text}
        The resume text ends here.

        The resume schema starts here:
        {resume_schema_string}
        The resume schema ends here.
        
        Please provide only the JSON object in 
        your response, with no additional text.
        """
    
    # Initialize the Anthropic client, after getting 
    # ANTHROPIC_API_KEY from the .env file at the root of the project
    load_dotenv()    
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY-20240816")
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    model = "claude-3-sonnet-20240229"
    
    start_time = time.time() # seconds
    print(f"prompt sent to {model}")
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        temperature=0,
        system="You are an expert at using resume schemas to convert resume text into structured resume objects.",
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    elapsed_time = time.time() - start_time
    print(f"response received in {elapsed_time:.2f} seconds")

    # use the response to load to define the json object
    json_object = None
    output = response.content[0].text
    if isinstance(output, str):
        json_object = json.loads(output)
    elif isinstance(output, dict):
        json_object = output

    # Print the parsed JSON
    if json_object is not None:
        with open(resume_output_json_path, 'w') as f:
            json.dump(json_object, f, indent=2)

    print(f"{resume_input_path} has been parsed to: {resume_output_json_path} by schema {resume_schema_path}")

if __name__ == "__main__":
    main()
