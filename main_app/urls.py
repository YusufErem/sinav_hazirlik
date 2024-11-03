from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('add_question/', views.addQuestion, name='add_question'),
    path('category/<int:category_id>/', views.categoryQuestions, name='category_questions'),
    path('question/<int:question_id>/', views.questionDetail, name='question_detail'),
    path('question/<int:question_id>/edit/', views.editQuestion, name='edit_question'),
    path('question/<int:question_id>/delete/', views.deleteQuestion, name='delete_question'),
    path('question/<int:question_id>/toggle_complete/', views.toggleCompleteQuestion, name='toggle_complete_question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)