from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

from .modules import config
from .modules import file_manager as fm
from .modules import filter as my_filter
from .modules import sort as my_sort
from .modules import stats as my_stats

CURRENT_DATA = []
CURRENT_FILEPATH = ""

@api_view(['GET'])
def list_files(request):
    """Renvoie la liste des fichiers disponibles dans le dossier data"""
    try:
        if os.path.exists(config.DATA_DIR):
            files = [f for f in os.listdir(config.DATA_DIR) 
                     if os.path.isfile(os.path.join(config.DATA_DIR, f))]
            return Response({"status": "success", "files": files})
        return Response({"status": "success", "files": []})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)
    
    
@api_view(['POST'])
def load_file(request):
    global CURRENT_DATA, CURRENT_FILEPATH
    path = request.data.get('path')
    
    if not path:
        return Response({"status": "error", "message": "Chemin vide"}, status=400)
        
    try:
        CURRENT_DATA = fm.load_data(path)
        CURRENT_FILEPATH = path
        return Response({
            "status": "success", 
            "count": len(CURRENT_DATA),
            "data": CURRENT_DATA[:50]
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
        filtered = my_filter.filter_data(CURRENT_DATA, field, value)
        CURRENT_DATA = filtered
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
    
@api_view(['POST'])
def preview_file(request):
    """Renvoie les 10 premières lignes du fichier brut pour prévisualisation"""
    path = request.data.get('path')
    
    if not path:
        return Response({"status": "error", "message": "Chemin vide"}, status=400)
    
    try:
        # Construction du chemin complet
        full_path = os.path.join(config.DATA_DIR, path)
        
        if not os.path.exists(full_path):
            return Response({"status": "error", "message": "Fichier introuvable"}, status=404)

        preview_lines = []
        with open(full_path, 'r', encoding='utf-8') as f:
            for _ in range(5):
                line = f.readline()
                if not line: break
                preview_lines.append(line)
                
        return Response({
            "status": "success", 
            "preview": "".join(preview_lines)
        })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)