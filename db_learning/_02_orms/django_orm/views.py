# 02_orms/django_orm/views.py

from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json

def get_users(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)

@csrf_exempt
def create_user(request):
    data = json.loads(request.body)
    User.objects.create(name=data['name'], age=data['age'])
    return JsonResponse({'message': 'User created'})

@csrf_exempt
def update_user(request, user_id):
    data = json.loads(request.body)
    User.objects.filter(id=user_id).update(name=data['name'], age=data['age'])
    return JsonResponse({'message': 'User updated'})

@csrf_exempt
def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return JsonResponse({'message': 'User deleted'})