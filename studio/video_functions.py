from grade.models import Assignment, Language, EvaluationPrompt
from os.path import isfile, join
import json
import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from .forms import YoutubeVideoForm
from .models import YoutubeVideo
from celery.result import AsyncResult
from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django_celery_results.models import TaskResult
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from openai import OpenAI




def create_assignment_questions_from_video(video_description):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    print("Generando examen")
    system_prompt = EvaluationPrompt.objects.get(label="youtube_generation_prompt").prompt_text
    print("\033[92m" + system_prompt + "\033[0m")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": video_description}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return ''
    

def create_assignment_rubric_from_questions(questions, video_transcript):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    print("Generando rbrica")
    system_prompt = EvaluationPrompt.objects.get(label="youtube_rubric_prompt").prompt_text
    print("\033[94m" + system_prompt + "\033[0m")
    user_message = f"ESTAS SON LAS PREGUNTAS DEL EXAMEN:\n\n {questions}\n\nESTA ES LA TRANSCRIPCIÓN DEL VIDEO: {video_transcript}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        response.choices[0].message.content
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return ''

def create_assignment_from_video(video):
    print(f"DEBUG: Creating assignment from video: {video.title}")
    print(f"DEBUG: Video transcript length: {len(video.transcript)}")
    print(f"DEBUG: Video user: {video.user}")
    assignment_questions = create_assignment_questions_from_video(video.transcript)
    assignment_rubric = create_assignment_rubric_from_questions(assignment_questions, video.transcript)
    assignment_full_text = ''

    assignment = Assignment.objects.create(        
        name=video.title,
        assignment_questions=assignment_questions,
        assignment_rubric=assignment_rubric,
        assignment_full_text=assignment_full_text,        
        user=video.user,
        language = Language.objects.get(id=1)
    )
    assignment.save()


def task_output(request):
    '''
    Returns a task output 
    '''

    task_id = request.GET.get('task_id')
    task    = TaskResult.objects.get(id=task_id)

    if not task:
        return ''

    # task.result -> JSON Format
    return HttpResponse( task.result )

def task_log(request):
    '''
    Returns a task LOG file (if located on disk) 
    '''

    task_id  = request.GET.get('task_id')
    task     = TaskResult.objects.get(id=task_id)
    task_log = 'NOT FOUND'

    if not task: 
        return ''

    try: 

        # Get logs file
        all_logs = [f for f in os.listdir(settings.CELERY_LOGS_DIR) if isfile(join(settings.CELERY_LOGS_DIR, f))]
        
        for log in all_logs:

            # Task HASH name is saved in the log name
            if task.task_id in log:
                
                with open( os.path.join( settings.CELERY_LOGS_DIR, log) ) as f:
                    
                    # task_log -> JSON Format
                    task_log = f.readlines() 

                break    
    
    except Exception as e:

         task_log = json.dumps( { 'Error CELERY_LOGS_DIR: ' : str( e) } )

    return HttpResponse(task_log)

def download_log_file(request, file_path):
    path = file_path.replace('%slash%', '/')
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id):
    try:
        # Listar todas las transcripciones disponibles
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_transcripts = {}
        
        for transcript in transcript_list:
            available_transcripts[transcript.language_code] = transcript
            # Imprimir las propiedades de cada transcripción
            print(
                transcript.video_id,
                transcript.language,
                transcript.language_code,
                transcript.is_generated,
                transcript.is_translatable,
                transcript.translation_languages,
            )
        
        # Intentar obtener la transcripción en inglés
        if 'en' in available_transcripts:
            transcript_data = available_transcripts['en'].fetch()
            return transcript_data
        
        # Si falla, intentar obtener la transcripción en español
        if 'es' in available_transcripts:
            transcript_data = available_transcripts['es'].fetch()
            return transcript_data
        
        # Si falla, obtener la primera transcripción disponible en otro idioma
        for lang_code, transcript in available_transcripts.items():
            transcript_data = transcript.fetch()
            return transcript_data
            
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"Error retrieving transcripts: {e}")
        return None

def youtubevideo_create(request):
    if request.method == 'POST':
        form = YoutubeVideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            transcript = get_transcript(video.video_id)
            
            if transcript:
                video.transcript = '\n'.join([entry['text'] for entry in transcript])
                video.save()
            else:
                messages.error(request, "No transcript available in any language.")
            return redirect('studio:youtubevideo-list')
    else:
        form = YoutubeVideoForm()
    return render(request, 'studio/youtubevideo_form.html', {'form': form})
