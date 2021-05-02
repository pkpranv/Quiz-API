from django.urls import path
#
from .views.users import RegistrationView,LoginView
from .views.user_answer_view import UserAnswerCreate,GetQuestionView,GetScoreView

urlpatterns = [
    path('register/', RegistrationView.as_view(),
         name='register'),
    path('login/', LoginView.as_view(),
         name='login'),
    path('answer/', UserAnswerCreate.as_view(),
         name='answer'),
    path('get_next_question/', GetQuestionView.as_view(),
         name='get_next_question'),
    path('get_score/',GetScoreView.as_view(),
         name = 'get_score')
    ]