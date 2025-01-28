from django.urls import path
from .views import TOCView, GenerateCourseView, YoutubeQueryView

urlpatterns = [
    path('toc/', TOCView.as_view(), name='toc'),  # POST request for generating TOC
    path('generate-course/', GenerateCourseView.as_view(), name='generate-course'),  # POST request for generating course
    path('search-youtube/', YoutubeQueryView.as_view(), name='search-youtube'),  # POST request for generating course
]
