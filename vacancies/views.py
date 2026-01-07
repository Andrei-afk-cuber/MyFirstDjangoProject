import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy

# class for vacancies
@method_decorator(csrf_exempt, name='dispatch')
class VacancyView(View):
    # GET processing
    def get(self, request):
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

    def post(self, request):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy()
        vacancy.text = vacancy_data['text']

        vacancy.save()

        return JsonResponse({
            "text": vacancy.text
        })

# class for detail vacancy view
class VacancyDetailView(DetailView):
    model = Vacancy

    # GET processing
    def get(self, *args, **kwargs):
        vacancy = self.get_object()

        return JsonResponse({
            'id': vacancy.id,
            'text': vacancy.text
        })
