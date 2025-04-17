from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import numpy as np
import os
import pandas as pd

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

# On prend le chemin du dossier actuel (api/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'ml_model.pkl')

# Chargement du modèle
model = joblib.load(model_path)

# Créer une vue de prédiction
@api_view(['POST'])
def predict(request):
    try:
        # Récupérer les données envoyées
        sexe_pieton = request.data.get("sexe_pieton")
        departement = request.data.get("departement")
        meteo = request.data.get("meteo")
        jour_semaine = request.data.get("jour_semaine")
        lumiere = request.data.get("lumiere")

        # Préparer les données d'entrée pour la prédiction
        data = pd.DataFrame([{
            "sexe_pieton": sexe_pieton,
            "Département": departement,
            "Conditions atmosphériques": meteo,
            "Jour_semaine": jour_semaine,
            "Lumière": lumiere,
        }])

        # Prédire la gravité
        prediction = model.predict(data)
        prediction_proba = model.predict_proba(data)

        # Retourner les résultats de la prédiction et les probabilités
        return JsonResponse({
            "prediction": int(prediction[0]),
            "proba_indemne": prediction_proba[0][0],
            "proba_blesse": prediction_proba[0][1],
            "proba_tue": prediction_proba[0][2],
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)