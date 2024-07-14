from django import forms
from .models import YoutubeVideo

class YoutubeVideoForm(forms.ModelForm):
    class Meta:
        model = YoutubeVideo
        fields = ['url']

    def clean_url(self):
        url = self.cleaned_data['url']
        video_id = YoutubeVideo.extract_video_id(url)
        if not video_id:
            raise forms.ValidationError('Invalid YouTube URL')
        return url