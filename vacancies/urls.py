from django.urls import path

from vacancies import views as vacancies_views

urlpatterns = [
    path('', vacancies_views.VacancyView.as_view()),
    path('<int:pk>/', vacancies_views.VacancyDetailView.as_view()),
    path('create/', vacancies_views.VacancyCreateView.as_view()),
    path('<int:pk>/update/', vacancies_views.VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', vacancies_views.VacancyDeleteView.as_view()),
]