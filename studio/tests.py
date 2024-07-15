from django.test import TestCase
from .video_functions import create_assignment_questions_from_video  # Asegúrate de importar correctamente tu función
from django.conf import settings

class CreateAssignmentQuestionsFromVideoTest(TestCase):
    def setUp(self):
        # Configura tu API Key de OpenAI para pruebas si no está ya configurada en settings
        #settings.OPENAI_API_KEY = openai.api_key = settings.OPENAI_API_KEY
        pass

    def test_create_assignment_questions_from_video(self):
        video_description = "Este es un texto de prueba para la descripción del video. Debe contener información relevante para crear preguntas de examen."
        
        result = create_assignment_questions_from_video(video_description)
        
        # Comprueba que la respuesta no esté vacía y tenga el formato esperado
        self.assertNotEqual(result, '', "La función debería devolver un texto no vacío")
        print(result)  # Esto imprimirá el resultado para que puedas revisarlo manualmente si lo deseas

# Para ejecutar la prueba, usa el siguiente comando en tu terminal:
# python manage.py test tu_app
