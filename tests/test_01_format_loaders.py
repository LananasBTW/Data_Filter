import unittest
import os
import sys
import json
import shutil
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules import file_manager as fm
import config

class TestFormatLoaders(unittest.TestCase):
    """Tests unitaires pour vérifier le chargement des différents formats de fichiers."""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation avant tous les tests."""
        config.OUTPUT_DIR = str(Path(__file__).parent / "fixtures")
        config.TMP_DIR = str(Path(__file__).parent / "tmp")
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(config.TMP_DIR, exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests."""
        shutil.rmtree(config.OUTPUT_DIR, ignore_errors=True)
        shutil.rmtree(config.TMP_DIR, ignore_errors=True)
        
    def setUp(self):
        """Initialisation avant chaque test."""
        pass # rien à init
    
    # ========== Tests CSV - Structure ==========
    
    def test_csv_load_structure(self):
        """Test de la structure des données chargées depuis un CSV."""
        csv_path = Path(config.OUTPUT_DIR) / "test_structure.csv"
        csv_content = """id,name,score
1,Alice,98.5
2,Bob,87.3"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = fm.load_data(str(csv_path))
        
        self.assertIsNotNone(data, "Les données ne doivent pas être None")
        self.assertIsInstance(data, list, "Les données doivent être une liste")
        self.assertEqual(len(data), 2, "Le fichier doit contenir 2 lignes")
        
        for row in data:
            self.assertIsInstance(row, dict, "Chaque ligne doit être un dictionnaire")
    
    def test_csv_load_values(self):
        """Test des valeurs chargées depuis un CSV."""
        csv_path = Path(config.OUTPUT_DIR) / "test_values.csv"
        csv_content = """name,age,city
Alice,25,Paris
"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = fm.load_data(str(csv_path))
        
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['age'], 25)
        self.assertEqual(data[0]['city'], 'Paris')
    
    def test_csv_load_complex_types(self):
        """Test du chargement de types complexes (listes, floats) depuis un CSV."""
        csv_path = Path(config.OUTPUT_DIR) / "test_complex.csv"
        csv_content = """id,name,tags,score
1,Item1,"[""tag1"", ""tag2""]",99.5"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = fm.load_data(str(csv_path))
        
        self.assertEqual(data[0]['id'], 1)
        self.assertIsInstance(data[0]['tags'], list, "Les tags doivent être une liste")
        self.assertEqual(data[0]['tags'], ['tag1', 'tag2'])
        self.assertEqual(data[0]['score'], 99.5)
    
    def test_csv_load_inconsistent_fields(self):
        """Test du chargement de CSV avec des champs manquants dans certaines lignes."""
        csv_path = Path(config.OUTPUT_DIR) / "test_inconsistent.csv"
        csv_content = """id,name,age,score
1,Alice,25,
2,Bob,,87.5
3,Charlie,30,95.0"""
        csv_path.write_text(csv_content, encoding='utf-8')
        
        data = fm.load_data(str(csv_path))
        
        self.assertEqual(len(data), 3)
        # Les champs vides doivent être des strings vides ou convertis selon le contexte
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['age'], 25)
        # Champ score vide
        self.assertEqual(data[0]['score'], '')
        
        # Ligne avec age manquant
        self.assertEqual(data[1]['age'], '')
    
    # ========== Tests JSON - Structure ==========
    
    def test_json_load_structure(self):
        """Test de la structure des données chargées depuis un JSON."""
        json_path = Path(config.OUTPUT_DIR) / "test_structure.json"
        test_data = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30},
            {"id": 3, "name": "Charlie", "age": 35}
        ]
        json_path.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
        
        data = fm.load_data(str(json_path))
        
        self.assertIsNotNone(data, "Les données ne doivent pas être None")
        self.assertIsInstance(data, list, "Les données doivent être une liste")
        self.assertEqual(len(data), 3, "Le fichier doit contenir 3 éléments")
    
    def test_json_load_values(self):
        """Test des valeurs chargées depuis un JSON."""
        json_path = Path(config.OUTPUT_DIR) / "test_values.json"
        test_data = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30}
        ]
        json_path.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
        
        data = fm.load_data(str(json_path))
        
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['age'], 25)
        self.assertEqual(data[1]['name'], 'Bob')
        self.assertEqual(data[1]['age'], 30)
    
    def test_json_load_complex_structure(self):
        """Test du chargement de structures complexes (objets imbriqués) depuis un JSON."""
        json_path = Path(config.OUTPUT_DIR) / "test_complex.json"
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
        
        data = fm.load_data(str(json_path))
        
        self.assertIsNotNone(data, "Les données ne doivent pas être None")
        self.assertIsInstance(data, list, "Les données doivent être une liste")
        self.assertEqual(len(data), 2, "Le fichier doit contenir 2 éléments")
    
    def test_json_load_complex_values(self):
        """Test du chargement de structures complexes (objets imbriqués) depuis un JSON."""
        json_path = Path(config.OUTPUT_DIR) / "test_complex.json"
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
        
        data = fm.load_data(str(json_path))
        self.assertIsInstance(data[0]['tags'], list)
        self.assertIsInstance(data[0]['metadata'], dict)
        self.assertEqual(data[0]['metadata']['category'], 'A')
        self.assertEqual(data[1]['metadata']['priority'], 2)
    
    # ========== Tests d'erreurs ==========
    
    def test_load_nonexistent_file(self):
        """Test du chargement d'un fichier inexistant."""
        nonexistent_path = Path(config.OUTPUT_DIR) / "nonexistent"
        
        with self.assertRaises(FileNotFoundError):
            fm.load_data(str(nonexistent_path))
    
    def test_load_invalid_format_file(self):
        """Test du chargement d'un fichier avec un format non supporté."""
        invalid_path = Path(config.OUTPUT_DIR) / "invalid_format.txt"
        invalid_path.write_text("This is a test.", encoding='utf-8')
        with self.assertRaises(ValueError):
            fm.load_data(str(invalid_path))
    
    def test_load_no_format_file(self):
        """Test du chargement d'un fichier sans extension."""
        no_format_path = Path(config.OUTPUT_DIR) / "invalid_format"
        no_format_path.write_text("This is a test.", encoding='utf-8')
        with self.assertRaises(ValueError):
            fm.load_data(str(no_format_path))
    
    def test_load_empty_path(self):
        """Test du chargement avec un chemin vide."""
        with self.assertRaises(ValueError):
            fm.load_data("")

if __name__ == '__main__':
    unittest.main()
