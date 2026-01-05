from django.http import JsonResponse
from django.shortcuts import render

from vacancies.models import Vacancy, User

# view for vacancies
def vacancies(request):
    if request.method == "GET":
        vacancies = Vacancy.object.all()

        response = []

        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text
            })

        return JsonResponse(response, safe=False)

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