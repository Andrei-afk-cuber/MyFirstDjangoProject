import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from vacancies.models import Vacancy

# view for vacancies
# use decorator for off csrf
@csrf_exempt
def vacancies(request):
    if request.method == "GET":
        vacancies = Vacancy.objects.all()

        # get 'text' query parameter
        search_text = request.GET.get('text', None)

        if search_text:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text
            })

        return JsonResponse(response, safe=False)

    elif request.method == "POST":
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy()
        vacancy.text = vacancy_data['text']

        vacancy.save()

        return JsonResponse({
            "text": vacancy.text
        })

# view for get vacancy by id
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

