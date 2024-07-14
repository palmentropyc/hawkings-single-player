from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from youtube_transcript_api import YouTubeTranscriptApi
from celery.result import AsyncResult
from django_celery_results.models import TaskResult
from .models import YoutubeVideo
from .forms import YoutubeVideoForm
import json
import os
from os.path import isfile, join
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import YoutubeVideo
from .forms import YoutubeVideoForm
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import os
import requests


def youtubevideo_create(request):
    if request.method == 'POST':
        form = YoutubeVideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video.video_id)
                video.transcript = '\n'.join([entry['text'] for entry in transcript])
            except Exception as e:
                messages.error(request, f"Error fetching transcript: {str(e)}")
            video.save()
            return redirect('studio:youtubevideo-list')
    else:
        form = YoutubeVideoForm()
    return render(request, 'studio/youtubevideo_form.html', {'form': form})

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

class YoutubeVideoListView(LoginRequiredMixin, ListView):
    model = YoutubeVideo
    template_name = 'studio/youtubevideo_list.html'
    context_object_name = 'videos'
    ordering = ['-id']




from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import YoutubeVideo
from .forms import YoutubeVideoForm
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os
import json

from bs4 import BeautifulSoup
import requests
import re

class YoutubeVideoCreateView(LoginRequiredMixin, CreateView):
    model = YoutubeVideo
    form_class = YoutubeVideoForm
    template_name = 'studio/youtubevideo_form.html'
    success_url = reverse_lazy('studio:youtubevideo-list')

    def form_valid(self, form):
        video = form.save(commit=False)
        video.user = self.request.user
        video.video_id = YoutubeVideo.extract_video_id(form.cleaned_data['url'])

        print(f"DEBUG: Video ID extraído: {video.video_id}")

        # Obtener información del video usando scraping
        url = f"https://www.youtube.com/watch?v={video.video_id}"
        response = requests.get(url)

        print(f"DEBUG: Código de estado de la respuesta: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Usar BeautifulSoup para extraer el título del video
            title_tag = soup.find('meta', {'name': 'title'})
            if title_tag:
                video.title = title_tag['content']
                print(f"DEBUG: Título extraído: {video.title}")
            else:
                print("DEBUG: No se encontró la etiqueta del título en la página")
        else:
            print(f"DEBUG: Error al acceder a la página del video. Código de estado: {response.status_code}")

        # Obtener la transcripción
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video.video_id)
            video.transcript = '\n'.join([entry['text'] for entry in transcript])
            print(f"DEBUG: Transcripción obtenida. Longitud: {len(video.transcript)}")
        except Exception as e:
            print(f"DEBUG: Error al obtener la transcripción: {str(e)}")

        video.save()
        return super().form_valid(form)


class YoutubeVideoDetailView(LoginRequiredMixin, DetailView):
    model = YoutubeVideo
    template_name = 'studio/youtubevideo_detail.html'
    context_object_name = 'video'