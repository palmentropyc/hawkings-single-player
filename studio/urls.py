from django.urls import path
from .views import YoutubeVideoCreateView, YoutubeVideoDetailView, YoutubeVideoListView

app_name = 'studio'


urlpatterns = [
    path('videos/', YoutubeVideoListView.as_view(), name='youtubevideo-list'),
    path('videos/new/', YoutubeVideoCreateView.as_view(), name='youtubevideo-create'),
    path('videos/<int:pk>/', YoutubeVideoDetailView.as_view(), name='youtubevideo-detail'),
]