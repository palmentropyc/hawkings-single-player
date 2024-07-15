
import requests

from django.views.generic import ListView
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from youtube_transcript_api import YouTubeTranscriptApi
from .forms import YoutubeVideoForm
from .models import YoutubeVideo
from django.utils.decorators import method_decorator
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .video_functions import create_assignment_from_video
from django.contrib.auth.mixins import LoginRequiredMixin

    
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
            create_assignment_from_video(video)
        except Exception as e:
            print(f"DEBUG: Error al obtener la transcripción: {str(e)}")

        video.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class YoutubeVideoDetailView(DetailView):
    model = YoutubeVideo
    template_name = 'studio/youtubevideo_detail.html'
    context_object_name = 'video'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("You don't have permission to view this video.")
        return obj

@method_decorator(login_required, name='dispatch')
class YoutubeVideoListView(LoginRequiredMixin, ListView):
    model = YoutubeVideo
    template_name = 'studio/youtubevideo_list.html'
    context_object_name = 'videos'
    ordering = ['-id']

    def get_queryset(self):
        return YoutubeVideo.objects.filter(user=self.request.user).order_by('-id')