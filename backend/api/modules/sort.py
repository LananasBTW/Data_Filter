def sort_data(data, field, reverse=False):
    if not data:
        return []
    
    try:
        return sorted(data, key=lambda x: x.get(field, 0), reverse=reverse)
    except:
        return data