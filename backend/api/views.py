from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def get_message(request, section):
    messages = {
        "accueil": "Bienvenue sur la page d'accueil ! 🎉",
        "machinelearning": "Découvrez les modèles d'IA 🤖",
        "graphe": "Visualisation des données et graphes",
    }
    
    # Retourne le message en JSON
    return JsonResponse({"message": messages.get(section, "Section non trouvée ! ❌")})
