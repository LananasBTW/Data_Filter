from . import config
from . import utils

def calculate_statistics(data):
    if not data: return {}

    for e in data:
        pass

def analyze_structure(data):
    if not data: return {}
    
    # Collecter tous les champs
    all_fields = utils.get_all_fields(data)
    
    stats = {}
    
    for field in all_fields:
        field_values_per_type = dict()
        field_stats = {
            'type_stats': dict(),
                # "number": {"count": 0, "min": None, "max": None, "mean": None},
                # "bool": {"count": 0, "true_percentage": None, "false_percentage": None, "true_count": None, "false_count": None},
                # "list": {"count": 0, "size_min": None, "size_max": None, "size_mean": None},
                # "str": {"count": 0, "sample_values": []},
            'non_null_count': 0,
            'null_count': 0,
        }
        
        for content in data:
            if field not in content or content[field] is None:
                field_stats['null_count'] += 1
                continue
            
            field_stats['non_null_count'] += 1

            # Déterminer le type de données
            field_type = utils.get_type_str(content[field])
            if field_type in ['unknown', 'None']:
                field_stats['null_count'] += 1
                field_stats['non_null_count'] -= 1
                continue
            
            if utils.type_is_number(field_type):
                field_type = 'number'

            if field_type not in field_values_per_type:
                field_values_per_type[field_type] = []
            field_values_per_type[field_type].append(content[field])

        for ftype, values in field_values_per_type.items():
            print(f"Field: {field}, Type: {ftype}, Values Sample: {values[:2]}")
            if not values: continue
            match ftype:
                case 'number':
                    field_stats['type_stats']['number'] = {
                        'count': len(values),
                        'min': min(values),
                        'max': max(values),
                        'mean': sum(values) / len(values)
                    }
            
                case 'bool':
                    total = len(values)
                    true_count = sum(1 for v in values if v is True)
                    false_count = total - true_count
                    field_stats['type_stats']['bool'] = {
                        'count': len(values),
                        'true_count': true_count,
                        'false_count': false_count,
                        'true_percentage': (true_count / total) * 100 if total > 0 else 0,
                        'false_percentage': (false_count / total) * 100 if total > 0 else 0
                    }
                
                case 'str':
                    field_stats['type_stats']['str'] = {
                        'count': len(values),
                        'sample_values': values[:config.STATS_MAX_SAMPLE_VALUES]
                    }
            
                case 'list':
                    sizes = [len(v) for v in values if isinstance(v, list)]
                    field_stats['type_stats']['list'] = {
                        'count': len(values),
                        'size_min': min(sizes) if sizes else 0,
                        'size_max': max(sizes) if sizes else 0,
                        'size_mean': sum(sizes) / len(sizes) if sizes else 0
                    }
                
                case 'dict':
                    sizes = [len(v) for v in values if isinstance(v, dict)]
                    field_stats['type_stats']['dict'] = {
                        'count': len(values),
                        'size_min': min(sizes) if sizes else 0,
                        'size_max': max(sizes) if sizes else 0,
                        'size_mean': sum(sizes) / len(sizes) if sizes else 0
                    }

        stats[field] = field_stats

    return stats