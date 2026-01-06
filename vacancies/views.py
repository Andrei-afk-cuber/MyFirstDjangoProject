from django.http import JsonResponse
from django.shortcuts import render

from vacancies.models import Vacancy

# view for vacancies
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

