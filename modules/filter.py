import config
from modules import stats

def filter_data(data, field=None, operator=None, value=None):
    """
    Filtre les données selon les critères donnés.
    
    Args:
        data: Liste de dictionnaires à filtrer
        field: Nom du champ sur lequel filtrer
        operator: Opérateur de comparaison ('=', '<', '>', '<=', '>=', '!=', 'contains', 'starts_with', 'ends_with')
        value: Valeur de comparaison
        
    Returns:
        list: Liste filtrée de dictionnaires
    """
    if not data:
        return []
    
    if field is None or operator is None:
        return data
    
    filtered = []
    
    for row in data:
        if field not in row:
            continue
        
        field_value = row[field]
        
        # Gérer les valeurs None
        if field_value is None:
            if operator == '=' and value is None:
                filtered.append(row)
            continue
        
        # Appliquer le filtre selon l'opérateur
        if operator == '=':
            if field_value == value:
                filtered.append(row)
        
        elif operator == '!=':
            if field_value != value:
                filtered.append(row)
        
        elif operator == '<':
            if isinstance(field_value, (int, float)) and isinstance(value, (int, float)):
                if field_value < value:
                    filtered.append(row)
            elif isinstance(field_value, str) and isinstance(value, str):
                if field_value < value:
                    filtered.append(row)
            elif isinstance(field_value, list):
                if len(field_value) < value:
                    filtered.append(row)
        
        elif operator == '>':
            if isinstance(field_value, (int, float)) and isinstance(value, (int, float)):
                if field_value > value:
                    filtered.append(row)
            elif isinstance(field_value, str) and isinstance(value, str):
                if field_value > value:
                    filtered.append(row)
            elif isinstance(field_value, list):
                if len(field_value) > value:
                    filtered.append(row)
        
        elif operator == '<=':
            if isinstance(field_value, (int, float)) and isinstance(value, (int, float)):
                if field_value <= value:
                    filtered.append(row)
            elif isinstance(field_value, str) and isinstance(value, str):
                if field_value <= value:
                    filtered.append(row)
            elif isinstance(field_value, list):
                if len(field_value) <= value:
                    filtered.append(row)
        
        elif operator == '>=':
            if isinstance(field_value, (int, float)) and isinstance(value, (int, float)):
                if field_value >= value:
                    filtered.append(row)
            elif isinstance(field_value, str) and isinstance(value, str):
                if field_value >= value:
                    filtered.append(row)
            elif isinstance(field_value, list):
                if len(field_value) >= value:
                    filtered.append(row)
        
        elif operator == 'contains' and isinstance(field_value, str) and isinstance(value, str):
            if value.lower() in field_value.lower():
                filtered.append(row)
        
        elif operator == 'starts_with' and isinstance(field_value, str) and isinstance(value, str):
            if field_value.lower().startswith(value.lower()):
                filtered.append(row)
        
        elif operator == 'ends_with' and isinstance(field_value, str) and isinstance(value, str):
            if field_value.lower().endswith(value.lower()):
                filtered.append(row)
        
        elif operator == 'list_all' and isinstance(field_value, list):
            # Tous les éléments de la liste doivent satisfaire une condition
            # Pour simplifier, on vérifie si tous les éléments sont >, <, ou = à value
            # Cette fonctionnalité peut être étendue
            if all(isinstance(item, (int, float)) and item > value for item in field_value if isinstance(item, (int, float))):
                filtered.append(row)
        
        elif operator == 'list_any' and isinstance(field_value, list):
            # Au moins un élément de la liste doit satisfaire une condition
            if any(isinstance(item, (int, float)) and item > value for item in field_value if isinstance(item, (int, float))):
                filtered.append(row)
    
    return filtered

def filter_by_stats(data, field, operator, stat_type='mean'):
    """
    Filtre les données en comparant avec les statistiques globales.
    Exemple: âge > moyenne des âges
    
    Args:
        data: Liste de dictionnaires
        field: Nom du champ
        operator: Opérateur ('>', '<', '>=', '<=')
        stat_type: Type de statistique ('mean', 'min', 'max')
        
    Returns:
        list: Liste filtrée
    """
    if not data:
        return []
    
    # Calculer les statistiques
    report = stats.analyze_structure(data)
    
    if field not in report or report[field]['type'] != 'number':
        return data
    
    field_stats = report[field]
    
    if stat_type == 'mean' and 'mean' in field_stats:
        threshold = field_stats['mean']
    elif stat_type == 'min' and 'min' in field_stats:
        threshold = field_stats['min']
    elif stat_type == 'max' and 'max' in field_stats:
        threshold = field_stats['max']
    else:
        return data
    
    return filter_data(data, field, operator, threshold)
