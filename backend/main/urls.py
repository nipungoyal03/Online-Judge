from django.urls import path
from main.views import ProblemListAPIView,ProblemDetailAPIView,ExecuteCodeAPIView

urlpatterns = [
    path('api/problems/', ProblemListAPIView.as_view(), name='problem-list'),
    path('api/problem/<str:code>/', ProblemDetailAPIView.as_view(), name='problem-detail'),
    path('api/execute/', ExecuteCodeAPIView.as_view(), name='execute'),

]