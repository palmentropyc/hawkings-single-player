import decimal
import time  
from .models import Grade  
import os
import PyPDF2
import os
import requests
from json import JSONDecodeError
from openai import OpenAI

def process_submission_with_ai(grade_id):
    try:
        grade = get_grade(grade_id)
        update_grade_initial_status(grade)
        update_grade_numeric(grade)
        file_path = get_file_path(grade)
        text_extracted = extract_text(file_path)
        update_grade_final_status(grade, text_extracted)
        print("Grade updated with status:", grade.ai_status)
        if grade.ai_status == 'doc_processed_ok':
            process_with_ai(grade)            
        print("End of processing")
    except Grade.DoesNotExist:
        print(f'Grade with id {grade_id} does not exist')

def process_with_ai(grade):
    print("Procesando con AI")
    grade.ai_status = 'processing'    
    grade.save()
    assignment_questions = grade.assignment.assignment_questions
    assignment_rubric = grade.assignment.assignment_rubric
    full_prompt = f"Eres un profesor experto, vas a corregir un examen. Estas son las preguntas:\n {assignment_questions}\n, esta es la rbrica y criterios de correccion:\n {assignment_rubric}\n y estas son las respuetas del alumno\n {grade.grade_student_response}"
    print(full_prompt)
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Resume este texto"}, {"role": "user", "content": full_prompt}]
    )
    grade.grade_feedback = response.choices[0].message.content
    grade.ai_status = 'ai_processed_ok'  
    grade.save()




def get_grade(grade_id):
    return Grade.objects.get(id=grade_id)

def update_grade_initial_status(grade):
    print(f'Procesando el archivo {grade.local_path}')
    grade.ai_status = 'processing'
    grade.grader_comments = 'Procesando...'

def update_grade_numeric(grade):
    if grade.grade_numeric is None:
        grade.grade_numeric = 0
    else:
        grade.grade_numeric += decimal.Decimal('0.1')

def get_file_path(grade):
    return grade.local_path.path

def extract_text(file_path):
    if os.environ.get('DJANGO_ENVIRONMENT') == 'local':
        print("Extrayendo texto localmente de ", file_path)
        return extract_text_pdf_local(file_path)
    else:
        print("Extrayendo texto con Jina")
        return extract_text_from_pdf_with_jina(file_path)

def update_grade_final_status(grade, text_extracted):
    if text_extracted is not None:
        grade.grade_student_response = text_extracted
        grade.ai_status = 'doc_processed_ok'
    else:
        grade.error_message = "Error al extraer el texto del archivo"
        grade.ai_status = 'error'
    grade.save()





def extract_text_pdf_local(file_path):
    text = ""
    
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
    print("Texto extraido:", text)
    return text.strip()

def extract_text_from_pdf_with_jina(file_path):
    if not file_path.lower().endswith('.pdf'):
        print("El archivo no es un PDF.")
        return None

    try:
        headers = {
            "Authorization": "Bearer jina_b716485cb75b4dcdb4a4864866b69aa3wF7JNTrxI3kc3ufJoJbgIc86ZqA8",
            "X-With-Generated-Alt": "true"
        }
        url_jina = f"https://r.jina.ai/{file_path}"
        print(f"Intentando con el archivo: {url_jina}")
        response = requests.get(url_jina, headers=headers)
        print("Response status code:", response.status_code)
        print("Response headers:", response.headers)
        
        # Print the raw content of the response
        print("Raw response content:")
        print(response.text[:100])  # Print first 100 characters to avoid overwhelming output
        
        # Try to parse as JSON, but handle the case where it's not JSON
        try:
            response_data = response.json()
            print("Parsed JSON response:", response_data)
        except JSONDecodeError:
            print("Response is not in JSON format.")
            # If it's not JSON, we might want to treat the response.text as the content directly
            return response.text
        
        # If we successfully parsed JSON, proceed with extracting content
        if isinstance(response_data, dict) and "data" in response_data and "content" in response_data["data"]:
            return response_data["data"]["content"]
        else:
            print("Expected 'data' and 'content' keys not found in the JSON response.")
            return None

    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        return None
