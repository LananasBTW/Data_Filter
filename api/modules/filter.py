def filter_data(data, field, value, operator="="):
    if not data:
        return []
    
    filtered = []
    for row in data:
        if field not in row:
            continue
            
        item_val = row[field]
        
        try:
            if operator == "=":
                if str(item_val).lower() == str(value).lower():
                    filtered.append(row)
            elif operator == ">" and isinstance(item_val, (int, float)) and isinstance(value, (int, float)):
                if item_val > value:
                    filtered.append(row)
            elif operator == "<" and isinstance(item_val, (int, float)) and isinstance(value, (int, float)):
                if item_val < value:
                    filtered.append(row)
        except:
            continue
            
    return filtered