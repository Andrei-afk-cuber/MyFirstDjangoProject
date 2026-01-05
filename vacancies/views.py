from django.http import JsonResponse
from django.shortcuts import render

from vacancies.models import Vacancy, User

# view for vacancies
def vacancies(request):
    if request.method == "GET":
        vacancies = Vacancy.objects.all()

        response = []

        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text
            })

        return JsonResponse(response, safe=False)

# Craete view for get vacancy by id
def get_vacancy(request, vacancy_id):
    if request.method == "GET":
        # get one vacancy by id (ot pk (universal))
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({"error": "Vacancy not found"}, status=404)

        return JsonResponse({
            'id': vacancy.id,
            'text': vacancy.text
        })

# view for get
def users(request):
    if request.method == "GET":
        users = User.objects.all()

        response = []

        for user in users:
            response.append({
                "id": user.id,
                "name": user.name,
                "age": user.age
            })

        return JsonResponse(response, safe=False)

# view for get user by id
def get_user(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=user_id)
        except:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({
            "id": user.id,
            "name": user.name,
            "age": user.age,
        })