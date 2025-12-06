from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import sys

# Import de tes modules (assure-toi que le dossier 'modules' a un __init__.py)
from .modules import file_manager as fm
from .modules import filter as my_filter
from .modules import sort as my_sort
from .modules import stats as my_stats

# "Mémoire" globale du serveur pour ce projet simple
# (Attention: en prod, on utiliserait une BDD ou une session)
CURRENT_DATA = []
CURRENT_FILEPATH = ""

@api_view(['POST'])
def load_file(request):
    global CURRENT_DATA, CURRENT_FILEPATH
    path = request.data.get('path')
    
    if not path:
        return Response({"status": "error", "message": "Chemin vide"}, status=400)
        
    try:
        # On utilise ton module file_manager existant
        CURRENT_DATA = fm.load_data(path)
        CURRENT_FILEPATH = path
        return Response({
            "status": "success", 
            "count": len(CURRENT_DATA),
            "data": CURRENT_DATA[:50] # On renvoie juste un aperçu pour ne pas surcharger
        })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)

@api_view(['POST'])
def filter_data(request):
    global CURRENT_DATA
    field = request.data.get('field')
    value = request.data.get('value')
    
    if not CURRENT_DATA:
        return Response({"status": "error", "message": "Aucune donnée chargée"}, status=400)

    try:
        # On appelle ton module filter
        # Note: assure-toi de convertir 'value' dans le bon type si nécessaire côté frontend ou ici
        filtered = my_filter.filter_data(CURRENT_DATA, field, value)
        CURRENT_DATA = filtered # On met à jour la donnée en cours (comme dans le script)
        return Response({
            "status": "success", 
            "count": len(CURRENT_DATA),
            "data": CURRENT_DATA[:50]
        })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)

@api_view(['POST'])
def sort_data(request):
    global CURRENT_DATA
    field = request.data.get('field')
    
    if not CURRENT_DATA:
        return Response({"status": "error", "message": "Aucune donnée chargée"}, status=400)

    try:
        CURRENT_DATA = my_sort.sort_data(CURRENT_DATA, field)
        return Response({
            "status": "success", 
            "data": CURRENT_DATA[:50]
        })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)

@api_view(['GET'])
def get_stats(request):
    global CURRENT_DATA
    if not CURRENT_DATA:
        return Response({"status": "error", "message": "Aucune donnée"}, status=400)
    
    try:
        report = my_stats.analyze_structure(CURRENT_DATA)
        return Response({"status": "success", "report": report})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)

@api_view(['POST'])
def save_file(request):
    global CURRENT_DATA
    path = request.data.get('path')
    
    if not CURRENT_DATA:
        return Response({"status": "error", "message": "Rien à sauvegarder"}, status=400)
        
    try:
        output_path = fm.save_data(CURRENT_DATA, path)
        return Response({"status": "success", "path": output_path})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)