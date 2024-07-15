from django.urls import path
from .video_functions import YoutubeVideoListView
from .views import YoutubeVideoCreateView, YoutubeVideoDetailView

app_name = 'studio'


urlpatterns = [
    path('videos/', YoutubeVideoListView.as_view(), name='youtubevideo-list'),
    path('videos/new/', YoutubeVideoCreateView.as_view(), name='youtubevideo-create'),
    path('videos/<int:pk>/', YoutubeVideoDetailView.as_view(), name='youtubevideo-detail'),
]