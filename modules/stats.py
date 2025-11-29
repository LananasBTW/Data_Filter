import config

def analyze_structure(data):
    """
    Analyse la structure des données et calcule des statistiques par champ.
    
    Args:
        data: Liste de dictionnaires représentant les données
        
    Returns:
        dict: Dictionnaire contenant les statistiques par champ
    """
    if not data:
        return {}
    
    # Collecter tous les champs
    all_fields = set()
    for row in data:
        all_fields.update(row.keys())
    
    stats = {}
    
    for field in all_fields:
        field_stats = {
            'type': None,
            'count': 0,
            'null_count': 0
        }
        
        # Collecter toutes les valeurs non-null pour ce champ
        values = []
        bool_values = []
        list_sizes = []
        
        for row in data:
            if field not in row or row[field] is None:
                field_stats['null_count'] += 1
            else:
                value = row[field]
                field_stats['count'] += 1
                
                # Déterminer le type dominant
                if isinstance(value, bool):
                    bool_values.append(value)
                    if field_stats['type'] is None:
                        field_stats['type'] = 'bool'
                elif isinstance(value, (int, float)):
                    values.append(value)
                    if field_stats['type'] is None:
                        field_stats['type'] = 'number'
                elif isinstance(value, list):
                    list_sizes.append(len(value))
                    if field_stats['type'] is None:
                        field_stats['type'] = 'list'
                elif isinstance(value, str):
                    if field_stats['type'] is None:
                        field_stats['type'] = 'str'
        
        # Calculer les statistiques selon le type
        if field_stats['type'] == 'number' and values:
            field_stats['min'] = min(values)
            field_stats['max'] = max(values)
            field_stats['mean'] = sum(values) / len(values)
        
        elif field_stats['type'] == 'bool' and bool_values:
            true_count = sum(1 for v in bool_values if v is True)
            false_count = len(bool_values) - true_count
            total = len(bool_values)
            field_stats['true_percentage'] = (true_count / total) * 100 if total > 0 else 0
            field_stats['false_percentage'] = (false_count / total) * 100 if total > 0 else 0
            field_stats['true_count'] = true_count
            field_stats['false_count'] = false_count
        
        elif field_stats['type'] == 'list' and list_sizes:
            field_stats['list_size_min'] = min(list_sizes)
            field_stats['list_size_max'] = max(list_sizes)
            field_stats['list_size_mean'] = sum(list_sizes) / len(list_sizes)
        
        elif field_stats['type'] == 'str':
            field_stats['sample_values'] = []
            # Prendre quelques exemples de valeurs
            for row in data:
                if field in row and row[field] is not None and isinstance(row[field], str):
                    if row[field] not in field_stats['sample_values']:
                        field_stats['sample_values'].append(row[field])
                    if len(field_stats['sample_values']) >= 3:
                        break
        
        stats[field] = field_stats
    
    return stats
