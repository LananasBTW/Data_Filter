import config

def sort_data(data, field=None, reverse=False, fields=None):
    """
    Trie les données selon un ou plusieurs champs.
    
    Args:
        data: Liste de dictionnaires à trier
        field: Nom du champ pour tri simple (déprécié, utiliser fields)
        reverse: True pour tri décroissant, False pour croissant
        fields: Liste de tuples (champ, reverse) pour tri multi-critères
                Exemple: [('lastname', False), ('firstname', False)]
        
    Returns:
        list: Liste triée de dictionnaires
    """
    if not data:
        return []
    
    # Support de l'ancienne API (field simple)
    if field is not None and fields is None:
        fields = [(field, reverse)]
    elif fields is None:
        return data
    
    def sort_key(row):
        """
        Génère une clé de tri pour une ligne.
        Gère les valeurs None en les plaçant à la fin.
        """
        key = []
        for field_name, rev in fields:
            if field_name not in row or row[field_name] is None:
                # None va à la fin, donc on utilise un tuple avec un booléen
                key.append((1, None))  # 1 pour placer après les valeurs normales
            else:
                value = row[field_name]
                # Pour les listes, on trie par taille
                if isinstance(value, list):
                    key.append((0, len(value)))
                else:
                    key.append((0, value))
        return key
    
    try:
        sorted_data = sorted(data, key=sort_key)
        
        # Appliquer l'ordre reverse pour chaque champ
        # On inverse l'ordre global si nécessaire
        if reverse and len(fields) == 1:
            sorted_data = list(reversed(sorted_data))
        elif len(fields) > 1:
            # Pour multi-critères, on doit gérer chaque champ individuellement
            # On va re-trier en appliquant les reverses dans l'ordre
            for i, (field_name, rev) in enumerate(reversed(fields)):
                if rev:
                    # Trier par ce champ en reverse, en préservant l'ordre des champs précédents
                    # C'est complexe, donc on fait un tri stable
                    def key_func(row):
                        if field_name not in row or row[field_name] is None:
                            return (1, None)
                        value = row[field_name]
                        if isinstance(value, list):
                            return (0, len(value))
                        return (0, value)
                    
                    sorted_data = sorted(sorted_data, key=key_func, reverse=rev)
        
        return sorted_data
    
    except Exception as e:
        # En cas d'erreur, retourner les données non triées
        print(f"⚠️ Erreur lors du tri: {e}")
        return data
