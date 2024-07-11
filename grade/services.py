# grade/services.py
import decimal
import time  # Solo para simulación, remueve esto y añade tu lógica real
from .models import Grade  # Asegúrate de importar el modelo Grade

def process_submission_with_ai(grade_id):
    # Recuperar el objeto Grade
    try:
        grade = Grade.objects.get(id=grade_id)
        # Simulación de procesamiento del archivo
        time.sleep(2)  # Remueve esta línea y añade tu lógica real
        print(f'Procesando el archivo {grade.local_path}')
        grade.ai_status = 'processing'
        grade.grader_comments = 'Procesando...'
        if grade.grade_numeric is None:
            grade.grade_numeric = 0
        else:
            grade.grade_numeric = grade.grade_numeric + decimal.Decimal('0.1')
        grade.save()
        print("Grade updated with status:", grade.ai_status)
        print("End of processing")
        # Aquí añadirías el código para procesar el archivo
    except Grade.DoesNotExist:
        print(f'Grade with id {grade_id} does not exist')
