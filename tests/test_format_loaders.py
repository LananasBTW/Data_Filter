import unittest
import os
import sys
import json
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules import file_manager


class TestFormatLoaders(unittest.TestCase):
    """Tests unitaires pour vérifier le chargement des différents formats de fichiers."""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation avant tous les tests."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        
        # Crée le répertoire fixtures s'il n'existe pas (ou lève une erreur si un fichier du même nom existe)
        if cls.fixtures_dir.exists():
            if not cls.fixtures_dir.is_dir():
                raise FileExistsError(f"Un fichier existe avec le même nom que le répertoire fixtures: {cls.fixtures_dir}")
        else:
            cls.fixtures_dir.mkdir(parents=True, exist_ok=True)
        
    def setUp(self):
        """Initialisation avant chaque test."""
        self.fixtures_dir = Path(__file__).parent / "fixtures"
    
    # ========== Tests CSV - Structure ==========
    
    def test_csv_load_structure(self):
        """Test de la structure des données chargées depuis un CSV."""
        csv_path = self.fixtures_dir / "test_structure.csv"
        csv_content = """id,name,score
1,Alice,98.5
2,Bob,87.3"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = file_manager.load_data(str(csv_path))
        
        self.assertIsNotNone(data, "Les données ne doivent pas être None")
        self.assertIsInstance(data, list, "Les données doivent être une liste")
        self.assertEqual(len(data), 2, "Le fichier doit contenir 2 lignes")
        
        for row in data:
            self.assertIsInstance(row, dict, "Chaque ligne doit être un dictionnaire")
    
    def test_csv_load_values(self):
        """Test des valeurs chargées depuis un CSV."""
        csv_path = self.fixtures_dir / "test_values.csv"
        csv_content = """name,age,city
Alice,25,Paris
"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = file_manager.load_data(str(csv_path))
        
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['age'], 25)
        self.assertEqual(data[0]['city'], 'Paris')
    
    def test_csv_load_complex_types(self):
        """Test du chargement de types complexes (listes, floats) depuis un CSV."""
        csv_path = self.fixtures_dir / "test_complex.csv"
        csv_content = """id,name,tags,score
1,Item1,"[""tag1"", ""tag2""]",99.5"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = file_manager.load_data(str(csv_path))
        
        self.assertEqual(data[0]['id'], 1)
        self.assertIsInstance(data[0]['tags'], list, "Les tags doivent être une liste")
        self.assertEqual(data[0]['tags'], ['tag1', 'tag2'])
        self.assertEqual(data[0]['score'], 99.5)
    
    # ========== Tests JSON - Structure ==========
    
    def test_json_load_structure(self):
        """Test de la structure des données chargées depuis un JSON."""
        json_path = self.fixtures_dir / "test_structure.json"
        test_data = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30},
            {"id": 3, "name": "Charlie", "age": 35}
        ]
        json_path.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
        
        data = file_manager.load_data(str(json_path))
        
        self.assertIsNotNone(data, "Les données ne doivent pas être None")
        self.assertIsInstance(data, list, "Les données doivent être une liste")
        self.assertEqual(len(data), 3, "Le fichier doit contenir 3 éléments")
    
    def test_json_load_values(self):
        """Test des valeurs chargées depuis un JSON."""
        json_path = self.fixtures_dir / "test_values.json"
        test_data = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30}
        ]
        json_path.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
        
        data = file_manager.load_data(str(json_path))
        
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['age'], 25)
        self.assertEqual(data[1]['name'], 'Bob')
        self.assertEqual(data[1]['age'], 30)
    
    def test_json_load_complex_structure(self):
        """Test du chargement de structures complexes (objets imbriqués) depuis un JSON."""
        json_path = self.fixtures_dir / "test_complex.json"
        test_data = [
            {
                "id": 1,
                "name": "Item1",
                "tags": ["tag1", "tag2"],
                "metadata": {"category": "A", "priority": 1}
            },
            {
                "id": 2,
                "name": "Item2",
                "tags": ["tag3"],
                "metadata": {"category": "B", "priority": 2}
            }
        ]
        json_path.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
        
        data = file_manager.load_data(str(json_path))
        
        self.assertIsNotNone(data, "Les données ne doivent pas être None")
        self.assertIsInstance(data, list, "Les données doivent être une liste")
        self.assertEqual(len(data), 2, "Le fichier doit contenir 2 éléments")
    
    def test_json_load_complex_values(self):
        """Test du chargement de structures complexes (objets imbriqués) depuis un JSON."""
        json_path = self.fixtures_dir / "test_complex.json"
        test_data = [
            {
                "id": 1,
                "name": "Item1",
                "tags": ["tag1", "tag2"],
                "metadata": {"category": "A", "priority": 1}
            },
            {
                "id": 2,
                "name": "Item2",
                "tags": ["tag3"],
                "metadata": {"category": "B", "priority": 2}
            }
        ]
        json_path.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
        
        data = file_manager.load_data(str(json_path))
        self.assertIsInstance(data[0]['tags'], list)
        self.assertIsInstance(data[0]['metadata'], dict)
        self.assertEqual(data[0]['metadata']['category'], 'A')
        self.assertEqual(data[1]['metadata']['priority'], 2)
    
    # ========== Tests d'erreurs ==========
    
    def test_load_nonexistent_file(self):
        """Test du chargement d'un fichier inexistant."""
        nonexistent_path = self.fixtures_dir / "nonexistent"
        
        with self.assertRaises(FileNotFoundError):
            file_manager.load_data(str(nonexistent_path))
    
    def test_load_invalid_format_file(self):
        """Test du chargement d'un fichier avec un format non supporté."""
        invalid_path = self.fixtures_dir / "invalid_format.txt"
        invalid_path.write_text("This is a test.", encoding='utf-8')
        with self.assertRaises(ValueError):
            file_manager.load_data(str(invalid_path))
    
    def test_load_no_format_file(self):
        """Test du chargement d'un fichier sans extension."""
        no_format_path = self.fixtures_dir / "invalid_format"
        no_format_path.write_text("This is a test.", encoding='utf-8')
        with self.assertRaises(ValueError):
            file_manager.load_data(str(no_format_path))
    
    def test_load_empty_path(self):
        """Test du chargement avec un chemin vide."""
        with self.assertRaises(ValueError):
            file_manager.load_data("")

if __name__ == '__main__':
    unittest.main()
