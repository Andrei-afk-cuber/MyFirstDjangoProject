import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from users.models import User

# class for users
@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request):
        users = User.objects.all()

        name = request.GET.get('name', None)
        age = request.GET.get('age', None)

        if name:
            users = users.filter(name=name)

        if age:
            users = users.filter(age=age)

        response = []
        for user in users:
            response.append({
                "id": user.id,
                "name": user.name,
                "age": user.age
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        user_data = json.loads(request.body)

        new_user = User()

        try:
            new_user.name = user_data['name']
            new_user.age = user_data['age']
            new_user.save()
        except:
            return JsonResponse({"error": "Invalid data"}, status=400)

        return JsonResponse({
            "name": new_user.name,
            "age": new_user.age
        })

# class for get detail info about user
class UserDetailView(DetailView):
    # set model for working
    model = User

    def get(self, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "name": user.name,
            "age": user.age
        })