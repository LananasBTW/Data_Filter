"""
Module pour la gestion dynamique des champs (ajout/suppression).
"""

def add_field(data, field_name, default_value=None):
    """
    Ajoute un nouveau champ à toutes les lignes de données.
    
    Args:
        data: Liste de dictionnaires
        field_name: Nom du nouveau champ
        default_value: Valeur par défaut pour le nouveau champ (None si non spécifié)
        
    Returns:
        list: Liste de dictionnaires avec le nouveau champ ajouté
    """
    if not data:
        return data
    
    result = []
    for row in data:
        new_row = row.copy()
        if field_name not in new_row:
            new_row[field_name] = default_value
        result.append(new_row)
    
    return result

def remove_field(data, field_name):
    """
    Supprime un champ de toutes les lignes de données.
    
    Args:
        data: Liste de dictionnaires
        field_name: Nom du champ à supprimer
        
    Returns:
        list: Liste de dictionnaires sans le champ spécifié
    """
    if not data:
        return data
    
    result = []
    for row in data:
        new_row = row.copy()
        if field_name in new_row:
            del new_row[field_name]
        result.append(new_row)
    
    return result

def rename_field(data, old_name, new_name):
    """
    Renomme un champ dans toutes les lignes de données.
    
    Args:
        data: Liste de dictionnaires
        old_name: Ancien nom du champ
        new_name: Nouveau nom du champ
        
    Returns:
        list: Liste de dictionnaires avec le champ renommé
    """
    if not data:
        return data
    
    if old_name == new_name:
        return data
    
    result = []
    for row in data:
        new_row = row.copy()
        if old_name in new_row:
            new_row[new_name] = new_row.pop(old_name)
        result.append(new_row)
    
    return result

def update_field_value(data, field_name, condition_field, condition_operator, condition_value, new_value):
    """
    Met à jour la valeur d'un champ pour les lignes satisfaisant une condition.
    
    Args:
        data: Liste de dictionnaires
        field_name: Nom du champ à mettre à jour
        condition_field: Champ pour la condition
        condition_operator: Opérateur de condition
        condition_value: Valeur de condition
        new_value: Nouvelle valeur à assigner
        
    Returns:
        list: Liste de dictionnaires avec les valeurs mises à jour
    """
    if not data:
        return data
    
    from modules import filter
    
    # Filtrer les lignes qui satisfont la condition
    matching_rows = filter.filter_data(data, condition_field, condition_operator, condition_value)
    
    # Créer un set d'indices pour un accès rapide
    matching_indices = set()
    for i, row in enumerate(data):
        if row in matching_rows:
            matching_indices.add(i)
    
    # Mettre à jour les valeurs
    result = []
    for i, row in enumerate(data):
        new_row = row.copy()
        if i in matching_indices:
            new_row[field_name] = new_value
        result.append(new_row)
    
    return result

def get_field_info(data):
    """
    Retourne des informations sur les champs présents dans les données.
    
    Args:
        data: Liste de dictionnaires
        
    Returns:
        dict: Informations sur les champs (nom, type, présence)
    """
    if not data:
        return {}
    
    all_fields = set()
    for row in data:
        all_fields.update(row.keys())
    
    field_info = {}
    for field in all_fields:
        field_info[field] = {
            'present_in_all': all(field in row for row in data),
            'present_count': sum(1 for row in data if field in row),
            'null_count': sum(1 for row in data if field in row and row[field] is None),
            'total_rows': len(data)
        }
    
    return field_info

