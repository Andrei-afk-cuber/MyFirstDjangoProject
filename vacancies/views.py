import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.db.models.fields.json import JSONExact
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from DjangoProject import settings
from vacancies.models import Vacancy, Skill


def hello(request):
    return HttpResponse("Hello, world!!!")

# class for vacancies
@method_decorator(csrf_exempt, name='dispatch')
class VacancyView(ListView):
    model = Vacancy

    # GET processing
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # get 'text' query parameter
        search_text = request.GET.get('text', None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        self.object_list = self.object_list.order_by("text")

        # pagination
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGES)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        vacancies = []
        for vacancy in page_obj:
            vacancies.append({
                "id": vacancy.id,
                "text": vacancy.text,
                "slug": vacancy.slug,
                "status": vacancy.status,
                "skills": list(map(str, vacancy.skills.all())),
                "user_id": vacancy.user.id
            })

        response = {
            "items": vacancies,
            "num_pages": paginator.num_pages,
            "ent_page": page_number,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)

# class for detail vacancy view
@method_decorator(csrf_exempt, name='dispatch')
class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        return JsonResponse({
            'id': vacancy.id,
            'text': vacancy.text,
            'slug': vacancy.slug,
            'status': vacancy.status,
            'created': vacancy.created,
            'user': vacancy.user_id,
            "skills": list(map(str, vacancy.skills.all())),
            "user_id": vacancy.user.id
        })

@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)

        # return obj or 404
        user = get_object_or_404(User, pk=vacancy_data["user_id"])

        vacancy = Vacancy.objects.create(
            user=user,
            slug=vacancy_data['slug'],
            text=vacancy_data['text'],
            status=vacancy_data['status']
        )

        for skill in vacancy_data['skills']:
            skill_obj, created = Skill.objects.get_or_create(name=skill, defaults={
                "is_active": True
            })
            vacancy.skills.add(skill_obj)

        vacancy.save()

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug,
            "status": vacancy.status,
            "created": vacancy.created,
            "user": vacancy.user_id
        })

@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["slug", "text", "status", "skills"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)
        self.object.slug=vacancy_data['slug']
        self.object.text=vacancy_data['text']
        self.object.status=vacancy_data['status']

        for skill in vacancy_data['skills']:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({"status": "Skill not found"}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "text": self.object.text,
            "slug": self.object.slug,
            "status": self.object.status,
            "user": self.object.user_id,
            "skills": list(self.object.skills.all().values_list("name", flat=True))
        })

@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            "status": "ok"
        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGES)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies
            })

        return JsonResponse({
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]
        })