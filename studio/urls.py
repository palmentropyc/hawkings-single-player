from django.urls import path
from .views import YoutubeVideoListView, YoutubeVideoCreateView, YoutubeVideoDetailView

app_name = 'studio'


urlpatterns = [
    path('videos/', YoutubeVideoListView.as_view(), name='youtubevideo-list'),
    path('videos/new/', YoutubeVideoCreateView.as_view(), name='youtubevideo-create'),
    path('videos/<int:pk>/', YoutubeVideoDetailView.as_view(), name='youtubevideo-detail'),
]