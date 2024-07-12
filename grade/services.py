import decimal
import time  
from .models import Grade  
import os
import PyPDF2
import os
import requests
from json import JSONDecodeError
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

def process_submission_with_ai(grade_id):
    logger.debug(f"Processing submission with AI for grade_id: {grade_id}")
    try:
        grade = get_grade(grade_id)
        update_grade_initial_status(grade)
        update_grade_numeric(grade)
        file_path = get_file_path(grade)
        text_extracted = extract_text(file_path)
        update_grade_final_status(grade, text_extracted)
        logger.debug(f"Grade updated with status: {grade.ai_status}")
        if grade.ai_status == 'doc_processed_ok':
            process_with_ai(grade)            
        logger.debug("End of processing")
    except Grade.DoesNotExist:
        logger.error(f'Grade with id {grade_id} does not exist')

def process_with_ai(grade):
    logger.debug(f"Processing with AI for grade: {grade.id}")
    grade.ai_status = 'processing'    
    grade.save()
    assignment_questions = grade.assignment.assignment_questions
    assignment_rubric = grade.assignment.assignment_rubric
    full_prompt = f"Eres un profesor experto, vas a corregir un examen. Estas son las preguntas:\n {assignment_questions}\n, esta es la rbrica y criterios de correccion:\n {assignment_rubric}\n y estas son las respuetas del alumno\n {grade.grade_student_response}"
    logger.debug(f"Full prompt: {full_prompt}")
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Resume este texto"}, {"role": "user", "content": full_prompt}]
    )
    grade.grade_feedback = response.choices[0].message.content
    grade.ai_status = 'ai_processed_ok'  
    grade.save()
    logger.debug(f"AI processing completed for grade: {grade.id}")

def get_grade(grade_id):
    logger.debug(f"Getting grade with id: {grade_id}")
    return Grade.objects.get(id=grade_id)

def update_grade_initial_status(grade):
    logger.debug(f'Processing file {grade.local_path}')
    grade.ai_status = 'processing'
    grade.grader_comments = 'Procesando...'

def update_grade_numeric(grade):
    logger.debug(f"Updating numeric grade for grade: {grade.id}")
    if grade.grade_numeric is None:
        grade.grade_numeric = 0
    else:
        grade.grade_numeric += decimal.Decimal('0.1')

def get_file_path(grade):
    logger.debug(f"Getting file path for grade: {grade.id}")
    return grade.local_path.path

def extract_text(file_path):
    logger.debug(f"Extracting text from file: {file_path}")
    if os.environ.get('DJANGO_ENVIRONMENT') == 'local':
        logger.debug(f"Extracting text locally from {file_path}")
        return extract_text_pdf_local(file_path)
    else:
        logger.debug("Extracting text with Jina")
        return extract_text_from_pdf_with_jina(file_path)

def update_grade_final_status(grade, text_extracted):
    logger.debug(f"Updating final status for grade: {grade.id}")
    if text_extracted is not None:
        grade.grade_student_response = text_extracted
        grade.ai_status = 'doc_processed_ok'
    else:
        grade.error_message = "Error al extraer el texto del archivo"
        grade.ai_status = 'error'
    grade.save()

def extract_text_pdf_local(file_path):
    logger.debug(f"Extracting text locally from PDF: {file_path}")
    text = ""
    
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
    logger.debug(f"Extracted text: {text[:100]}...")  # Log first 100 characters
    return text.strip()

def extract_text_from_pdf_with_jina(file_path):
    logger.debug(f"Extracting text from PDF with Jina: {file_path}")
    if not file_path.lower().endswith('.pdf'):
        logger.warning("The file is not a PDF.")
        return None

    try:
        headers = {
            "Authorization": "Bearer jina_b716485cb75b4dcdb4a4864866b69aa3wF7JNTrxI3kc3ufJoJbgIc86ZqA8",
            "X-With-Generated-Alt": "true"
        }
        url_jina = f"https://r.jina.ai/{file_path}"
        logger.debug(f"Attempting with file: {url_jina}")
        response = requests.get(url_jina, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        
        logger.debug(f"Raw response content (first 100 chars): {response.text[:100]}")
        
        try:
            response_data = response.json()
            logger.debug(f"Parsed JSON response: {response_data}")
        except JSONDecodeError:
            logger.warning("Response is not in JSON format.")
            return response.text
        
        if isinstance(response_data, dict) and "data" in response_data and "content" in response_data["data"]:
            return response_data["data"]["content"]
        else:
            logger.error("Expected 'data' and 'content' keys not found in the JSON response.")
            return None

    except Exception as e:
        import traceback
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        return None
